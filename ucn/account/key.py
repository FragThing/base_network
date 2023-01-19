"""Account key store and generation
"""

from json import loads, dumps
from dataclasses import dataclass
from hashlib import shake_256
from ucn.account.encrypt import KEY_ENCRYPT_MAP


@dataclass
class KeyStore:
    """Store key and load or save by json"""

    public_key: str
    private_key: str
    encryt_algo: str

    def loads(self, json_str: str):
        """Load public or private key from json string"""
        json = loads(json_str)
        self.public_key = json["public_key"]
        self.private_key = json["private_key"]
        self.encryt_algo = json["encryt_algo"]

    def dumps(self) -> str:
        """Dump public or private key to json string"""
        return dumps(
            {
                "public_key": self.public_key,
                "private_key": self.private_key,
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


class KeyZip:
    """Keys store with key_url"""

    HASH_MAP = {"SHAKE256": shake_256}

    def __init__(self, key_list: list[Key], hash_algo: str = "SHAKE256"):
        self.hash_algo = hash_algo
        self.key_list = key_list

    @property
    def url(self):
        """Get a url as account id"""
        scheme = "+".join(
            [
                self.hash_algo,
            ]
            + [key.keystore.encryt_algo for key in self.key_list]
        )
        content_id = "".join([key.keystore.public_key for key in self.key_list])
        content_id_hash = shake_256(content_id)
        return f"{scheme}://{content_id_hash}"
