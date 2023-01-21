"""Account Utils
Account New, Import
Key New
"""
from ucn.account.wallet import Account
from ucn.encrypt.key import KeyStore, Key, MultiKey
from ucn.encrypt.encrypt import KEY_ENCRYPT_MAP
from ucn.utils import json_dumps

DEF_ENCRYPT = "Ed25519"


def new_account_by_json(key_data_list: list[dict[str, str]]) -> Account:
    """New account (from private key)"""
    return Account(
        MultiKey(
            [
                Key(__gen_key_store(KeyStore.load(j)))
                for j in key_data_list
            ]
        )
    )


def new_single_key_account(encryt_algo=DEF_ENCRYPT) -> Account:
    """New account with single private key from nothing"""
    return new_account([KeyStore(encryt_algo=encryt_algo, public_key=None)])


def new_account(key_store_list: list[KeyStore]) -> Account:
    """New account (from private key)"""
    return Account(
        MultiKey([Key(__gen_key_store(key_store)) for key_store in key_store_list])
    )


def export_account(account: Account) -> str:
    """Export account key list as json"""
    return json_dumps([key.keystore.dump() for key in account.key.key_list])


def import_account(key_data_list: list[dict[str, str]]) -> Account:
    """Import account from (json) dict"""
    return Account(MultiKey([Key(KeyStore.load(k)) for k in key_data_list]))


def __gen_key_store(key_store: KeyStore) -> KeyStore:
    """Generate private key or public key for KeyStore"""
    key_encrypt = KEY_ENCRYPT_MAP[key_store.encryt_algo]
    if not key_store.private_key:
        key_store.private_key = key_encrypt.generate_private_key(key_store.passphrase)
    if not key_store.public_key:
        key_store.public_key = key_encrypt.generate_public_key(
            key_store.private_key, key_store.passphrase
        )
    return key_store
