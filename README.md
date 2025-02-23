# bcoin

A minimal blockchain simulation implemented in Python. It demonstrates basic blockchain concepts such as proof-of-work, transactions, a UTXO model, wallets using ECDSA keys, and a simple P2P network simulation.

## Features

- **Blockchain**: Contains blocks with transactions and proof-of-work.
- **Transactions**: Basic transaction structure with inputs, outputs, and signatures.
- **Wallet**: Generates key pairs and creates signed transactions.
- **Networking**: Simulated P2P network for broadcasting transactions and blocks.

## Usage

The only dependency is the `ecdsa` library. Install it with:

```
pip install ecdsa
```

```
python main.py
```

## Example Output

```
Mining new block...
Block mined! Nonce: 14506 | Hash: 0000eb0f1c8a479d4b4171d0f91896ea286693be7e5b1928612794a4701992ae
Genesis block created with hash: 0000eb0f1c8a479d4b4171d0f91896ea286693be7e5b1928612794a4701992ae
Mining new block...
Block mined! Nonce: 33280 | Hash: 00009c32ef70241e545b96924b5e1c6de906eef1c297fef06aa3f23f6dc25bae
Node received block with hash: 00009c32ef70241e545b96924b5e1c6de906eef1c297fef06aa3f23f6dc25bae
Block rejected: previous hash mismatch.
Wallet created transaction with tx_id: 19cc8490d67cfd6edf68441fa38a8d3c95208d90bc52fe17caad7fa79b007c77
Node received transaction: 19cc8490d67cfd6edf68441fa38a8d3c95208d90bc52fe17caad7fa79b007c77
Transaction added to mempool (simulation): 19cc8490d67cfd6edf68441fa38a8d3c95208d90bc52fe17caad7fa79b007c77
Node received transaction: 19cc8490d67cfd6edf68441fa38a8d3c95208d90bc52fe17caad7fa79b007c77
Transaction added to mempool (simulation): 19cc8490d67cfd6edf68441fa38a8d3c95208d90bc52fe17caad7fa79b007c77
Mining new block...
Block mined! Nonce: 25708 | Hash: 00008efcb1bb82878af57b024abada7990cdd036f51f823b44e1b96e3b2a1d40
Node received block with hash: 00008efcb1bb82878af57b024abada7990cdd036f51f823b44e1b96e3b2a1d40
Block rejected: previous hash mismatch.

Final Blockchain State:

Block 0 | Hash: 0000eb0f1c8a479d4b4171d0f91896ea286693be7e5b1928612794a4701992ae
 Previous Hash: 0000000000000000000000000000000000000000000000000000000000000000
 Timestamp: 1740346193.8694808
 Nonce: 14506
 Merkle Root: 3d6099caada2fecdb9077829c0fe8e82f9c5645216ce1921f4d70615b156cb08
  Transaction: 3d6099caada2fecdb9077829c0fe8e82f9c5645216ce1921f4d70615b156cb08
    Output -> amount: 50 recipient: genesis

Block 1 | Hash: 00009c32ef70241e545b96924b5e1c6de906eef1c297fef06aa3f23f6dc25bae
 Previous Hash: 0000eb0f1c8a479d4b4171d0f91896ea286693be7e5b1928612794a4701992ae
 Timestamp: 1740346193.894497
 Nonce: 33280
 Merkle Root: 32100ca55275f6bbcd210c58a01df2c2824d924e04ab9014594cacfa0480cbe0
  Transaction: 32100ca55275f6bbcd210c58a01df2c2824d924e04ab9014594cacfa0480cbe0
    Output -> amount: 50 recipient: f6b1b37c8ef74f1a55cea1ff22d1039c3113c0d970f816279c296b840a96d279d022921afb11fd5f41f8f951ca7116255692db36a4c58585f57c8b3645702f47

Block 2 | Hash: 00008efcb1bb82878af57b024abada7990cdd036f51f823b44e1b96e3b2a1d40
 Previous Hash: 00009c32ef70241e545b96924b5e1c6de906eef1c297fef06aa3f23f6dc25bae
 Timestamp: 1740346193.943789
 Nonce: 25708
 Merkle Root: 19cc8490d67cfd6edf68441fa38a8d3c95208d90bc52fe17caad7fa79b007c77
  Transaction: 19cc8490d67cfd6edf68441fa38a8d3c95208d90bc52fe17caad7fa79b007c77
    Input -> tx_id: 3d6099caada2fecdb9077829c0fe8e82f9c5645216ce1921f4d70615b156cb08 index: 0 signature: 724bf27a0fd88d3d41c67887d4498d03d5b634564c47bdce3594c60a39257d684233f4e9f45b3e02283bfa851db32820abace9dae3d76304ac243dcd9951396b
    Output -> amount: 30 recipient: 2668a4f02c648ae45e668b54c92d43befe8f02c58ec979aefc86b2158466d159b625b536a9378e3675309a9e017c760c60766b5c8d65760b194059847f890e10
    Output -> amount: 20 recipient: f6b1b37c8ef74f1a55cea1ff22d1039c3113c0d970f816279c296b840a96d279d022921afb11fd5f41f8f951ca7116255692db36a4c58585f57c8b3645702f47
```

Happy coding! 🚀
