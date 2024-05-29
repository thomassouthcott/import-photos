"""Main module for ImportPhotos"""
import argparse
import configparser as configParser
import datetime
import os

from importphotos.args import ArgumentParser
from importphotos.config import Config
from importphotos.helpers.cli import print_banner, print_dict, print_header, print_message, print_done, input_custom, input_date, input_yes_no
from importphotos.lib import Folder, ImportJob, DeleteJob
from importphotos.validators import FileValidator

#TODO: Change all uses of "Photo" to "Image" to be more generic, do this for the classes as well
def main():
    """Main function for ImportPhotos.py"""
    print_banner("Thomas Southcott", 1.1)

    #Parse arguments
    parser = ArgumentParser()
    args = parser.parse_args()

    #Get configuration and args
    try:
        config = Config()
        if args.verbose:
            print_header('Configuration:',2)
            print_message(config)
        if args.verbose:
            print_header('Arguments:',2)
            print_message(args)

    except configParser.Error as exc:
        print_message(f"Error reading configuration file.")
        print_message(exc.message)
        input("# Press Enter to exit...")
        exit(1)
    
    except argparse.ArgumentError as exc:
        print_message(f"Error parsing arguments.")
        print_message(exc.message)
        input("# Press Enter to exit...")
        exit(1)

    source_dir = args.path is not None if args.path else config.source_dir
    destination_dir = args.destination is not None if args.destination else config.destination_dir
    file_extensions = args.extension is not None if args.extension else config.file_types
    
    #Interactive Mode for missing arguments
    if args.interactive and not args.path:
        print_message(f"Please provide a source directory. Press Enter to use currently selected. {source_dir}")
        tmp = input_custom('Enter the source directory: ', FileValidator.file_path, 'Please enter a valid directory path')
        source_dir = tmp if tmp else source_dir
    if args.interactive and not args.destination:
        print_message(f"Please provide a destination directory. Press Enter to use currently selected. {destination_dir}")
        tmp = input_custom('Enter the destination directory: ', FileValidator.file_path, 'Please enter a valid directory path')
        destination_dir = tmp if tmp else destination_dir
    if args.interactive and not args.extension:
        print_message(f"Please provide a file type. Press Enter to use currently selected. {file_extensions}")
        tmp = input_custom('Enter the file types: ', FileValidator.file_extension, 'Please enter a valid file extension')
        file_extensions = tmp if tmp else file_extensions

    #Search for files
    print_header('Searching for Photos',2)
    source_photos = Folder(source_dir)
    if not args.recursive and args.interactive:
        print_message(f"Do you want to search for photos in subfolders of {source_dir}? (Y/N)")
        args.recursive = input_yes_no("Enter Y/N: ")
    print_message(f"Searching for photos in {source_dir}{" and subfolders" if args.recursive else ""} with extensions {file_extensions}")
    found_photos = source_photos.get_files_with_extension(file_extensions, args.recursive, args.verbose)
    if found_photos == 0:
        print_message(f"No photos found in {source_dir}{" and subfolders" if args.recursive else ""}. Exiting.")
        input("# Press Enter to exit...")
        exit()
    
    #Filter by date
    if args.date_search is None and args.interactive:
        print_message("Please provide a date range to filter for. Press Enter to skip.")
        start = input_date("Enter Start Date (YYYY-MM-DD:HH:mm:ss): ")
        if start:
            print_message("Please provide an end date to filter for. Press Enter for now.")
            end = input_date("Enter End Date (YYYY-MM-DD:HH:mm:ss): ")
            if end:
                args.date_search = (start, end)
            else:
                args.date_search = (start, datetime.datetime.now())
    if args.date_search is not None:
        print_message(f"Filtering photos by date taken between {args.date_search[0]} and {args.date_search[1]}")
        selected_photos=source_photos.filter_by_date(args.date_search[0], args.date_search[1], args.verbose)
        if len(selected_photos) == 0:
            print_message("No photos found in date range. Exiting.")
            input("# Press Enter to exit...")
            exit()
    
    #Create Jobs
    if ((not args.overwrite or not args.foldername) and args.interactive) or args.verbose:
        print_header('Creating Jobs from selected photos')
    if not args.overwrite and args.interactive:
        print_message("Do you want to overwrite existing photos in the destination folder? (Y/N)")
        args.overwrite = input_yes_no("Enter Y/N: ")
    if not args.foldername and args.interactive:
        print("Please provide a folder name to copy photos to. Press Enter to sort by year-month.")
        tmp = input("Enter folder name: ")
        if tmp:
            args.foldername = tmp
    jobs = dict()

    if args.foldername:
        if args.verbose:
            print_message(f"Copying {len(source_photos.photos)} selected photos to {os.path.join(destination_dir, args.foldername)}")
        jobs[args.foldername] = ImportJob(source_photos.photos, os.path.join(destination_dir, args.foldername), args.overwrite)
    else:
        jobs = ImportJob(source_photos, destination_dir, args.overwrite).sort_files_by_date(args.verbose)
        if args.verbose:
            print_message(f"Copying {len(source_photos.photos)} selected photos to {destination_dir} sorted by year-month")
            print_dict(jobs)
    print_header(f'Executing {len(jobs)} Import Job{"" if len(jobs) == 1 else "s"}',2)
    import_results = [], [], []
    for i, job in enumerate(jobs.values()):
        job_result = job.execute(i+1, args.verbose)
        import_results[0].extend(job_result[0])
        import_results[1].extend(job_result[1])
        import_results[2].extend(job_result[2])

    #Delete Job
    if not args.move and args.interactive:
        args.move = input_yes_no(f"Do you want to delete the source photos ({len(import_results[0])})? (Y/N)")
    if args.move:
        delete_results = [],[]
        if len(import_results[0]) > 0:
            copied_folder = Folder(source_dir)
            print_header('Deleting Photos',2)
            for photo in import_results[0]:
                copied_folder.add_photo(photo)
            delete_job = DeleteJob(copied_folder)
            delete_results = delete_job.execute(0, args.verbose)

    print_header("Results", 2)
    print_header("Import Results")
    print_message(f"Successfully copied {len(import_results[0])} photos")
    if args.verbose and len(import_results[0]) > 0:
        print_message(import_results[0])
    print_message(f"Failed to copy {len(import_results[1])} photos")
    if args.verbose and len(import_results[1]) > 0:
        print_message(import_results[1])
    print_message(f"Skipped {len(import_results[2])} photos")
    if args.verbose and len(import_results[2]) > 0:
        print_message(import_results[2])
    if args.move:
        print_header("Delete Results")
        if (len(delete_results[0]) <= 0 and len(delete_results[1]) <= 0):
            print_message("No photos to delete")
        else:
            print_message(f"Successfully deleted {len(delete_results[0])} photos")
            if args.verbose and len(delete_results[0]) > 0:
                print_message(delete_results[0])
            print_message(f"Failed to delete {len(delete_results[1])} photos")
            if args.verbose and len(delete_results[1]) > 0:
                print_message(delete_results[1])
    print_done()
    try:
        input("# Press enter to exit...")
    except EOFError:
        pass
