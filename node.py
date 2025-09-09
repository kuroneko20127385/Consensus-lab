from blockchain import proof_of_work, hybrid_block, elect_leader_for_height

class Node:
    def __init__(self, node_id, stake=1, byzantine=False):
        self.node_id = node_id
        self.stake = stake
        self.chain = None
        self.byzantine = byzantine

    def attach_chain(self, blockchain):
        self.chain = blockchain

    def mine_block_pow(self, txs):
        prev = self.chain.get_last_block()
        return proof_of_work(prev.height + 1, prev.hash(), txs, self.node_id)

    def mine_block_hybrid(self, txs):
        prev = self.chain.get_last_block()
        return hybrid_block(prev.height + 1, prev.hash(), txs, self.node_id)

    def propose_block_pos(self, txs, nodes, rng):
        prev = self.chain.get_last_block()
        leader = elect_leader_for_height(nodes, prev.height + 1, rng)
        if leader == self.node_id:
            return hybrid_block(prev.height + 1, prev.hash(), txs, self.node_id)
        return None
