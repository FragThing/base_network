""" IPFS Network send and receive by pubsub
"""
from urllib.parse import urljoin
from json import loads
from multibase import decode, encode

import requests


def send(data, topic: str, api_url: str):
    """Send string data to topic
    """
    topic_encode: bytes = encode('base64url', topic)
    data_encode: bytes = encode('base64url', data)
    url = urljoin(api_url, f'/api/v0/pubsub/pub?arg={topic_encode.decode()}')
    files = {'file': ('d', data_encode)}
    rsp = requests.post(url, files=files)
    print(rsp.txt)
    return rsp.status_code == 200


def recv(topic: str, api_url: str):
    """Receive data from topic
    """
    topic_encode: bytes = encode('base64url', topic)
    url = urljoin(api_url, f'/api/v0/pubsub/sub?arg={topic_encode.decode()}')
    with requests.post(url, stream=True) as rsp:
        cache = b''
        for chunk in rsp.iter_content(8196):
            cache += chunk
            data_list = cache.split(b'\n')
            data = data_list.pop(0)
            cache = b''.join(data_list)
            if data_list:
                data_json = loads(data.decode())
                data_json['data'] = decode(data_json['data']).decode('utf-8')
                data_json['seqno'] = decode(data_json['seqno'])
                data_json['topicIDs'] = [
                    decode(b).decode('utf-8') for b in data_json['topicIDs']
                ]
                yield data_json
