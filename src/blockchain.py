import hashlib
import json
import time

########################################
# Helper Functions
########################################

def sha256(data: str) -> str:
    """Returns the SHA-256 hash of the given string."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def serialize(obj) -> str:
    """Serializes a Python object into JSON with sorted keys."""
    return json.dumps(obj, sort_keys=True)

def valid_proof(hash_value: str, difficulty: int) -> bool:
    """Check if hash_value meets difficulty (i.e. has required number of leading zeros)."""
    return hash_value.startswith('0' * difficulty)

def compute_merkle(transactions: list) -> str:
    """Computes the Merkle root of a list of transactions (using their tx_ids)."""
    if not transactions:
        return ''
    tx_ids = [tx.tx_id for tx in transactions]
    while len(tx_ids) > 1:
        if len(tx_ids) % 2 != 0:
            tx_ids.append(tx_ids[-1])
        new_tx_ids = []
        for i in range(0, len(tx_ids), 2):
            combined = tx_ids[i] + tx_ids[i+1]
            new_tx_ids.append(sha256(combined))
        tx_ids = new_tx_ids
    return tx_ids[0]

########################################
# Data Structures
########################################

class TransactionInput:
    def __init__(self, tx_id: str, output_index: int, signature: str = None):
        self.tx_id = tx_id
        self.output_index = output_index
        self.signature = signature

    def to_dict(self):
        return {
            'tx_id': self.tx_id,
            'output_index': self.output_index,
            'signature': self.signature
        }

class TransactionOutput:
    def __init__(self, amount: int, recipient_pubkey):
        self.amount = amount
        self.recipient_pubkey = recipient_pubkey

    def to_dict(self):
        key_repr = (self.recipient_pubkey.to_string().hex() 
                    if hasattr(self.recipient_pubkey, 'to_string') 
                    else self.recipient_pubkey)
        return {
            'amount': self.amount,
            'recipient_pubkey': key_repr
        }

class Transaction:
    def __init__(self, inputs: list, outputs: list):
        self.inputs = inputs
        self.outputs = outputs
        self.tx_id = self.compute_tx_id()

    def compute_tx_id(self) -> str:
        inputs_data = [inp.to_dict() for inp in self.inputs]
        outputs_data = [out.to_dict() for out in self.outputs]
        tx_data = serialize({'inputs': inputs_data, 'outputs': outputs_data})
        return sha256(tx_data)

class Block:
    def __init__(self, previous_hash: str, transactions: list, difficulty: int):
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = time.time()
        self.nonce = 0
        self.difficulty = difficulty
        self.merkle_root = self.compute_merkle_root()
        self.hash = self.compute_hash()

    def compute_merkle_root(self) -> str:
        return compute_merkle(self.transactions)

    def compute_hash(self) -> str:
        header = self.previous_hash + self.merkle_root + str(self.timestamp) + str(self.nonce)
        return sha256(header)

class Blockchain:
    def __init__(self):
        self.chain = []
        self.utxo_set = {}
        self.difficulty = 4

    def create_genesis_block(self):
        genesis_tx = Transaction([], [TransactionOutput(50, "genesis")])
        genesis_block = Block("0" * 64, [genesis_tx], self.difficulty)
        mined_block = self.mine_block(genesis_block)
        self.chain.append(mined_block)
        self.update_utxo_set(mined_block)
        print("Genesis block created with hash:", mined_block.hash)

    def mine_block(self, block: Block) -> Block:
        print("Mining new block...")
        while not valid_proof(block.hash, block.difficulty):
            block.nonce += 1
            block.hash = block.compute_hash()
        print(f"Block mined! Nonce: {block.nonce} | Hash: {block.hash}")
        return block

    def add_block(self, block: Block) -> bool:
        if self.validate_block(block):
            self.chain.append(block)
            self.update_utxo_set(block)
            return True
        return False

    def validate_block(self, block: Block) -> bool:
        if len(self.chain) > 0:
            last_block = self.chain[-1]
            if block.previous_hash != last_block.hash:
                print("Block rejected: previous hash mismatch.")
                return False
        if not valid_proof(block.hash, block.difficulty):
            print("Block rejected: invalid proof-of-work.")
            return False
        return True

    def update_utxo_set(self, block: Block):
        for tx in block.transactions:
            for inp in tx.inputs:
                utxo_key = (inp.tx_id, inp.output_index)
                if utxo_key in self.utxo_set:
                    del self.utxo_set[utxo_key]
            for index, out in enumerate(tx.outputs):
                utxo_key = (tx.tx_id, index)
                self.utxo_set[utxo_key] = out

    def add_transaction(self, transaction: Transaction):
        print("Transaction added to mempool (simulation):", transaction.tx_id)
        return transaction
