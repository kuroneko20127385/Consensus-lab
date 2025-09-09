import hashlib

class Block:
    def __init__(self, height, prev_hash, txs, proposer, nonce=0):
        self.height = height          
        self.prev_hash = prev_hash    
        self.txs = txs                
        self.proposer = proposer      
        self.nonce = nonce            

    def hash(self):
        header = f"{self.height}{self.prev_hash}{self.txs}{self.proposer}{self.nonce}"
        return hashlib.sha256(header.encode()).hexdigest()

    def __repr__(self):
        return f"Block(h={self.height}, proposer={self.proposer}, hash={self.hash()[:6]})"
