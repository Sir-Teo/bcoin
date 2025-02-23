from ecdsa import SigningKey, SECP256k1, VerifyingKey
from src.blockchain import Transaction, TransactionInput, TransactionOutput

class Wallet:
    def __init__(self):
        self.private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.private_key.get_verifying_key()

    def sign(self, message: str) -> str:
        signature = self.private_key.sign(message.encode('utf-8'))
        return signature.hex()

    def create_transaction(self, blockchain, outputs: list) -> Transaction:
        available_utxos = []
        total_amount = 0
        for utxo_key, utxo in blockchain.utxo_set.copy().items():
            if hasattr(utxo.recipient_pubkey, 'to_string'):
                if utxo.recipient_pubkey.to_string() == self.public_key.to_string():
                    available_utxos.append((utxo_key, utxo))
                    total_amount += utxo.amount
            else:
                available_utxos.append((utxo_key, utxo))
                total_amount += utxo.amount

        required_amount = sum([o.amount for o in outputs])
        if total_amount < required_amount:
            print("Transaction creation failed: insufficient funds.")
            return None

        inputs = []
        accumulated = 0
        for utxo_key, utxo in available_utxos:
            tx_id, index = utxo_key
            inp = TransactionInput(tx_id, index, "")
            inputs.append(inp)
            accumulated += utxo.amount
            if accumulated >= required_amount:
                break

        if accumulated > required_amount:
            change = accumulated - required_amount
            outputs.append(TransactionOutput(change, self.public_key))

        tx = Transaction(inputs, outputs)
        for inp in tx.inputs:
            inp.signature = self.sign(tx.tx_id)
        print("Wallet created transaction with tx_id:", tx.tx_id)
        return tx
