"""Key Utils
Multi-Key New, Import
Key New
"""
from ucn.encrypt.key import KeyStore, Key, MultiKey
from ucn.encrypt.encrypt import KEY_ENCRYPT_MAP
from ucn.utils import json_dumps

DEF_ENCRYPT = "Ed25519"


def new_multikey_by_json(key_data_list: list[dict[str, str]]) -> MultiKey:
    """New multi-key (from private key)"""
    return MultiKey(
            [
                Key(__gen_key_store(KeyStore.load(j)))
                for j in key_data_list
            ]
        )


def new_single_multikey(encryt_algo=DEF_ENCRYPT) -> MultiKey:
    """New multi-key with single private key from nothing"""
    return new_multikey([KeyStore(encryt_algo=encryt_algo, public_key=None)])


def new_multikey(key_store_list: list[KeyStore]) -> MultiKey:
    """New multi-key (from private key)"""
    return MultiKey([Key(__gen_key_store(key_store)) for key_store in key_store_list])


def export_multikey(multikey: MultiKey) -> str:
    """Export multi-key key list as json"""
    return json_dumps([key.keystore.dump() for key in multikey.key_list])


def import_multikey(key_data_list: list[dict[str, str]]) -> MultiKey:
    """Import multi-key from (json) dict"""
    return MultiKey([Key(KeyStore.load(k)) for k in key_data_list])


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
