"""Account info
"""
from ucn.account.key import MultiKey
from ucn.account.url_parse import url_parse


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
        return url_parse.generate(self.key.encode_algo, self.key.key_list)
