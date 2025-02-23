from src.blockchain import Blockchain, Block, Transaction, TransactionOutput
from src.wallet import Wallet
from src.node import Node

def main():
    # Create the blockchain and genesis block.
    blockchain = Blockchain()
    blockchain.create_genesis_block()

    # Initialize two nodes and connect them.
    node1 = Node(blockchain)
    node2 = Node(blockchain)
    node1.add_peer(node2)
    node2.add_peer(node1)

    # Create two wallets.
    wallet1 = Wallet()
    wallet2 = Wallet()

    # Simulate a coinbase-like transaction to send funds from genesis to wallet1.
    for utxo_key, utxo in list(blockchain.utxo_set.items()):
        if utxo.recipient_pubkey == "genesis":
            coinbase_tx = Transaction([], [TransactionOutput(50, wallet1.public_key)])
            break

    block1 = Block(blockchain.chain[-1].hash, [coinbase_tx], blockchain.difficulty)
    mined_block1 = blockchain.mine_block(block1)
    blockchain.add_block(mined_block1)
    node1.broadcast({'type': 'block', 'data': mined_block1})

    # Wallet1 creates a transaction sending 30 coins to Wallet2.
    tx1 = wallet1.create_transaction(blockchain, [TransactionOutput(30, wallet2.public_key)])
    if tx1:
        node1.broadcast({'type': 'transaction', 'data': tx1})

    block2 = Block(blockchain.chain[-1].hash, [tx1], blockchain.difficulty)
    mined_block2 = blockchain.mine_block(block2)
    blockchain.add_block(mined_block2)
    node1.broadcast({'type': 'block', 'data': mined_block2})

    # Print the final blockchain state.
    print("\nFinal Blockchain State:")
    for idx, block in enumerate(blockchain.chain):
        print(f"\nBlock {idx} | Hash: {block.hash}")
        print(" Previous Hash:", block.previous_hash)
        print(" Timestamp:", block.timestamp)
        print(" Nonce:", block.nonce)
        print(" Merkle Root:", block.merkle_root)
        for tx in block.transactions:
            print("  Transaction:", tx.tx_id)
            for inp in tx.inputs:
                print("    Input -> tx_id:", inp.tx_id, "index:", inp.output_index, "signature:", inp.signature)
            for out in tx.outputs:
                recipient = (out.recipient_pubkey.to_string().hex() 
                             if hasattr(out.recipient_pubkey, 'to_string') 
                             else out.recipient_pubkey)
                print("    Output -> amount:", out.amount, "recipient:", recipient)

if __name__ == "__main__":
    main()
