"""Account info
"""
from .key import MultiKey


class Account:
    """Account info saving class
    No need Subaccount which is same private key but different public key
    Like Bake Card
    """

    def __init__(self, key: MultiKey):
        self.key = key

    @property
    def id_url(self) -> str:
        """Account id"""
        return self.key.url
