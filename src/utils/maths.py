# -*- encoding: utf-8 -*-
# src/utils/maths.py
# Helper functions for mathematical operations.


from decimal import Decimal
from src.utils.logging import log_error


def calculate_surplus(exec_amount, min_amount) -> float:
    """
        Calculate the surplus of an executed limit_sell order 
    """
    return int(exec_amount - min_amount)
