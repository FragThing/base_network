"""Key URL parse and generate"""

from ucn.url_parse import url_parse
from ucn.encrypt.key import Key, KeyStore


class KeyUrl:
    """Key URL parse and generate"""

    @staticmethod
    def generate(key_list: list[Key], encode_algo: str = None) -> str:
        """Generate URL by encode algorithm and keys"""
        content = b""
        for key in key_list:
            keystore = key.keystore
            content += b"%c\n" % keystore.encryt_algo
            content += b"%b\n" % keystore.public_key
        return url_parse.encode(content[:-1], encode_algo)

    @staticmethod
    def parse(url: str) -> list[Key] or None:
        """Parse URL to encode algorithm and keys"""
        content = url_parse.decode(url)
        content_lines = content.split("\n")
        if not content_lines:
            return None
        key_list = []
        for i in range(0, len(content_lines), 2):
            encryt_algo, public_key = content_lines[i], content_lines[i + 1]
            key = Key(KeyStore(encryt_algo=encryt_algo, public_key=public_key))
            key_list.append(key)
        return key_list


key_url = KeyUrl()
