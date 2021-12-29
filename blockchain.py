from hashlib import sha256
import sqlite3
from sqlite3 import Error

# sqlite database setup to store all users with accounts on record
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print("The error {} occurred".format(e))

    return connection

db = create_connection("/Users/mosman/blockchain/BlockChain_Learning/blockchain_db.sqlite")
cur = db.cursor()

cur.execute(
    '''
    CREATE TABLE acct (
        id INT PRIMARY KEY,
        name TEXT,
        balance INT
    )
    '''
)

cur.execute(
    '''
    INSERT INTO acct
    VALUES (0, "Person1", 10000),
           (1, "Person2", 10000),
           (2, "Person3", 10000)
    '''
)


# each block will have a capacity of 100 transactions
BLOCK_CAPACITY = 100
idx = set()

'''
-- Block --

The Block Class defines a block in a blockchain

Params:
- block_id:      a unique id for the block
- block_hash:    sha256 hash of the transactions in the block
- prev_hash:     the block_hash of the previous block
- transactions:  list of transactions ("soure|target|amount")
- next_block:    next block in the blockchain
- is_full:       whether the current block is at capacity

Methods:
- ComputeHash:             updates block_hash whenever a transaction is added
- AddTransactionToBlock:   adds a transaction to the current block
'''
class Block:
    def __init__(self, block_id):
        self.block_id = block_id
        self.block_hash = "" 
        self.prev_hash = None
        self.transactions = []
        self.next_block = None
        self.is_full = False

    def ComputeHash(self):
        # when transaction is added, update the block_hash
        string_to_hash = "".join(self.transactions)
        self.block_hash = sha256(string_to_hash.encode('utf-8')).hexdigest()

        if self.next_block:
            self.next_block.prev_hash = self.block_hash
        
    def AddTransactionToBlock(self, source, target, amt):
        # if the transaction is valid (i.e. balances check out), then append
        # TODO: this should be connected to a database with users and their
        # current balances
        self.transactions.append("|".join([source,target,amt]))
        self.ComputeHash()

        if len(self.transactions) >= BLOCK_CAPACITY:
            self.is_full = True
            self.next_block = Block(self.block_id + 1)
            self.next_block.prev_hash = self.block_hash
        
    
cur = Block(0)

tmp = cur

for i in range(200):
    tmp.AddTransactionToBlock("a", "b", "20")

    if len(tmp.transactions) == 100:
        tmp = tmp.next_block

while cur:
    print(cur.transactions)
    cur = cur.next_block





