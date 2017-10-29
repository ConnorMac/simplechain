import sys
import getopt
import asyncio
import json
from hashlib import sha256
from enum import Enum
from ast import literal_eval as make_tuple
from blockchain import Blockchain
from block import Block


class NetworkFunctions(Enum):
    CREATE_AND_ADD_BLOCK = 'create_and_add_block'
    CHAIN_DUMP = 'chain_dump'


class SimplechainProtocol(asyncio.Protocol):
    """
    Protocol for Simplechain node communication
    """

    def __init__(self, blockchain, nodes=[]):
        self.nodes = {}
        self._update_nodes(nodes)
        self.clients = {}
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
        peer_ip = self.transport.get_extra_info('peername')[0]
        peer_port = self.transport.get_extra_info('peername')[1]
        self._update_nodes([peer_ip + ':' + str(peer_port)])
        self.clients[peer_ip + ':' + str(peer_port)] = self.transport
        # Dumps blockchain json byte data
        self.transport.write(self.create_chain_dump_data())

    def data_received(self, data):
        self.log('Data received: {!r}'.format(data.decode()))
        try:
            data_dict = json.loads(data.decode())

            # Read in the function key to figure out what to do next
            function = data_dict.get('function', '')
            if function == NetworkFunctions.CREATE_AND_ADD_BLOCK.value:
                self.log('Creating new block')
                data = data_dict.get('block_data', '')
                self.blockchain.create_and_append_block(
                    data=data
                )
                self.broadcast_data_to_nodes(
                    data=self.create_chain_dump_data()
                )
            elif function == NetworkFunctions.CHAIN_DUMP.value:
                self.consume_chain_dump_data(data_dict)
        except json.decoder.JSONDecodeError as e:
            self.log('Recieved data is not valid json')

    def connection_lost(self, exc):
        self.log(
            message='Connection lost to: ' + str(
                self.transport.get_extra_info('peername')
            )
        )

    def log(self, message):
        """
        Logging function
        """
        print(message)

    def _update_nodes(self, nodes):
        # Todo:  create proper routing table
        if nodes:
            for node in nodes:
                self.nodes[str(node)] = node

    def get_node_array(self):
        node_array = []
        if self.nodes:
            for node in self.nodes:
                node_array.append(self.nodes.get(node))
        return node_array

    def broadcast_data_to_nodes(self, data):
        print('Broadcasting data to all peers')
        for client in self.clients:
            transport = self.clients.get(client)
            self.log('Broadcasting new chain to:' + client)
            transport.write(self.create_chain_dump_data())

    def create_chain_dump_data(self):
        response_dict = {
            "function": "chain_dump",
            "blockchain": self.blockchain.to_raw_array()
        }
        response_dict['nodes'] = self.get_node_array()
        return str.encode(json.dumps(response_dict))

    def consume_chain_dump_data(self, data):
        self.blockchain.calculate_and_update_main_chain(
            data.get('blockchain', [])
        )
        # self._update_nodes(data.get('nodes', []))
