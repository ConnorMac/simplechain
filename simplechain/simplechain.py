"""
Ultra simple blockchain implementation in python. For learning purposes.
No-proof block addition.
No blockchain persitance.
"""

import sys
import getopt
import asyncio
from blockchain import Blockchain
from block import Block


class SimplechainProtocol(asyncio.Protocol):
    """
    Protocol for Simplechain node communication
    """

    def __init__(self, nodes):
        # TODO: Look for nodes it can load the blockchain from
        self.blockchain = Blockchain()
        self.transport = None
        self.stream_data = {}
        self.nodes = nodes

    def connection_made(self, transport: asyncio.Transport):
        self.transport = transport
        self.log(
            message=str(self.transport.get_extra_info('peername')) + ' connected to node.'
        )
        blockchain_bytes = str.encode(self.blockchain.to_json())
        # Dumps blockchain json byte data
        self.transport.write(blockchain_bytes)

    def data_received(self, data):
        # TODO: Parse recieved data
        print('Data received: {!r}'.format(data.decode()))

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
            nodes = arg

    loop = asyncio.get_event_loop()
    # Each client connection will create a new protocol instance
    coro = loop.create_server(SimplechainProtocol(nodes), '127.0.0.1')
    server = loop.run_until_complete(coro)

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
