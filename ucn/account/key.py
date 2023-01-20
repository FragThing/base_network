"""Account key store and generation
"""

from json import loads, dumps
from dataclasses import dataclass
from ucn.account.encrypt import KEY_ENCRYPT_MAP


@dataclass
class KeyStore:
    """Store key and load or save by json"""

    encryt_algo: str
    public_key: bytes
    private_key: bytes = None
    passphrase: str = None

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

    def sign(self, data: bytes) -> bytes:
        """Sign data"""
        return self.key_encrypt.sign(self.keystore.private_key, self.keystore.passphrase, data)

    def verify(self, data: bytes, signature: bytes) -> bool:
        """Verify data"""
        return self.key_encrypt.verify(self.keystore.public_key, signature, data)


class MultiKey:
    """Keys store with key_url"""

    def __init__(self, key_list: list[Key], encode_algo: str = "SHAKE256"):
        self.encode_algo = encode_algo
        self.key_list = key_list

    @property
    def decoder(self):
        """Return decoder
        If it is encode by base or other but NOT HASH
        """

    @property
    def key_dict(self):
        """Get key_dict to easy search by kid"""
        return {key.public_key: key for key in self.key_list}

    def sign(self, data: bytes) -> list((bytes, bytes)):
        "Sign by keys, one by one"
        return [(key.public_key, key.sign(data)) for key in self.key_list]

    def verify(self, data: bytes, signature_list: list((bytes, bytes))) -> str:
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
