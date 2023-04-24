"""Account key store and generation
"""

from base64 import b85encode, b85decode
from dataclasses import dataclass
from ucn.encrypt.encrypt import KEY_ENCRYPT_MAP


@dataclass
class KeyStore:
    """Store key and load or save by json"""

    encrypt_algo: str
    public_key: bytes
    private_key: bytes = None
    passphrase: str or None = None

    def __post_init__(self):
        if self.encrypt_algo not in KEY_ENCRYPT_MAP:
            raise ValueError(f"Invalid encryption algorithm: {self.encrypt_algo}")

    @staticmethod
    def load(key_data: dict[str, str]):
        """Load public or private key from (json) dict"""
        return KeyStore(
            encrypt_algo=key_data["encrypt_algo"],
            public_key=b85decode(key_data["public_key"].encode("utf-8")),
            private_key=b85decode(key_data["private_key"].encode("utf-8")),
        )

    def dump(self) -> dict[str, str]:
        """Dump public or private key to (json) dict"""
        return {
            "public_key": b85encode(self.public_key).decode("utf-8"),
            "private_key": b85encode(self.private_key).decode("utf-8"),
            "encrypt_algo": self.encrypt_algo,
        }

    def set_passphrase(self, passphrase):
        """Set passphrase individually"""
        self.passphrase = passphrase


class Key:
    """Simgle Key store"""

    def __init__(self, keystore: KeyStore):
        self.keystore = keystore

    @property
    def key_encrypt(self):
        """Get KeyEncrypt of the key"""
        return KEY_ENCRYPT_MAP[self.keystore.encrypt_algo]

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
    def key_dict(self):
        """Get key_dict to easy search by kid"""
        return {key.keystore.public_key: key for key in self.key_list}

    def sign(self, data: bytes) -> list[tuple[Key, bytes]]:
        "Sign by keys, one by one"
        return [(key, key.sign(data)) for key in self.key_list]

    def verify(self, data: bytes, key_signature_list: list[tuple[bytes, bytes]]) -> str:
        """Verify data and return fraction(str) of reliability"""
        key_map = self.key_dict
        verified = 0
        total = len(key_map)
        for public_key, signature in key_signature_list:
            try:
                key = key_map[public_key]
                if key.verify(data, signature):
                    verified += 1
            except KeyError:
                pass
        return f"{verified}/{total}"
