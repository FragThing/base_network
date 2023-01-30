"""Account info
"""
from ucn.encrypt.key import MultiKey
from ucn.encrypt.key_url import key_url


class Account:
    """Account info saving class
    No need Subaccount which is same private key but different public key
    Like Bake Card
    """

    def __init__(self, key: MultiKey, encode_algo: str):
        self.key = key
        self.encode_algo = encode_algo

    @property
    def id_url(self) -> str:
        """Account id"""
        return key_url.generate(self.key.key_list, self.encode_algo)

    @property
    def credit(self) -> float:
        """Account credit
        High credit means low pay costs
        Low credit means a lot of limit, such as can't pay
        """

    @property
    def balance(self) -> float:
        """Account balance for pay"""
