# -*- encoding: utf-8 -*-
# src/utils/logging.py
# Helper functions for logging.


import sys
import logging

from pprint import PrettyPrinter


def set_logging(log_level) -> None:
    """Set logging level according to .env config."""

    if log_level == 'info':
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        logging.getLogger('httpx').setLevel(logging.WARNING)  

    elif log_level == 'error':
        logging.basicConfig(level=logging.ERROR, format='%(message)s')
        logging.getLogger('httpx').setLevel(logging.ERROR)  

    elif log_level == 'debug':
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')
        logging.getLogger('httpx').setLevel(logging.DEBUG) 

    else:
        print(f'Logging level {log_level} is not available. Setting to ERROR')
        logging.basicConfig(level=logging.ERROR, format='%(message)s')
        logging.getLogger('httpx').setLevel(logging.ERROR)  


def exit_with_error(message) -> None:
    """Log an error message and halt the program."""
    log_error(message)
    sys.exit(1)


def log_error(string) -> None:
    """Print STDOUT error using the logging library."""
    logging.error('%s', '🛑 ' + string)


def log_info(string) -> None:
    """Print STDOUT info using the logging library."""
    logging.info('%s', string)


def log_debug(string) -> None:
    """Print STDOUT debug using the logging library."""
    logging.debug('%s', string)


def log_debug_object(string: str, object_description: str, obj: 'list | dict') -> None:
    """
    Print debug information for a list or dictionary to STDOUT.
    
    Args:
        string (str): A prefix message to include in the debug output.
        object_description (str): Description to prepend to each item in the object.
        obj (list | dict): The list or dictionary to be logged.
    
    Returns:
        None
    """
    log_debug(string)
    
    if isinstance(obj, list):
        for i, element in enumerate(obj):
            log_debug(f'{object_description} {i}: {str(element)}')
    elif isinstance(obj, dict):
        for key, value in obj.items():
            log_debug(f'{object_description} {key}: {str(value)}')
    else:
        log_debug(f'{object_description}: {str(obj)}')

def pprint(data, indent=None) -> None:
    """Print dicts and data in a suitable format"""
    print()
    indent = indent or 4
    pp = PrettyPrinter(indent=indent)
    pp.pprint(data)
    print()

def hourglass(message : str, index : int) -> int:
    """Print a waiting message"""
    hourglasses = ['⏳', '⌛']  # Symbols to alternate between
    sys.stdout.write(f'\r{hourglasses[index]} ' + message )
    sys.stdout.flush()
    
    # Alternate between hourglass symbols
    index = (index + 1) % len(hourglasses)
    return index
