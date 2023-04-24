"""Generalized URL parse and generate"""

from hashlib import shake_256
from base64 import b85encode, b85decode


class URLParse:
    """Generalized URL parse and generate"""

    ENCODE_LEN_MAP = {
        128: "Base85",
        -1: "SHAKE256",
    }

    ENCODE_MAP = {
        "SHAKE256": lambda d: shake_256(d).hexdigest(128),
        "Base85": lambda d: b85encode(d).decode("utf-8"),
    }

    DECODE_MAP = {
        "Base85": lambda d: b85decode(d),
    }

    def encode(
        self, data: bytes, encode_algo: str = None, force_hash: bool = False
    ) -> str:
        """Encode or Hash key_id content"""
        if not encode_algo:
            encode_algo = self.__get_encoder(data, force_hash)
        encoder = self.ENCODE_MAP[encode_algo]
        return f"{encode_algo}://{encoder(data)}"

    def __get_encoder(self, data: bytes, force_hash: bool):
        """Get encoder by data length"""
        length = len(data)
        for max_length, encoder in self.ENCODE_LEN_MAP.items():
            if force_hash and encoder in self.DECODE_MAP:
                continue
            if max_length == -1:
                return encoder
            if length <= max_length:
                return encoder
        return None

    def decode(self, url: str) -> bytes or None:
        """Decode key_id content
        If it is encode by base or other but NOT HASH
        """
        encode_algo, content = url.rsplit("://", maxsplit=1)
        try:
            return self.DECODE_MAP[encode_algo](content)
        except KeyError:
            return None

    def decodable_algo(self, encode_algo: str) -> bool:
        """Check key_id content is decodable
        """
        return encode_algo in self.DECODE_MAP

    @staticmethod
    def get_scheme(url: str) -> list[str]:
        """Get scheme list from URL"""
        return url.split("://", maxsplit=1)[0].split("+")

    @staticmethod
    def reset_scheme(url: str, scheme_list: list[str]) -> str:
        """Reset URL scheme"""
        scheme = "+".join(scheme_list)
        url_content = url.split("://", maxsplit=1)[1]
        return f"{scheme}://{url_content}"


url_parse = URLParse()
