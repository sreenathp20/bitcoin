from bitcoin_tools.core.keys import load_keys
from bitcoin_tools.core.transaction import TX

# Key loading
btc_addr = "miWdbNn9zDLnKpcNuCLdfRiJx59c93bT8t"
sk, pk = load_keys(btc_addr)

# Reference to the previous transaction output that will be used to redeem and spend the funds, consisting on an id and
# an output index.
prev_tx_id = "7767a9eb2c8adda3ffce86c06689007a903b6f7e78dbc049ef0dbaf9eeebe075"
prev_out_index = 0

# Amount to be spent, in Satoshis, and the fee to be deduced (should be calculated).
value = 6163910
fee = 230 * 240

# Destination Bitcoin address where the value in bitcoins will be sent and locked until the owner redeems it.
destination_btc_addr = "miWdbNn9zDLnKpcNuCLdfRiJx59c93bT8t"

# First, we  build our transaction from io (input/output) using the previous transaction references, the value, and the
# destination.
tx = TX.build_from_io(prev_tx_id, prev_out_index, value - fee, destination_btc_addr)
# Finally, the transaction is signed using the private key associated with the Bitcoin address from each input.
# Input 0 will be signed, since we have only created one.
tx.sign(sk, 0)

# Once created we can display the serialized transaction. Transaction is now ready to be broadcast.
print ("hex: " + tx.serialize())

# Finally, we can analyze each field of the transaction.
tx.display()