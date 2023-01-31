"""Local data store
To save:
1. local cache
2. pure data
3. data type proxy
"""
from pathlib import Path
from ucn.config import DATA_DIR_PATH
from base64 import b85encode


class BaseLocalStore:
    """Local data store"""

    FILE_STORE = "file/store"

    base_dir = Path(DATA_DIR_PATH)

    def read(self, *path: str) -> bytes:
        """Read file"""
        file_path = self.__get_file_path(*path)
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def save(self, content: bytes, *path: str):
        """Save file"""
        file_path = self.__get_file_path(*path)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    def __get_file_path(self, *path: str):
        file_path = self.base_dir
        for single_path in path:
            file_path = file_path / self.__encode(single_path)
        return file_path

    @staticmethod
    def __encode(name) -> str:
        return b85encode(name.encode("utf-8")).decode("utf-8")


base_local_store = BaseLocalStore()
