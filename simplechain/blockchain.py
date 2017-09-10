from hashlib import sha256
import time
from .block import Block


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
