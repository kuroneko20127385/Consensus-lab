import random

class Network:
    def __init__(self, nodes, drop_rate=0.0, seed=None):
        self.nodes = nodes
        self.drop_rate = drop_rate
        self.rng = random.Random(seed)

    def broadcast_block(self, sender, block):
        for node in self.nodes:
            if node.node_id != sender.node_id:   
                if self.rng.random() >= self.drop_rate:  
                    node.chain.add_block(block)
