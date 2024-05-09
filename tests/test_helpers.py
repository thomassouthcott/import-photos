import argparse
import datetime

from tabulate import tabulate

from importphotos.helpers.cli import _find_last_space, print_banner, print_header, print_message, print_done, print_dict, print_progress_bar, print_table, input_yes_no, input_date, input_custom

def test_find_last_space():
    assert _find_last_space('This is a test', 15) == 13
    assert _find_last_space('This is a test', 10) == 9
    assert _find_last_space('This is a test', 5) == 4
    assert _find_last_space('This is a test', 3) == 2
    assert _find_last_space('This is a test', 1) == 0

def test_print_banner(capsys):
    print_banner('John Doe', 1.0)
    captured = capsys.readouterr()
    assert captured.out == r"""######################################################################################
#  _____                              _____                            _             #
# |_   _|                            |_   _|                          | |            #
#   | |  _ __ ___   __ _  __ _  ___    | |  _ __ ___  _ __   ___  _ __| |_ ___ _ __  #
#   | | | '_ ` _ \ / _` |/ _` |/ _ \   | | | '_ ` _ \| '_ \ / _ \| '__| __/ _ \ '__| #
#  _| |_| | | | | | (_| | (_| |  __/  _| |_| | | | | | |_) | (_) | |  | ||  __/ |    #
# |_____|_| |_| |_|\__,_|\__, |\___| |_____|_| |_| |_| .__/ \___/|_|   \__\___|_|    #
#                         __/ |                      | |                             #
#                        |___/                       |_|                             #
######################################################################################
########################### Author: John Doe # Version 1.0 ###########################
######################################################################################
"""

def test_print_header(capsys):
    print_header('This is a test')
    captured = capsys.readouterr()
    assert captured.out == r"""######################################################################################
####################################This is a test####################################
######################################################################################
"""

def test_print_message(capsys):
    print_message('This is a test')
    captured = capsys.readouterr()
    assert captured.out == r"""# This is a test                                                                     #
"""

def test_print_done(capsys):
    print_done()
    captured = capsys.readouterr()
    assert captured.out == r"""# DONE!                                                                              #
"""

def test_print_table(mocker, capsys):
    print_table(['Header 1', 'Header 2'], [['Row 1-1', 'Row 1-2'], ['Row 2-1', 'Row 2-2']])
    captured = capsys.readouterr()
    assert captured.out == r"""# +------------+------------+                                                        #
# | Header 1   | Header 2   |                                                        #
# +============+============+                                                        #
# | Row 1-1    | Row 1-2    |                                                        #
# +------------+------------+                                                        #
# | Row 2-1    | Row 2-2    |                                                        #
# +------------+------------+                                                        #
"""
    headers = ['Header 1' * 60, 'Header 2']
    rows = [['Row 1-1', 'Row 1-2'], ['Row 2-1', 'Row 2-2']]
    print_table(headers, rows)
    captured = capsys.readouterr()
    assert captured.out == tabulate(rows, headers, tablefmt="grid") + '\n'

def test_print_dict(capsys):
    print_dict({'key1': 'value1', 'key2': 'value2'})
    captured = capsys.readouterr()
    assert captured.out == r"""# key1 # value1                                                                      #
# key2 # value2                                                                      #
"""

def test_print_progress_bar(capsys):
    print_progress_bar(0, 10, length=10)
    captured = capsys.readouterr()
    assert captured.out == """\r |----------| 0.0% \r"""
    print_progress_bar(5, 10, length=10)
    captured = capsys.readouterr()
    assert captured.out == """\r |█████-----| 50.0% \r"""
    print_progress_bar(10, 10, length=10)
    captured = capsys.readouterr()
    assert captured.out == """\r |██████████| 100.0% \r\n"""

def test_input_yes_no(mocker, capsys):
    mocker.patch('builtins.input', return_value=None)
    assert input_yes_no('Are you sure?') == False
    mocker.patch('builtins.input', return_value='y')
    assert input_yes_no('Are you sure?') == True
    mocker.patch('builtins.input', return_value='n')
    assert input_yes_no('Are you sure?') == False
    mocker.patch('builtins.input', side_effect=['a', 'y'])
    assert input_yes_no('Are you sure?') == True
    captured = capsys.readouterr()
    assert captured.out == 'Please enter Y or N\n'

def test_input_date(mocker, capsys):
    mocker.patch('builtins.input', return_value=None)
    assert input_date('Enter a date') == None
    mocker.patch('builtins.input', return_value='2021-01-01:00:00:00')
    assert input_date('Enter a date') == datetime.datetime.fromisoformat('2021-01-01:00:00:00')
    mocker.patch('builtins.input', side_effect=['2021-01-32','2021-01-01:00:00:00'])
    assert input_date('Enter a date') == datetime.datetime.fromisoformat('2021-01-01:00:00:00')
    captured = capsys.readouterr()
    assert captured.out == 'Please enter a valid date in the format YYYY-MM-DD:HH:mm:ss\n'

def test_input_custom(mocker, capsys):
    mocker.patch('builtins.input', return_value=None)
    assert input_custom('Enter a date', lambda x:x, "Help text") == None
    def throw_error(x):
        if x == 'error':
            raise argparse.ArgumentTypeError(x)
        return x
    mocker.patch('builtins.input', side_effect=['error', 'test'])
    assert input_custom('Enter a value', throw_error, 'Help text') == 'test'
    captured = capsys.readouterr()
    assert captured.out == 'Help text\n'