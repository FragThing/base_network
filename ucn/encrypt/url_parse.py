"""URL parse and generate for key"""

from hashlib import shake_256
from base64 import b85encode, b85decode
from ucn.encrypt.key import Key, KeyStore


class URLParse:
    """Keys URL Parse or Generate"""

    ENCODE_MAP = {
        "SHAKE256": lambda d: shake_256(d).hexdigest(64),
        "Base85": lambda d: b85encode(d).decode("utf-8"),
    }

    DECODE_MAP = {
        "Base85": lambda d: b85decode(d).decode("utf-8"),
    }

    def encode(self, encode_algo: str, data: bytes) -> str:
        """Encode or Hash key_id content"""
        encoder = self.ENCODE_MAP[encode_algo]
        return encoder(data)

    def decode(self, encode_algo: str, content: str) -> bytes or None:
        """Decode key_id content
        If it is encode by base or other but NOT HASH
        """
        try:
            return self.DECODE_MAP[encode_algo](content)
        except KeyError:
            return None

    def decodable(self, encode_algo: str) -> bool:
        """Check encode algorithm is decodable"""
        return encode_algo in self.DECODE_MAP

    def generate(self, encode_algo, key_list: list[Key]) -> str:
        """Generate URL by encode algorithm and keys"""
        scheme = f"{encode_algo}"
        content = ""
        decodable = self.decodable(encode_algo)
        for key in key_list:
            key_content = key.keystore.public_key
            scheme += f"+{key.keystore.encryt_algo}"
            if decodable:
                scheme += f":{len(key_content)}"
            content += key_content
        return f"{scheme}://{self.encode(encode_algo, content)}"

    def parse(self, url: str) -> [str, list[str or Key]]:
        """Parse URL to encode algorithm and keys"""
        scheme, encode_content = url.split("://", maxsplit=1)
        encode_algo, *key_algo_list = scheme.split("+")
        content = self.decode(encode_algo, encode_content)
        if not self.decodable(encode_algo) or content.strip():
            return encode_algo, str
        key_list = []
        for key_algo_str in key_algo_list:
            key_algo_split = key_algo_str.rsplit(".", maxsplit=1)
            key_algo, key_len = key_algo_split
            key = Key(KeyStore(encryt_algo=key_algo, public_key=content[:key_len]))
            content = content[key_len:]
            key_list.append(key)
        return scheme, key_list


url_parse = URLParse()
