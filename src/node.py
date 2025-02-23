from src.blockchain import Blockchain

class Node:
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
        self.peers = []
        self.seen_messages = set()

    def add_peer(self, peer_node):
        self.peers.append(peer_node)

    def broadcast(self, message: dict):
        for peer in self.peers:
            peer.receive_message(message)

    def receive_message(self, message: dict):
        msg_type = message.get('type')
        data = message.get('data')

        if msg_type == 'transaction':
            msg_id = data.tx_id
        elif msg_type == 'block':
            msg_id = data.hash
        else:
            return

        if msg_id in self.seen_messages:
            return
        self.seen_messages.add(msg_id)

        if msg_type == 'transaction':
            tx = data
            print("Node received transaction:", tx.tx_id)
            self.blockchain.add_transaction(tx)
            self.broadcast(message)
        elif msg_type == 'block':
            block = data
            print("Node received block with hash:", block.hash)
            if self.blockchain.validate_block(block):
                self.blockchain.add_block(block)
                self.broadcast(message)
