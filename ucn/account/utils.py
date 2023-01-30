"""Account Utils
Account New, Import
Key New
"""
from json import loads
from base64 import b85encode, b85decode
from fractions import Fraction
from ucn.account.wallet import Account
from ucn.account.wallet_store import AccountStore
from ucn.encrypt.key import KeyStore, Key, MultiKey
from ucn.encrypt.encrypt import KEY_ENCRYPT_MAP
from ucn.utils import json_dumps

DEF_ENCRYPT = "Ed25519"


def sig_encode(key_signature_list: list[tuple[bytes, bytes]]):
    """Signature bytes encode to str"""
    return json_dumps(
        [(b85encode(sig[0]), b85encode(sig[1])) for sig in key_signature_list]
    )


def sig_decode(sig_str: str) -> list[tuple[bytes, bytes]]:
    """Signature str decode to bytes"""
    return [(b85decode(sig[0]), b85decode(sig[1])) for sig in loads(sig_str)]


def export_account(account: Account) -> str:
    """Export account key list as json"""
    return json_dumps(
        AccountStore(
            encode_algo=account.encode_algo,
            key_store_list=[key.keystore for key in account.key.key_list],
        ).dump()
    )


def import_account(json_str: str) -> Account:
    """Import account from (json) dict"""
    json_data = loads(json_str)
    account_store = AccountStore.load(json_data)
    return Account(
        MultiKey([Key(keystore) for keystore in account_store.key_store_list]),
        encode_algo=account_store.encode_algo,
    )


def export_account_with_sig(account: Account) -> str:
    """A wrap of export_account with signature"""
    account_export_str = export_account(account)
    return json_dumps(
        {
            "sig": sig_encode(account.key.sign(account_export_str.encode("utf-8"))),
            "id": account.id_url,
            "data": account_export_str,
        }
    )


def import_account_with_sig(json_str: str) -> Account or None:
    """A wrap of import_account with check signature"""
    json_data = loads(json_str)
    data = json_data["data"]
    account = import_account(data)
    sig = json_data["sig"]
    account_id = json_data["id"]
    if account.id_url == account_id and int(Fraction(
        account.key.verify(data.encode("utf-8"), sig_decode(sig))
    )):
        return account
    return None


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
