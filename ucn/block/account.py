from time import time
from ucn.proto.account_pb2 import AccountBlock, PublicKey, AdditionalBlock
from ucn.account.wallet import Account
from .store.local_store import local_block_store

ACCOUNT_PROTOCOL = "account"
ACCOUNT_ADDON_PROTOCOL = "account_addon"


def add_account(account: Account) -> str:
    protobuf_account = AccountBlock(
        creation_time=int(time()),
        encode_algo=account.encode_algo,
        public_keys=[
            PublicKey(
                algorithm=key.keystore.encrypt_algo,
                key=key.keystore.public_key,
            )
            for key in account.key.key_list
        ],
    )
    return local_block_store.add_block(
        protocol=ACCOUNT_PROTOCOL, data=protobuf_account.SerializeToString()
    )


def add_account_addon(account: Account, addon_map: map[str, bytes]) -> list[str]:
    hash_list = []
    for key, value in addon_map.items():
        protobuf_account_addon = AdditionalBlock(
            account_url=account.id_url,
            protocal=key,
            data=value,
        )
        hash_list.append(
            local_block_store.add_block(
                protocol=ACCOUNT_ADDON_PROTOCOL,
                data=protobuf_account_addon.SerializeToString(),
            )
        )
    return hash_list
