"""Account key encryption"""
from Crypto.PublicKey import ECC
from abc import ABCMeta, abstractmethod


KEY_EXPORT_FORMAT = "PEM"
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
    def gennerate_public_key(self, private_key_str: str, passphrase: str) -> str:
        """Gennerate public_key from a private_key
        if need, passphrase for decode private_key
        """

    @abstractmethod
    def get_hash_content(self, public_key: str) -> str:
        """Get content from a public_key which should been hash
        Generally hash algorithm use SHA3 256 or better
        """


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

    def gennerate_public_key(self, private_key_str: str, passphrase: str) -> str:
        key = ECC.import_key(private_key_str, passphrase=passphrase)
        public_key_str = key.publickey().export_key(format=KEY_EXPORT_FORMAT)
        return public_key_str

    @staticmethod
    def get_pem_content(pem_str) -> str:
        """Get PEM file content without start and end
        to avoid Collision attack
        """
        return "\n".join(pem_str.split("\n")[1:-1])

    def get_hash_content(self, public_key: str) -> str:
        return self.get_pem_content(public_key)


KEY_ENCRYPT_MAP = dict((key.name, key()) for key in KeyEncrypt.__subclasses__())
