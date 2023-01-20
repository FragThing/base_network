"""Account key store and generation
"""

from json import loads, dumps
from dataclasses import dataclass
from hashlib import shake_256
from ucn.account.encrypt import KEY_ENCRYPT_MAP


@dataclass
class KeyStore:
    """Store key and load or save by json"""

    public_key: bytes
    private_key: bytes
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

    def __init__(self, keystore: KeyStore, passphrase: str):
        self.passphrase = passphrase
        self.keystore = keystore

    @property
    def key_encrypt(self):
        """Get KeyEncrypt of the key"""
        return KEY_ENCRYPT_MAP[self.keystore.encryt_algo]

    @property
    def hash_id(self) -> str:
        """Hash key as id"""
        shake_256(self.keystore.public_key).hexdigest(8)

    def sign(self, data: bytes) -> bytes:
        """Sign data"""
        return self.key_encrypt.sign(self.keystore.private_key, self.passphrase, data)

    def verify(self, data: bytes, signature: bytes) -> bool:
        """Verify data"""
        return self.key_encrypt.verify(self.keystore.public_key, signature, data)


class MultiKey:
    """Keys store with key_url"""

    HASH_MAP = {"SHAKE256": shake_256}

    def __init__(self, key_list: list[Key], hash_algo: str = "SHAKE256"):
        self.hash_algo = hash_algo
        self.key_list = key_list

    @property
    def key_dict(self):
        """Get key_dict to easy search by kid"""
        return {key.hash_id: key for key in self.key_list}

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
        content_id_hash = shake_256(content_id).hexdigest(64)
        return f"{scheme}://{content_id_hash}"

    def sign(self, data: bytes) -> bytes:
        "Sign by keys, one by one"
        data_sign = b""
        for key in self.key_list:
            data_presign = dumps(
                {
                    "d": data,
                    "kid": key.hash_id,
                },
                separators=(",", ":"),
            ).encode("utf-8")
            data_sign += dumps(
                {"sign": key.sign(data_presign), "d": data_presign},
                separators=(",", ":"),
            ).encode("utf-8")
        return data_sign

    def verify(self, data: bytes) -> str:
        """Verify data and return fraction(str) of reliability"""
        key_map = self.key_dict
        verified = 0
        total = len(key_map)
        while True:
            data_json = loads(data.decode("utf-8"))
            if "kid" not in data_json:
                break
            try:
                data = data_json["d"]
                key = key_map[data_json["kid"]]
                if key.sign(data):
                    verified += 1
            except KeyError:
                pass
        return f"{verified}/{total}"
