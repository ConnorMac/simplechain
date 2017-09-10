from hashlib import sha256
import time


class Block(object):
    def __init__(self, index, block_hash, previous_hash, timestamp, data):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.hash = block_hash
        self.data = data

    @classmethod
    def build_new_block(cls, data, previous_block=None):
        """
        Returns a new instance of the block class
        """
        if previous_block:
            new_index = previous_block.index+1
            previous_hash = previous_block.previous_hash
        else:
            new_index = 0
            previous_hash = ''
        timestamp = int(time.time())
        block_hash = cls.build_block_hash(
            index=new_index,
            timestamp=timestamp,
            data=data,
            previous_hash=previous_hash
        )
        block = cls(
            index=new_index,
            previous_hash=previous_hash,
            data=data,
            timestamp=timestamp,
            block_hash=block_hash
        )

        return block

    def to_dict(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "hash": self.hash,
            "data": self.data
        }

    @staticmethod
    def build_block_hash(index, timestamp, data, previous_hash):
        """
        Builds the block hash
        Can be extended at a later stage to add more functionality on mine
        """
        str_to_hash = str(index) + str(timestamp) + str(data) + str(previous_hash)
        block_hash = sha256(
            bytes(str_to_hash, encoding='utf-8')
        ).hexdigest()
        return block_hash

    @classmethod
    def build_genesis_block(cls, data="Welcome to simplechain"):
        data = data
        return cls.build_new_block(data)
