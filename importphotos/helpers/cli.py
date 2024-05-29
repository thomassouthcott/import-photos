"""Functions for printing to the terminal"""

import argparse
import datetime
import shutil

from tabulate import tabulate

def width():
    """Returns the width of the terminal"""
    return shutil.get_terminal_size(fallback = (100, 1))[0] -1

def find_last_space(text : str, width : int):
    """Find the last space in the text before the width"""
    if len(text) < width:
        return len(text) - 1
    for i in range(width - 1, 0, -1):
        if text[i] == ' ':
            return i
    return width-1

def print_banner(author : str, version : float):
    """Prints the banner for the program"""
    print("#" * width())
    print("#" + r"  _____                              _____                            _             ".center(width()-2, ' ') + '#')
    print("#" + r" |_   _|                            |_   _|                          | |            ".center(width()-2, ' ') + '#')
    print("#" + r"   | |  _ __ ___   __ _  __ _  ___    | |  _ __ ___  _ __   ___  _ __| |_ ___ _ __  ".center(width()-2, ' ') + '#')
    print("#" + r"   | | | '_ ` _ \ / _` |/ _` |/ _ \   | | | '_ ` _ \| '_ \ / _ \| '__| __/ _ \ '__| ".center(width()-2, ' ') + '#')
    print("#" + r"  _| |_| | | | | | (_| | (_| |  __/  _| |_| | | | | | |_) | (_) | |  | ||  __/ |    ".center(width()-2, ' ') + '#')
    print("#" + r" |_____|_| |_| |_|\__,_|\__, |\___| |_____|_| |_| |_| .__/ \___/|_|   \__\___|_|    ".center(width()-2, ' ') + '#')
    print("#" + r"                         __/ |                      | |                             ".center(width()-2, ' ') + '#')
    print("#" + r"                        |___/                       |_|                             ".center(width()-2, ' ') + '#')
    print("#" * width())
    half = int(width()/2)-1
    print('#' + f" Author: {author} ".center(half-1 if width() % 2 == 0 else half, ' ') + '#' +f" Version {version} ".center(half, ' ') + '#')
    print("#" * width())
    print_message("Welcome to the Import Photos program. This program is designed to help you import photos from a camera or phone into a folder on your computer. It can automatically sort the photos into folders based on the date they were taken or copy to a given folder name.")

def print_header(text : str, strength : int = 1):
    """Prints a header with the text centered in the middle of the line"""
    if strength > 1:
        print("#" * width())
        print(f"#{text.center(width() - 2, ' ')}#")
        print("#" * width())
    else:
        print(f"#{f" {text} ".center(width() - 2, '#')}#")

def print_message(message : str):
    """Prints a message"""
    message = str(message)
    message = message.strip()
    while len(message) > width() - 2:
        last_space = find_last_space(message, width() -  4)
        print(f"# {message[:last_space+1].ljust(width()-4, ' ')} #")
        message = message[last_space + 1:]
    print(f"# {message.ljust(width() - 4, ' ')} #")

def print_done():
    """Prints a done message"""
    print_header("DONE!")

def print_table(headers: list, rows : list[list]):
    """Prints a table"""
    lines = tabulate(rows, headers, tablefmt="grid").split('\n')
    for line in lines:
        if len(line) > width() - 4:
            print(line)
        else:
            print_message(line)

def print_dict(dictionary : dict):
    """Prints a dictionary"""
    for key, value in dictionary.items():
        message = f"# {key} # {value} ".ljust(width() - 1, ' ') + "#"
        print(message)


#From https://gist.github.com/greenstick/b23e475d2bfdc3a82e34eaa1f6781ee4
def print_progress_bar (iteration : int, total : int, prefix = '', suffix = '', decimals = 1, length = 56, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        autosize    - Optional  : automatically resize the length of the progress bar to the terminal window (Bool)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    styling = '%s |%s| %s%% %s' % (prefix, fill, percent, suffix)
    cols, _ = shutil.get_terminal_size(fallback = (width(), 1))
    length = cols - len(styling) - 2
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r# %s' % styling.replace(fill, bar), end = '#\r')
    # Print New Line on Complete
    if iteration == total:
        print()

def input_yes_no(prompt : str):
    """Prompt the user for a yes or no response"""
    while True:
        response = input(f"# {prompt}")
        if not response:
            return False
        if response[0].upper() == "Y":
            return True
        if response[0].upper() == "N":
            return False
        else:
            print("Please enter Y or N")

def input_date(prompt : str):
    """Prompt the user for a date"""
    while True:
        response = input(f"# {prompt}")
        if not response:
            return response
        try:
            return datetime.datetime.fromisoformat(response)
        except ValueError:
            print("Please enter a valid date in the format YYYY-MM-DD:HH:mm:ss")

def input_custom(prompt : str, func, help_text : str):
    """Prompt the user for a custom input"""
    while True:
        response = input(f"# {prompt}")
        if not response:
            return response
        try:
            return func(response)
        except argparse.ArgumentTypeError:
            print(f"{help_text}")