"""
Ultra simple blockchain implementation in python. For learning purposes.
No-proof block addition.
No blockchain persitance.
"""

import asyncio
from .blockchain import Blockchain
from .block import Block


class SimplechainProtocol(asyncio.Protocol):
    """
    Protocol for Simplechain node communication
    """

    def __init__(self):
        # TODO: Look for nodes it can load the blockchain from
        self.blockchain = Blockchain()
        self.transport = None
        self.stream_data = {}

    def connection_made(self, transport: asyncio.Transport):
        self.transport = transport
        self.log(
            message=str(self.transport.get_extra_info('peername')) + ' connected to node.'
        )
        blockchain_bytes = str.encode(self.blockchain.to_json())
        # Dumps blockchain json byte data
        self.transport.write(blockchain_bytes)

    def log(self, message):
        """
        Logging function
        """
        print(message)

loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance
coro = loop.create_server(SimplechainProtocol, '127.0.0.1', 7934)
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
