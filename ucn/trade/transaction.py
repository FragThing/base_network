"""Transaction Data"""

from dataclasses import dataclass


@dataclass
class Transaction:
    input_balance = None
    output_balance = None
    checker_program = None
