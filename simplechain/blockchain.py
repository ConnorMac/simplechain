from hashlib import sha256
import time
from block import Block
import json


class Blockchain(object):
    def __init__(self, block_array=[]):
        self.block_array = block_array
        if not self.block_array:
            block = Block.build_genesis_block()
            self.append_block_to_chain(block)

    @property
    def latest_block(self):
        return self.block_array[-1]

    def append_block_to_chain(self, block):
        return self.block_array.append(block)

    def create_and_append_block(self, data=''):
        new_block = Block.build_new_block(
            data=data,
            previous_block=self.latest_block
        )
        self.append_block_to_chain(new_block)
        return new_block

    def to_raw_array(self):
        blockchain_raw_array = []
        for block in self.block_array:
            blockchain_raw_array.append(block.to_dict())
        return blockchain_raw_array

    def to_json(self):
        """
        Use for dumping the blockchain data in a consumable format
        """
        blockchain_raw_array = self.to_raw_array()
        return json.dumps(blockchain_raw_array)

    @classmethod
    def from_json(cls, blockchain_json):
        return cls(
            block_array=blockchain_json.get('blockchain', [])
        )

    def _array_to_block_array(self, raw_block_array):
        block_array = []
        for block in raw_block_array:
            new_block = Block.build_from_json(block)
            block_array.append(new_block)
        return block_array

    def _overwrite_blockchain_with_external(self, block_array):
        print('Overwriting current chain.')
        self.block_array = block_array

    def calculate_and_update_main_chain(self, external_chain):
        # Should be replaced by some proper consensus
        if len(external_chain) > len(self.block_array):
            block_array = self._array_to_block_array(
                external_chain
            )
            self._overwrite_blockchain_with_external(block_array)
        elif len(external_chain) == len(self.block_array):
            genesis_block_current = self.block_array[0]
            genesis_block_external = external_chain[0]
            if genesis_block_external.get('timestamp') < genesis_block_current.timestamp:
                block_array = self._array_to_block_array(
                    external_chain
                )
                self._overwrite_blockchain_with_external(block_array)
