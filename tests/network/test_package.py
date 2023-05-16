import pytest
from ucn.proto import package_pb2
from ucn.network import package


def test_generate_checksum():
    """Test generating a CRC32 checksum."""
    data = b"test data"
    checksum = package.generate_checksum(data)

    # The checksum should be a 4-byte integer.
    assert isinstance(checksum, int)
    assert 0 <= checksum < 2**32


@pytest.mark.parametrize(
    "source, protocol, data",
    [
        ("test source", "test protocol", b"test data"),
        ("", "test protocol", b"test data"),
        ("test source", "", b"test data"),
        ("test source", "test protocol", b""),
    ],
)
def test_generate_package(source, protocol, data):
    """Test generating a package with various inputs."""

    result = package.generate_package(source, protocol, data)

    # The result should be a bytes object.
    assert isinstance(result, bytes)

    # The result should include the source and protocol.
    assert source.encode() in result
    assert protocol.encode() in result

    # Create a header to calculate its length
    header = package_pb2.TransferHeader()
    header.source = source
    header.protocol = protocol
    header.length = len(data)
    header.checksum = package.generate_checksum(data)
    header_bytes = header.SerializeToString()
    header_length = len(header_bytes)

    # The length of result should be equal to the length of header length indicator (2 bytes),
    # plus the length of header, plus the length of data.
    assert len(result) == 2 + header_length + len(data)


def test_unpack_package():
    """Test unpacking a package."""
    source = "test source"
    protocol = "test protocol"
    data = b"test data"

    # First, generate a package.
    package_bytes = package.generate_package(source, protocol, data)

    # Then, unpack the package.
    header, unpacked_data = package.unpack_package(package_bytes)

    # The header should be a TransferHeader object.
    assert isinstance(header, package_pb2.TransferHeader)

    # The source and protocol should match the original values.
    assert header.source == source
    assert header.protocol == protocol

    # The data should match the original data.
    assert unpacked_data == data


def test_unpack_package_with_empty_data():
    """Test unpacking a package with empty data."""
    source = "test source"
    protocol = "test protocol"
    data = b""

    # First, generate a package.
    package_bytes = package.generate_package(source, protocol, data)

    # Then, unpack the package.
    header, unpacked_data = package.unpack_package(package_bytes)

    # The header should be a TransferHeader object.
    assert isinstance(header, package_pb2.TransferHeader)

    # The source and protocol should match the original values.
    assert header.source == source
    assert header.protocol == protocol

    # The data should match the original data.
    assert unpacked_data == data


def test_unpack_package_with_invalid_input():
    """Test unpacking a package with invalid input."""
    with pytest.raises(Exception):
        package.unpack_package(b"invalid input")
