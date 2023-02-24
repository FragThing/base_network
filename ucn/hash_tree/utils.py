"""Hash tree utils"""
from ucn.hash_tree.node import HashNode


def _make_node_list(
    hight, base_node_list: list[HashNode]
) -> list[HashNode]:
    """Make hash tree single hight node"""
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
        return node_list
    return base_node_list


def _make_tree(node_list: list[HashNode]) -> dict[int, list[HashNode]]:
    """Make hash tree root"""
    hight = 0
    node_hight_map = {}
    while True:
        node_hight_map[hight] = node_list
        if len(node_list) == 1:
            return node_hight_map
        hight += 1
        node_list = _make_node_list(hight, node_list)


def make_tree(data_list: list[bytes]) -> dict[int, list[HashNode]]:
    """Make a hash ture which make sure data is sorted"""
    data_list.sort()
    base_node_list = [HashNode(0, HashNode.hash(data)) for data in data_list]
    return _make_tree(base_node_list)
