""" IPFS Network send and receive by pubsub
"""
from json import loads
from typing import Iterator
from urllib.parse import urljoin

import requests
from multiformats.multibase import decode, encode

from .basic_network_model import BasicNetworkModel


class IPFSNetwork(BasicNetworkModel):
    def __init__(self, api_url: str):
        self.api_url = api_url

    def send(self, data: bytes, net_type: str, timeout: float) -> bool:
        """Send string data to topic"""
        topic = net_type.encode("utf-8")
        topic_encode: str = encode(topic, "base64url")
        url = urljoin(self.api_url, f"/api/v0/pubsub/pub?arg={topic_encode}")
        files = {"file": ("d", data)}
        rsp = requests.post(url, files=files, timeout=timeout)
        return rsp.status_code == 200

    def recv(self, net_type: str, timeout: float) -> Iterator[bytes]:
        """Receive data from topic"""
        topic = net_type.encode("utf-8")
        topic_encode: str = encode(topic, "base64url")
        url = urljoin(self.api_url, f"/api/v0/pubsub/sub?arg={topic_encode}")
        with requests.post(url, stream=True, timeout=timeout) as rsp:
            cache = b""
            for chunk in rsp.iter_content(8196):
                cache += chunk
                data_list = cache.split(b"\n")
                data = data_list.pop(0)
                cache = b"".join(data_list)
                if data_list:
                    data_json = loads(data.decode("utf-8"))
                    result = {}
                    result["data"] = decode(data_json["data"])
                    result["seqno"] = decode(data_json["seqno"])
                    result["topicIDs"] = [
                        decode(b).decode("utf-8") for b in data_json["topicIDs"]
                    ]
                    yield result["data"]
