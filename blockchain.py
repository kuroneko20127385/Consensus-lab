import hashlib
from block import Block

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.finalized = []

    def create_genesis_block(self):
        return Block(0, "0", "Genesis", -1, 0)

    def add_block(self, block, k=None):
        self.chain.append(block)
        if k is not None:
            self.finalized = finality_rule(self.chain, k)

    def get_last_block(self):
        return self.chain[-1]

    def __len__(self):
        return len(self.chain)

# Consensus mechanisms

def proof_of_work(height, prev_hash, txs, proposer, difficulty=2):
    nonce = 0
    while True:
        header = f"{height}{prev_hash}{txs}{proposer}{nonce}"
        h = hashlib.sha256(header.encode()).hexdigest()
        if h.startswith("0" * difficulty):
            return Block(height, prev_hash, txs, proposer, nonce)
        nonce += 1


def hybrid_block(height, prev_hash, txs, proposer):
    nonce = 0
    while True:
        header = f"{height}{prev_hash}{txs}{proposer}{nonce}"
        h = hashlib.sha256(header.encode()).hexdigest()
        if h.startswith("0"): 
            return Block(height, prev_hash, txs, proposer, nonce)
        nonce += 1


def elect_leader_for_height(nodes, height, rng):
    total_stake = sum(n.stake for n in nodes)
    pick = rng.randint(1, total_stake)
    acc = 0
    for node in nodes:
        acc += node.stake
        if acc >= pick:
            return node.node_id
    return nodes[-1].node_id

# Chain rule & Finality rule

def chain_rule(chains):
    return max(chains, key=len)

def finality_rule(chain, k):
    finalized = []
    for i, block in enumerate(chain):
        if i + k < len(chain):
            finalized.append(block)
    return finalized