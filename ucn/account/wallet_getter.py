"""Get Account"""
from ucn.account.wallet import Account
from ucn.encrypt.key import MultiKey

from ucn.encrypt.key_url import key_url


def get_account(url: str) -> Account:
    """Get account from url"""
    key_list = key_url.parse(url)
    if key_list:
        return Account(key=MultiKey(key_list))
