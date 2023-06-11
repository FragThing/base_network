from dataclasses import dataclass


@dataclass
class BasicBlock:
    protocol: str
    previous_block_hash: str
    data: bytes

    def serialize(self) -> bytes:
        return (
            b"%b/n" % self.protocol.encode("utf8")
            + b"%b/n" % self.previous_block_hash.encode("utf8")
            + b"%b" % self.data
        )

    @staticmethod
    def deserialize(data: bytes) -> "BasicBlock":
        protocol_bytes, previous_block_hash_bytes, data_bytes = data.split(b"\n", 2)

        protocol = protocol_bytes.decode("utf8")
        previous_block_hash = previous_block_hash_bytes.decode("utf8")

        return BasicBlock(
            protocol=protocol,
            previous_block_hash=previous_block_hash,
            data=data_bytes,
        )
