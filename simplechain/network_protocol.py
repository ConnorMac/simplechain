import sys
import getopt
import asyncio
import json
from blockchain import Blockchain
from block import Block


class SimplechainProtocol(asyncio.Protocol):
    """
    Protocol for Simplechain node communication
    """

    def __init__(self, nodes, blockchain):
        self.nodes = nodes
        self.blockchain = blockchain
        self.transport = None
        self.stream_data = {}

    def __call__(self):
        return self

    def connection_made(self, transport: asyncio.Transport):
        self.transport = transport
        self.log(
            message=str(self.transport.get_extra_info('peername')) + ' connected to node.'
        )
        response_dict = {
            "blockchain": self.blockchain.to_raw_array()
        }
        response_dict['nodes'] = self.nodes
        response_json_bytes = str.encode(json.dumps(response_dict))
        # Dumps blockchain json byte data
        self.transport.write(response_json_bytes)

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))
        data_dict = json.loads(data.decode())
        self.blockchain.calculate_and_update_main_chain(
            data_dict.get('blockchain', [])
        )
        self.nodes = self.nodes + data_dict.get('nodes', [])

    def connection_lost(self, exc):
        self.log(
            message='Connection lost to: ' + str(self.transport.get_extra_info('peername'))
        )

    def log(self, message):
        """
        Logging function
        """
        print(message)
