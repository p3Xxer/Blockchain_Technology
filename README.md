# Blockchain_Technology


# Group Details
# Khushil Kataria - 2020A7PS2086H
# Dhairya Agrawal - 2020A7PS0130H
# Pulkit Agrawal - 2020A7PS2072H
# Rahil Sanghavi - 2020A7PS2052H



## Land Management System using Blockchain
## The consensus algorithm used is Proof of Elapsed Time (PoET)

### --------------------COMPONENTS-------------------
## 1. Block
### Timestamp, Merkle root, Hash of the previous block, Transactions{List of transactions}
### block = {
###     "Header": {
###         "Index": len(self.chain) + 1,
###         "Timestamp": "",
###         "Merkle root": "",
###         "Hash of the previous block's header": "",
###     },
###     "Transaction": []
### }
###
## 2. Transaction
### Buyer ID, Seller ID, Property ID, Timestamp of the transaction.
### transaction = {
###     "Buyer ID": "",
###     "Seller ID": "",
###     "Property ID": "",
###     "Timestamp of the transaction": ""
### }
###
## 3. Node(All nodes are miners)
### Name, ID, Properties_Owned: [list of Properties], number of properties owned: num_prop
###
## 4. Property History
### property_history = {
###     "Property_ID": {
###         "Owner": "",
###         "History": []
###     }
### }

### --------------------FUNCTIONS-------------------
### 1. Create_Block
#### Create a new Block as soon as minimum threshold of transactions occur
### 2. Create_Node
#### Register new users as sellers or miners
### 3. New_Transaction
#### Create a new Transaction
### 4. Print_Property_history
#### Print the details of all the transactions related to a property
### 5. Print_Nodes
#### Print the details of particular user
### 6. Print_BlockChain
#### Print the entire BlockChain network
### 7. Poet(Create_Timer)
#### Implementation of Proof Of Elapsed Time
### 8. Print_Miner(Print_Leader)
#### Print the details of the Miner node selected by POET 
### 9. Create_Merkle_Tree
#### Implement Merkle Tree
### 10. Validate_Chain
#### Validates the Blockchain
### 11. Hash_Block
#### Hashes the data using SHA 256 protocol
### 12. Validate Transaction
#### Validates the transaction and checks for anomalies


