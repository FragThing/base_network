from zlib import crc32
from ucn.proto import package_pb2


def generate_checksum(data: bytes) -> int:
    """Generates a CRC32 checksum from the given data."""
    return crc32(data)


def generate_package(source: str, protocol: str, data: bytes) -> bytes:
    """Generates a package from the given source, protocol, and data."""

    # Create the header
    header = package_pb2.TransferHeader()
    header.source = source
    header.protocol = protocol
    header.length = len(data)
    header.checksum = generate_checksum(data)

    # Serialize the header to bytes
    header_bytes = header.SerializeToString()

    # Get the length of the header
    header_length = len(header_bytes)

    # Combine the header length, header and data to create the package
    package = header_length.to_bytes(2, "big") + header_bytes + data

    return package


def unpack_package(package: bytes):
    """Unpack a package into its header and data."""

    # Get the header length
    header_length = int.from_bytes(package[:2], "big")

    # Get the header
    header_bytes = package[2: 2 + header_length]
    header = package_pb2.TransferHeader()
    header.ParseFromString(header_bytes)

    # Get the data
    data = package[2 + header_length:]

    return header, data
