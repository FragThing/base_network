"""Account info
"""
from .key import KeyZip


class Account:
    """Account info saving class"""


class SubAccount:
    """Subaccount which is same private key but different public key"""

    def __init__(self, key: KeyZip):
        self.key = key

    @property
    def id_url(self) -> str:
        return self.key.url
