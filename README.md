# simplechain
A simple blockchain implementation in python.

A work in progress meant to be for learning purposes.

# How to use

Create initial node: `python simplechain/simplechain.py`

Add additional nodes: `python simplechain/simplechain.py -n NODE_IP:NODE_PORT,NODE2_IP:NODE2_PORT`

Create a new block: `echo '{"function":"create_and_add_block","block_data":"hello this is some new block data"}' | nc NODE_IP NODE_PORT`
