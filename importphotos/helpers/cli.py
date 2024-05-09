"""Functions for printing to the terminal"""

import argparse
import datetime
import shutil

from tabulate import tabulate

WIDTH = 86
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
    print("#" * WIDTH)
    print(r"""#  _____                              _____                            _             #
# |_   _|                            |_   _|                          | |            #
#   | |  _ __ ___   __ _  __ _  ___    | |  _ __ ___  _ __   ___  _ __| |_ ___ _ __  #
#   | | | '_ ` _ \ / _` |/ _` |/ _ \   | | | '_ ` _ \| '_ \ / _ \| '__| __/ _ \ '__| #
#  _| |_| | | | | | (_| | (_| |  __/  _| |_| | | | | | |_) | (_) | |  | ||  __/ |    #
# |_____|_| |_| |_|\__,_|\__, |\___| |_____|_| |_| |_| .__/ \___/|_|   \__\___|_|    #
#                         __/ |                      | |                             #
#                        |___/                       |_|                             #""")
    print("#" * WIDTH)
    print('#' + f" Author: {author} # Version {version} ".center(WIDTH-2, '#') + '#')
    print("#" * WIDTH)

def print_header(text : str):
    """Prints a header with the text centered in the middle of the line"""
    print("#" * WIDTH)
    print(f"#{text.center(WIDTH - 2, '#')}#")
    print("#" * WIDTH)

def print_message(message : str):
    """Prints a message"""
    text_width = WIDTH - 4
    while True:
        last_space = find_last_space(message, text_width)
        line = message[0:last_space+1]
        message = message[last_space:]
        print(f"# {line}".ljust(text_width+2, ' ') + ' #')
        if len(message) < text_width:
            break

def print_done():
    """Prints a done message"""
    print_message("DONE!")

def print_table(headers: list, rows : list[list]):
    """Prints a table"""
    lines = tabulate(rows, headers, tablefmt="grid").split('\n')

    if len(lines[0]) > WIDTH:
        print('\n'.join(lines))
        return
    for line in lines:
        print_message(line)

def print_dict(dictionary : dict):
    """Prints a dictionary"""
    for key, value in dictionary.items():
        message = f"# {key} # {value} "
        print(message.ljust(WIDTH - 1, ' ') + '#')


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
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s' % styling.replace(fill, bar), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()

def input_yes_no(prompt : str):
    """Prompt the user for a yes or no response"""
    while True:
        response = input(prompt)
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
        response = input(prompt)
        if not response:
            return response
        try:
            return datetime.datetime.fromisoformat(response)
        except ValueError:
            print("Please enter a valid date in the format YYYY-MM-DD:HH:mm:ss")

def input_custom(prompt : str, func, help_text : str):
    """Prompt the user for a custom input"""
    while True:
        response = input(prompt)
        if not response:
            return response
        try:
            return func(response)
        except argparse.ArgumentTypeError:
            print(f"{help_text}")