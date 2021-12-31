from hashlib import sha256
import sqlite3
from sqlite3 import Error
import uuid

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
- nonce:         string when hashed with block_hash should start with 3 zeros
                 for the purpose of proof of work

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
        self.nonce = None

    def ComputeHash(self):
        # when transaction is added, update the block_hash
        string_to_hash = "".join(self.transactions)
        self.block_hash = sha256(string_to_hash.encode('utf-8')).hexdigest()

        if self.next_block:
            self.next_block.prev_hash = self.block_hash
    
    # keep generating until starting 3 character of hash are zero
    def GenerateNonce(self):
        nonce_attempt = None 
        nonce_hash = '111'
        while nonce_hash[:3] != '000':
            nonce_attempt = uuid.uuid4().hex
            nonce_hash = sha256((self.block_hash + nonce_attempt)).hexdigest()
        
        self.nonce = nonce_attempt
        

    def AddTransactionToBlock(self, source, target, amt):
        # if the transaction is valid (i.e. balances check out), then append
        # TODO: this should be connected to a database with users and their
        # current balances
        self.transactions.append("|".join([source,target,amt]))
        self.ComputeHash()

        cur.execute("SELECT balance FROM acct WHERE name='{}'".format(source))
        source_bal = cur.fetchone()[0]
        cur.execute("SELECT balance FROM acct WHERE name='{}'".format(target))
        target_bal = cur.fetchone()[0]
        cur.execute(
            '''
            UPDATE acct
            SET balance={}
            WHERE name='{}'
            '''.format(source_bal-int(amt), source)
        )

        cur.execute(
            '''
            UPDATE acct
            SET balance={}
            WHERE name='{}';
            '''.format(target_bal+int(amt), target)
        )

        if len(self.transactions) >= BLOCK_CAPACITY:
            self.next_block = Block(self.block_id + 1)
            self.next_block.prev_hash = self.block_hash
            self.GenerateNonce()
        

'''
-- BlockChain --

The BlockChain Class defines a blockchain

Params:
- head:   the first block in the blockchain, stored for printing purposes
- tail:   the most recently added block to the blockchain 

Methods:
- VerifyBlock:      verifies the proof of work before adding block to blockchain 
- AddBlock:         adds block to blockchain
- PrintBlockChain   prints all transactions from all blocks 
'''
class BlockChain:
    def __init__(self):
        self.head = None
        self.tail = None

    def VerifyBlock(self, block):
        if not block.nonce or not block.block_hash:
            return False

        hash_val = sha256(block.block_hash + block.nonce).hexdigest()
        # confirm first three characters are 0
        if hash_val[:3] != '000':
            return False
        
        return True

    def AddBlock(self, block):
        if not self.VerifyBlock(block):
            return

        # if self.head is None then this is the first block
        if not self.head:
            self.head = block
            self.tail = block
            return

        block.prev_hash = self.tail.block_hash
        self.tail.next_block = block
        self.tail = block

    def PrintBlockChain(self):
        tmp = self.head
        while tmp:
            print(tmp.transactions)
            tmp = tmp.next_block

        
# Testing 
blockchain = BlockChain()

idy = 0
current = Block(idy)
for i in range(200):
    current.AddTransactionToBlock("Person1", "Person2", "20")

    if len(current.transactions) == BLOCK_CAPACITY:
        blockchain.AddBlock(current)
        idy += 1
        current = Block(idy)
        
for row in cur.execute("SELECT * FROM acct"):
    print(row)

blockchain.PrintBlockChain()




