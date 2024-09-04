# -*- encoding: utf-8 -*-
# utils/file_operations.py

import os
import json

from typing import Dict, Any
from fastapi import HTTPException


def load_data(file_path: str) -> Dict[str, Any]:
    """Load data from a given JSON file path."""
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r") as file:
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=500, detail=f"Error decoding JSON: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


def save_data(file_path: str, data: Dict[str, Any]):
    """Save data overwriting on a given JSON file path."""
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
