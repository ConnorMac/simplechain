from hashlib import sha256
import time
from .block import Block
import json


class Blockchain(object):
    def __init__(self, block_array=[]):
        self.block_array = block_array
        if not self.block_array:
            # TODO: Check for nodes to sync with
            block = Block.build_genesis_block()
            self.append_block_to_chain(block)

    @property
    def latest_block(self):
        return self.block_array[-1]

    def append_block_to_chain(self, block):
        return self.block_array.append(block)

    def to_json(self):
        """
        Use for dumping the blockchain data in a consumable format
        """
        blockchain_raw_array = []
        for block in self.block_array:
            blockchain_raw_array.append(block.to_dict())

        blockchain = {
            "blockchain": blockchain_raw_array
        }
        return json.dumps(blockchain)
