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
from network_protocol import SimplechainProtocol


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
    node_array = []
    coro = loop.create_server(
        SimplechainProtocol(blockchain, nodes),
        '127.0.0.1'
    )
    # Create the server
    server = loop.run_until_complete(coro)
    clients = {}

    # Create client coroutines for each passed node
    if nodes:
        for node in nodes:
            clients[node] = loop.create_connection(
                SimplechainProtocol(blockchain, nodes),
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
