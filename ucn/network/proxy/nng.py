"""Nanomsg Network send and receive base pubsub
"""

from typing import Iterator, List

from pynng import Pub0, Sub0
from pynng.exceptions import Timeout

from .basic_network_model import BasicNetworkModel


class NNGNetwork(BasicNetworkModel):
    def __init__(self, address: str, target_address_list: List[str]):
        self.address = address
        self.target_address_list = target_address_list

    def __enter__(self):
        self.service = self._init_service(self.address)
        self.sub_service_list = self._reflash_sub_service(self.target_address_list)
        super().__init__(timeout=0.5)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @staticmethod
    def _init_service(address) -> Pub0:
        service = Pub0()
        service.listen(address)
        return service

    @staticmethod
    def _reflash_sub_service(target_address_list: List[str]) -> List[Sub0]:
        sub_service_list = []
        for address in target_address_list:
            sub_service = Sub0()
            sub_service_list.append(sub_service)
        return sub_service_list

    def send(self, data: bytes, net_type: str, timeout: float) -> bool:
        self.service.send_timeout = timeout * 1000
        topic = net_type.encode("utf-8")
        self.service.send(topic + data)
        return True

    def _recv(self, net_type: str, timeout: float) -> Iterator[bytes]:
        topic = net_type.encode("utf-8")
        header_len = len(topic)
        for sub_service in self.sub_service_list:
            try:
                sub_service.recv_timeout = timeout * 1000
                sub_service.subscribe(net_type.encode("utf-8"))
                yield sub_service.recv()[header_len:]
            except Timeout:
                raise StopIteration

    def close(self):
        self.service.close()
        for sub_service in self.sub_service_list:
            sub_service.close()
