Import Photos
=============
<i>A Python tool for importing photos from a SD / Camera / Phone. </i>

Sync photos from source folder to destination folder, examines EXIF data for date taken. Optionally can filter by timestamp and sort into folders by year-month.

## Installation
Edit importphotos/config.ini.
<b>Example Config</b> - <i>config.ini</i>

    source_dir = D:\DCIM\
    destination_dir = C:\Users\thomassouthcott\Pictures\Camera Roll
    file_types = .jpg .jpeg .png .cr2 .arw .mp4

Then install with pip. (Remember to check privileges)

    pip install .


## Usage
    $ import_photos.py [-h] [-r] [-m] [-s start-dtm end-dtm] [-i] [-e EXTENSION [EXTENSION ...]] [--version] [-p PATH]
                        [-o DESTINATION] [-d] [-w] [-v]
                        [foldername]
### Positional Arguments
<b><i>Optional</i></b>
Name of the sub-folder to copy files to. If not provided, will sort by year-month.

    foldername

### Options
<b><i>All Optional</i></b>
| Option | Description |
| ------ | ----------- |
|  <i>-h, --help</i>          |  show this help message and exit |
  <i>-r, --recursive</i>      | Recursively search for files in subfolders of source folder. |
  <i>-m, --move </i>          | Deletes source files after copying. |
  <i>-s, --date-search start-dtm end-dtm</i> | Filter source files by start and end date. ISOformat - YYYY-MM-DD:HH:mm:ss |
  <i>-i, --interactive</i>    | Interactive mode.
  <i>-e, --extension EXTENSION [EXTENSION ...]</i>| File extension to search for in source folder. |
  <i>--version</i>            | show program's version number and exit |
  <i>-p, --path PATH</i> | Path to source folder. |
  <i>-o, --destination DESTINATION</i> | Path to destination folder. |
  <i>-d, --dry-run</i>        | Dry run. Does not copy files. |
  <i>-w, --overwrite </i>     | Overwrite files in destination folder. |
  <i>-v, --verbose </i>       | Verbose output. |

## Special Thanks
Here are some useful projects and answers I found that helped me out. Thank you.
[wimglenn/JonnyDep](https://github.com/wimglenn/johnnydep)
[greenstick/print-progress-auto.py](https://gist.github.com/greenstick/b23e475d2bfdc3a82e34eaa1f6781ee4)
