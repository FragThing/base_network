"""Account key store and generation
"""

from json import loads
from base64 import b85encode, b85decode
from dataclasses import dataclass
from ucn.utils import json_dumps
from ucn.account.encrypt import KEY_ENCRYPT_MAP


@dataclass
class KeyStore:
    """Store key and load or save by json"""

    encryt_algo: str
    public_key: bytes
    private_key: bytes = None
    passphrase: str or None = None

    @staticmethod
    def loads(json_str: str):
        """Load public or private key from json string"""
        key_store = KeyStore(None, None)
        json = loads(json_str)
        key_store.public_key = b85decode(json["public_key"].encode("utf-8"))
        key_store.private_key = b85decode(json["private_key"].encode("utf-8"))
        key_store.encryt_algo = json["encryt_algo"]
        return key_store

    def dumps(self) -> str:
        """Dump public or private key to json string"""
        return json_dumps(
            {
                "public_key": b85encode(self.public_key).decode("utf-8"),
                "private_key": b85encode(self.private_key).decode("utf-8"),
                "encryt_algo": self.encryt_algo,
            }
        )


class Key:
    """Simgle Key store"""

    def __init__(self, keystore: KeyStore):
        self.keystore = keystore

    @property
    def key_encrypt(self):
        """Get KeyEncrypt of the key"""
        return KEY_ENCRYPT_MAP[self.keystore.encryt_algo]

    def sign(self, data: bytes) -> bytes:
        """Sign data"""
        return self.key_encrypt.sign(
            self.keystore.private_key, self.keystore.passphrase, data
        )

    def verify(self, data: bytes, signature: bytes) -> bool:
        """Verify data"""
        return self.key_encrypt.verify(self.keystore.public_key, signature, data)


class MultiKey:
    """Keys store with key_url"""

    def __init__(self, key_list: list[Key]):
        self.key_list = key_list

    @property
    def decoder(self):
        """Return decoder
        If it is encode by base or other but NOT HASH
        """

    @property
    def key_dict(self):
        """Get key_dict to easy search by kid"""
        return {key.keystore.public_key: key for key in self.key_list}

    def sign(self, data: bytes) -> list[[bytes, bytes]]:
        "Sign by keys, one by one"
        return [(key.keystore.public_key, key.sign(data)) for key in self.key_list]

    def verify(self, data: bytes, signature_list: list[[bytes, bytes]]) -> str:
        """Verify data and return fraction(str) of reliability"""
        key_map = self.key_dict
        verified = 0
        total = len(key_map)
        for signature in signature_list:
            try:
                key = key_map[signature[0]]
                if key.verify(data, signature[1]):
                    verified += 1
            except KeyError:
                pass
        return f"{verified}/{total}"
