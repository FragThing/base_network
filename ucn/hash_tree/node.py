"""A hash link tree"""
from __future__ import annotations
from dataclasses import dataclass

from hashlib import shake_256


@dataclass
class HashNode:
    """Tree node"""

    hash_str: str = None
    hight: int = None
    l_node: str = None
    r_node: str = None

    def encode(self) -> dict:
        """Encode to dict"""
        return {
            self.hash_str: {
                "h": self.hight,
                "l": self.l_node,
                "r": self.r_node,
            }
        }

    @staticmethod
    def decode(data: dict) -> HashNode:
        """Decode from dict"""
        node = HashNode()
        node.hash_str = data.keys()[0]
        value = data.values()[0]
        node.hight = value["h"]
        node.l_node = value["l"]
        node.r_node = value["r"]

    @staticmethod
    def hash(data: bytes) -> str:
        """Hash function"""
        shake_256(data).hexdigest(16)

    @staticmethod
    def init_node(hight: int, l_node: str, r_node: str) -> HashNode:
        """Push child node"""
        node = HashNode()
        node.hight = hight
        node.l_node = l_node
        node.r_node = r_node
        node.hash_str = node._hash_node(l_node, r_node)

    def _hash_node(self, l_node: str, r_node: str) -> str:
        data = str(self.hight)
        if l_node:
            data += f"{l_node}"
        if r_node:
            data += r_node
        return self.hash(data.encode("utf-8"))

    def verify(self) -> bool:
        """Verify tree hash"""
        return self._hash_node(self.l_node, self.l_node) == self.hash_str


def _make_node_list(
    hight, base_node_list: list[HashNode]
) -> tuple[int, list[HashNode]]:
    """Make hash tree single hight node"""
    hight += 1
    if len(base_node_list) > 1:
        node_list = []
        while base_node_list:
            l_node, *base_node_list = base_node_list
            l_node_str = l_node.hash_str
            if base_node_list:
                r_node, *base_node_list = base_node_list
                r_node_str = r_node.hash_str
            else:
                r_node = None
                r_node_str = None
            node_list.append(HashNode.init_node(hight, l_node_str, r_node_str))
        return hight, node_list
    return base_node_list


def make_root_node(node_list: list[HashNode]) -> tuple[str, dict[int, list[HashNode]]]:
    """Make hash tree root"""
    hight = 0
    node_hight_map = {}
    while True:
        node_hight_map[hight] = node_list
        if len(node_list) == 1:
            return node_list[0].hash_str, node_hight_map
        hight, node_list = _make_node_list(hight, node_list)


def make_tree(data_list: list[bytes]) -> HashNode:
    """Make a hash ture which make sure data is sorted"""
    data_list.sort()
    base_node_list = [HashNode(0, HashNode.hash(data)) for data in data_list]
    return make_root_node(base_node_list)
