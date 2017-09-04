"""
Ultra simple blockchain implementation in python. For learning purposes.
No-proof block addition.
No blockchain persitance.
"""

from hashlib import sha256
import time


class BlockChain(object):
    def __init__(block_array=None):
        self.block_array = block_array

    @property
    def latest_block(self):
        return self.block_array[-1]

    def append_block_to_chain(self, block):
        return self.block_array.append(block)


class Block(object):
    def __init__(index, hash, previous_hash, timestamp, data):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.hash = block_hash
        self.data = data

    @classmethod
    def build_new_block(cls, previous_block, data):
        """
        Returns a new instance of the block class
        """
        new_index = previous_block.index+1
        timestamp = int(time.time())
        str_to_hash = str(new_index) + str(timestamp) + str(data) + str(previous_block.previous_hash)
        block_hash = sha256(
            bytes(str_to_hash, encoding='utf-8')
        )
        block = cls(
            index=new_index,
            previous_hash=previous_block.previous_hash,
            data=data,
            timestamp=timestamp,
            hash=block_hash
        )

        return block
