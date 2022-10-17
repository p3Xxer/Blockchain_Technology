# Blockchain_Technology

## Land Management System using Blockchain
## The consensus algorithm used is Proof of Elapsed Time (PoET)

### --------------------COMPONENTS-------------------
### Block
### Timestamp, Merkle root, Hash of the previous block, Transactions{List of transactions}
### block = {f
###     "Header": {
###         "Index": len(self.chain) + 1,
###         "Timestamp": "",
###         "Merkle root": "",
###         "Hash of the previous block's header": "",
###     },
###     "Transaction": []
### }

### Transaction
### Buyer ID, Seller ID, Property ID, Timestamp of the transaction.
### transaction = {
###     "Buyer ID": "",
###     "Seller ID": "",
###     "Property ID": "",
###     "Timestamp of the transaction": ""
### }

### Node(All nodes are miners)
### Name, ID, Properties_Owned: [list of Properties], number of properties owned: num_prop

### Property History
### property_history = {
###     "Property_ID": {
###         "Owner": "",
###         "History": []
###     }
### }

### --------------------FUNCTIONS-------------------
### 1. Create_Block
### 2. Create_Node
### 3. New_Transaction
### 4. Print_Property_history
### 5. Print_Nodes
### 6. Print_BlockChain
### 7. Poet(Create_Timer)
### 8. Print_Miner(Print_Leader)
### 9. Create_Merkle_Tree
### 10. Validate_Chain
### 11. Hash_Block
### 12. Validate Transaction


