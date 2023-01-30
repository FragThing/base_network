"""Count online account"""

from dataclasses import dataclass, asdict
from hashlib import shake_256
from ucn.utils import json_dumps, get_timestamp


@dataclass
class Online:
    """Count online single data"""

    account: str
    timestamp: int
    previous_hash: str
    signature: bytes

    @property
    def hash(self) -> bytes:
        """Get hash of itself"""
        json = json_dumps(asdict(self))
        return shake_256(json).hexdigest(16)


@dataclass
class OnlineList:
    """Count online list"""

    online_list: set[Online]

    def add_account(self, account) -> bool:
        """Push account to online list"""
        previous_hash = self.online_list[0].hash
        if account not in [online.account for online in self.online_list]:
            online = Online(account, get_timestamp(), previous_hash, None)
            self.online_list.append(online)
            return True
        return False

    def try_get_online_num(self, limit_time):
