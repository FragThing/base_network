import threading
from time import sleep

import pytest
from ucn.network.proxy.ipfs import IPFSNetwork

# Replace <API_URL> with the actual IPFS API URL
API_URL = "http://127.0.0.1:5001"


@pytest.fixture
def ipfs_network():
    return IPFSNetwork(API_URL)


def test_send_and_receive(ipfs_network):
    # Test data to send
    test_data = b"Hello, IPFS!"

    # Network type
    net_type = "test-net"

    # Define a function to receive data in a separate thread
    def recv_data():
        for data in ipfs_network.recv(net_type, 5.0):
            assert data == test_data
            break

    # Start the receiver thread
    recv_thread = threading.Thread(target=recv_data)
    recv_thread.start()

    # Give the receiver some time to start
    sleep(1)

    # Send the test data
    result = ipfs_network.send(test_data, net_type, 5.0)
    assert result

    # Wait until the receiver finishes
    recv_thread.join()


def test_send_with_invalid_timeout(ipfs_network):
    # Test data to send
    test_data = b"Hello, IPFS!"

    # Network type
    net_type = "test-net"

    # Test sending with an invalid (negative) timeout
    with pytest.raises(ValueError):
        ipfs_network.send(test_data, net_type, -1.0)


def test_receive_with_invalid_timeout(ipfs_network):
    # Network type
    net_type = "test-net"

    # Test receiving with an invalid (negative) timeout
    with pytest.raises(ValueError):
        next(ipfs_network.recv(net_type, -1.0))


def test_send_and_receive_empty_data(ipfs_network):
    # Test data to send
    test_data = b""

    # Network type
    net_type = "test-net-empty"

    # Define a function to receive data in a separate thread
    def recv_data():
        for data in ipfs_network.recv(net_type, 5.0):
            assert data == test_data
            break

    # Start the receiver thread
    recv_thread = threading.Thread(target=recv_data)
    recv_thread.start()

    # Give the receiver some time to start
    sleep(1)

    # Send the test data
    result = ipfs_network.send(test_data, net_type, 5.0)
    assert result

    # Wait until the receiver finishes
    recv_thread.join()
