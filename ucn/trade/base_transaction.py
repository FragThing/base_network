"""Base Transaction Data"""

from dataclasses import dataclass


@dataclass
class OutputBalance:
    """Transaction: Single output balance item"""

    coin_hash: str
    coin_num: int
    sign: bytes


@dataclass
class InputBalance:
    """Transaction: Single input balance item"""

    account: str
    coin_num: int


@dataclass
class PaidBalance:
    """FreeBalance: Single paid balance item"""

    timestamp: int
    account: str
    coin_num: int
    sign_account: str
    sign: bytes


@dataclass
class FreeBalance:
    """Free balance
    Free balance like gas int ETH
    Arch look like Transaction
    """

    prepay_balance: list[OutputBalance]
    paid_balance: list[PaidBalance]


@dataclass
class Transaction:
    """Base Transaction data class"""

    timestamp: int
    input_balance: list[InputBalance]
    output_balance: list[OutputBalance]
    free_balance: FreeBalance
    checker_program = None
