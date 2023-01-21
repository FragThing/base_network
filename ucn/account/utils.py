"""Account Utils
Account New, Import
Key New
"""
from json import loads
from ucn.utils import json_dumps
from ucn.account.key import KeyStore, Key, MultiKey
from ucn.account.wallet import Account
from ucn.account.encrypt import KEY_ENCRYPT_MAP

DEF_ENCRYPT = "Ed25519"


def new_account_by_json(key_store_json: str) -> Account:
    """New account (from private key)"""
    return Account(
        MultiKey(
            [
                Key(__gen_key_store(KeyStore.loads(json_dumps(j))))
                for j in loads(key_store_json)
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
    return json_dumps([loads(key.keystore.dumps()) for key in account.key.key_list])


def import_account(json_str: str) -> Account:
    """Import account from json string"""
    json = loads(json_str)
    return Account(MultiKey([Key(KeyStore.loads(json_dumps(j))) for j in json]))


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
