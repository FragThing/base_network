"""Account key encryption"""
from Crypto.PublicKey import ECC
from Crypto.Signature import eddsa
from Crypto.Hash import SHA512
from abc import ABCMeta, abstractmethod


KEY_EXPORT_FORMAT = "DER"
KEY_EXPORT_PROTECTION = "PBKDF2WithHMAC-SHA1AndAES128-CBC"


def save_key_to_file(file_path: str, key_str: str):
    """Save key or otherthing in a file, use x tag a void overwrite"""
    # tag x for avoid overwrite exist pem file
    with open(file_path, "x", encoding="utf-8") as f:
        f.write(key_str)


class KeyEncrypt(metadata=ABCMeta):
    """KeyEncrypt base class, for define function"""

    @staticmethod
    @property
    @abstractmethod
    def name():
        """Encryt algorithm name"""

    @abstractmethod
    def gennerate_private_key(self, passphrase: str) -> str:
        """Gennerate private_key
        if need, use passphrase to protect private_key
        """

    @abstractmethod
    def gennerate_public_key(self, private_key_data, passphrase: str) -> str:
        """Gennerate public_key from a private_key
        if need, passphrase for decode private_key
        """

    @abstractmethod
    def get_hash_content(self, public_key: str) -> str:
        """Get content from a public_key which should been hash
        Generally hash algorithm use SHA3 256 or better
        """

    @abstractmethod
    def sign(self, private_key_data, passphrase: str, data: bytes) -> bytes:
        """Sign data by private_key"""

    @abstractmethod
    def verify(self, public_key_data, signature: bytes, data: bytes) -> bool:
        """Sign data by private_key"""


class Ed25519KeyEncrypt(KeyEncrypt):
    """ECC Ed25519 KeyEncrypt"""

    @staticmethod
    @property
    def name():
        return "Ed25519"

    def gennerate_private_key(self, passphrase: str) -> str:
        key = ECC.generate(curve="Ed25519")
        key_str = key.export_key(
            passphrase=passphrase,
            protection=KEY_EXPORT_PROTECTION,
            format=KEY_EXPORT_FORMAT,
        )
        return key_str

    def gennerate_public_key(self, private_key_data, passphrase: str) -> str:
        key = ECC.import_key(private_key_data, passphrase=passphrase)
        public_key_str = key.publickey().export_key(format=KEY_EXPORT_FORMAT)
        return public_key_str

    def get_hash_content(self, public_key) -> str:
        return public_key

    def sign(self, private_key_data: str, passphrase: str, data: bytes) -> bytes:
        key = ECC.import_key(private_key_data, passphrase=passphrase)
        signer = eddsa.new(key, mode="rfc8032")
        prehashed_data = SHA512.new(data)
        return signer.sign(prehashed_data)

    def verify(self, public_key_data: str, signature: bytes, data: bytes) -> bool:
        key = ECC.import_key(public_key_data)
        verifier = eddsa.new(key, mode="rfc8032")
        try:
            verifier.verify(data, signature)
            print("The message is authentic")
            print(True)
        except ValueError:
            print("The message is not authentic")
            print(False)


KEY_ENCRYPT_MAP = dict((key.name, key()) for key in KeyEncrypt.__subclasses__())
