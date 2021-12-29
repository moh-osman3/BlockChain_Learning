from hashlib import sha256

# each block will have a capacity of 100 transactions
BLOCK_CAPACITY = 100
idx = set()


class Block:
    def __init__(self, block_id):
        self.block_id = block_id
        self.block_hash = None
        self.prev_hash = None
        self.transactions = []
        self.next_block = None
        self.is_full = False

    def ComputeHash():
        # when transaction is added, update the block_hash
        string_to_hash = "".join(self.transactions)
        self.block_hash = sha256(string_to_hash.encode('utf-8')).hexdigest()

        if self.next_block:
            self.next_block.prev_hash = self.block_hash
        
    def AddTransaction(self, source, target, amt):
        self.transactions.append("".join([source,target,amt]))

        if len(self.transactions) >= BLOCK_CAPACITY:
            self.is_full = True




Class BlockChain:
    def __init__(self, genesis_block):
        self.genesis_block = genesis_block
        self.node_store = {}





