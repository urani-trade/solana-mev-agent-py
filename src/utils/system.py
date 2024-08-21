# -*- encoding: utf-8 -*-
# src/utils/system.py
# Helper functions for system operations.

import os
import json
import copy
from src.utils.logging import log_error, exit_with_error


def deep_copy(dict_to_clone) -> dict:
    """Deep copy (not reference copy) to a dict."""
    return copy.deepcopy(dict_to_clone)


def save_output(destination, data) -> None:
    """Save data from memory to a destination in disk."""
    try:
        with open(destination, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4)

    except (IOError, TypeError) as e:
        log_error(f'Could not save {destination}: {e}')


def create_dir(result_dir) -> None:
    """Check whether a directory exists and create it if needed."""
    try:
        if not os.path.isdir(result_dir):
            os.mkdir(result_dir)

    except OSError as e:
        log_error(f'Could not create {result_dir}: {e}')


def get_timestamp_formatted(unix_timestamp: int) -> str:
    """Convert a Unix timestamp to human-readable format."""

    if unix_timestamp < 60:
        return f'{unix_timestamp} seconds'

    elif unix_timestamp < 3600:
        minutes = unix_timestamp // 60
        seconds = unix_timestamp % 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} and {seconds} second{'s' if seconds > 1 else ''}"

    elif unix_timestamp < 86400:
        hours = unix_timestamp // 3600
        minutes = (unix_timestamp % 3600) // 60
        return f"{hours} hour{'s' if hours > 1 else ''}, {minutes} minute{'s' if minutes > 1 else ''}"

    elif unix_timestamp < 604800:
        days = unix_timestamp // 86400
        hours = (unix_timestamp % 86400) // 3600
        return f"{days} day{'s' if days > 1 else ''}, {hours} hour{'s' if hours > 1 else ''}"

    elif unix_timestamp < 2629746:
        weeks = unix_timestamp // 604800
        days = (unix_timestamp % 604800) // 86400
        return f"{weeks} week{'s' if weeks > 1 else ''}, {days} day{'s' if days > 1 else ''}"

    else:
        months = unix_timestamp // 2629746
        days = (unix_timestamp % 2629746) // 86400
        return f"{months} month{'s' if months > 1 else ''}, {days} day{'s' if days > 1 else ''}"


def open_json(filepath) -> dict:
    """Load and parse a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as infile:
            return json.load(infile)

    except (IOError, FileNotFoundError, TypeError) as e:
        exit_with_error(f'Failed to parse: "{filepath}": {e}')


def open_file(filepath) -> str:
    """Load and parse a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as infile:
            return infile.read()
    except (IOError, FileNotFoundError, TypeError) as e:
        exit_with_error(f'Failed to parse: "{filepath}": {e}')
