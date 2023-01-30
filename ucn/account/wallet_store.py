"""Account store"""
from dataclasses import dataclass
from ucn.encrypt.key import KeyStore


@dataclass
class AccountStore:
    """Account store to export/import as json"""

    encode_algo: str
    key_store_list: list[KeyStore]

    @staticmethod
    def load(json_data: dict[str, str]):
        """Load account data from (json)dict"""
        return AccountStore(
            encode_algo=json_data["encode_algo"],
            key_store_list=[
                KeyStore.load(key_data) for key_data in json_data["key_list"]
            ],
        )

    def dump(self) -> dict[str, str]:
        """Export account as json"""
        return {
            "encode_algo": self.encode_algo,
            "key_list": [key.dump() for key in self.key_store_list],
        }
