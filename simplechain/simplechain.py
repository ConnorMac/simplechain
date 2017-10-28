"""
Ultra simple blockchain implementation in python. For learning purposes.
No-proof block addition.
No blockchain persitance.
"""

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
        # TODO: Parse recieved data
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        self.log(
            message='Connection lost to: ' + str(self.transport.get_extra_info('peername'))
        )

    def log(self, message):
        """
        Logging function
        """
        print(message)


def main(argv):
    nodes = []
    opts, args = getopt.getopt(
        argv, "hn:"
    )
    for opt, arg in opts:
        if opt == '-h':
            print('simplechain.py -n <NODE_IP:NODE_PORT,NODE2_IP:NODE2_PORT>')
            sys.exit()
        elif opt in ("-n"):
            nodes_string = arg
            nodes = nodes_string.split(',')
    # Initiate a new blockchain object
    blockchain = Blockchain()

    loop = asyncio.get_event_loop()
    # Each client connection will create a new protocol instance
    coro = loop.create_server(
        SimplechainProtocol(nodes, blockchain),
        '127.0.0.1'
    )
    # Create the server
    server = loop.run_until_complete(coro)
    clients = {}

    # Create client coroutines for each passed node
    if nodes:
        for node in nodes:
            print(node.split(':')[1])
            clients[node] = loop.create_connection(
                SimplechainProtocol(nodes, blockchain),
                str(node.split(':')[0]), int(node.split(':')[1])
            )
            loop.run_until_complete(clients[node])

    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == "__main__":
    main(sys.argv[1:])
