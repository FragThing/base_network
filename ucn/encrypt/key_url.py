"""Key URL parse and generate"""

from ucn.utils import data_bytes_to_string, data_string_to_bytes
from ucn.url_parse import url_parse
from ucn.encrypt.key import Key, KeyStore


class KeyURLException(Exception):
    """Custom exception class for handling invalid key URLs."""

    def __init__(self, message="Invalid key URL provided."):
        super().__init__(message)


class KeyUrl:
    """Key URL parse and generate"""

    def generate(self, key_list: list[Key], encode_algo: str = None) -> str:
        """
        Generate URL by encode algorithm and keys.

        :param key_list: List of Key objects to be encoded into the URL.
        :param encode_algo: Encoding algorithm to use for the URL.
        :return: Encoded URL string.
        """
        content = ""
        for key in key_list:
            keystore = key.keystore
            content += (
                f"{keystore.encrypt_algo}\n"
                f"{data_bytes_to_string(keystore.public_key)}\n"
            )
        if encode_algo is None:
            encode_algo = "Base85"
        return url_parse.encode(content.encode("utf8")[:-1], encode_algo)

    def parse(self, url: str) -> list[Key] or None:
        """
        Wrapper function to handle exceptions during URL parsing.

        :param url: The URL string to parse.
        :return: List of Key objects or None.
        """
        try:
            return self.__parse(url)
        except Exception as error:
            raise KeyURLException(str(error)) from error

    def __parse(self, url: str) -> list[Key] or None:
        """
        Parse URL to encode algorithm and keys, possible raise Error.

        :param url: The URL string to parse.
        :return: List of Key objects or None if parsing fails.
        """
        content = url_parse.decode(url)
        if content is None:
            return None
        content_lines = content.decode("utf8").split("\n")
        key_list = []
        for i in range(0, len(content_lines), 2):
            encrypt_algo = content_lines[i]
            public_key = data_string_to_bytes(content_lines[i + 1])
            key = Key(KeyStore(encrypt_algo=encrypt_algo, public_key=public_key))
            key_list.append(key)
        return key_list


key_url = KeyUrl()
