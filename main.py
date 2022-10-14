import hashlib
import json
import random
import time
import datetime
import merkle_tree
from uuid import uuid4

# TODO add merkle tree
# TODO add try except for all the functions
# TODO increase consensus time


#--------------------COMPONENTS-------------------#
# Block
# Timestamp, Merkle root, Hash of the previous block, Transactions{List of transactions}
# block = {
#     "Header": {
#         "Index": len(self.chain) + 1,
#         "Timestamp": "",
#         "Merkle root": "",
#         "Hash of the previous block's header": "",
#     },
#     "Transaction": []
# }

# Transaction
# Buyer ID, Seller ID, Property ID, Timestamp of the transaction.
# transaction = {
#     "Buyer ID": "",
#     "Seller ID": "",
#     "Property ID": "",
#     "Timestamp of the transaction": ""
# }

# Node(All nodes are miners)
# Name, ID, Properties_Owned: [list of Properties], number of properties owned: num_prop

# Property History
# property_history = {
#     "Property_ID": {
#         "Owner": "",
#         "History": []
#     }
# }
# POET
# Merkle Tree
# 3 Transactions in each block

#--------------------FUNCTIONS-------------------#
# 1. Create_Block - Done
# 2. Create_Node - Done
# 3. New_Transaction - Done
# 4. Print_Property_history - Done
# 5. Print_Nodes - Done
# 6. Print_BlockChain - Done
# 7. Poet(Create_Timer) - Done
# 8. Print_Miner(Print_Leader) - Done
# 9. Create_Merkle_Tree -
# 10. Validate_Chain - Done
# 11. Hash_Block - Done
# 12. Validate Transaction - Done

# try and accept
class Land_Blockchain(object):
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.users = {}
        self.property_history = {}
        self.node_ctr = 1
        self.prop_ctr = 1

    def create_user(self):
        self.mine = 0
        try:
            uid = self.node_ctr
            miner = str(input("Enter the name of the node: "))
            props_num = int(
                input("Enter the number of properties owned by the node: "))
            self.node_ctr = self.node_ctr + 1
            props = []
            for i in range(props_num):
                pid = self.prop_ctr+i
                props.append(pid)
                self.property_history[pid] = {
                    'Owner': uid,
                    'History': []
                }
            self.prop_ctr = self.prop_ctr + props_num
            self.users[uid] = {
                'ID': uid,
                'Name': miner,
                'Number of properties': props_num,
                'Properties owned': props
            }
            self.mine = 1
            print("The node was added to the blockchain")
        except:
            print("Enter the correct format of data required to add a new node!")

    def create_new_block(self, previous_hash=None):
        mtree = self.hash(self.transactions[:3])
        if (len(self.chain) == 0):
            block = {
                "Header": {
                    "Index": len(self.chain) + 1,
                    "Timestamp": datetime.datetime.now(),
                    "Merkle root": mtree,
                    "previous_hash": 0,
                },
                "Transaction": self.transactions[:3]  # 3 transactions
            }
        else:
            block = {
                "Header": {
                    "Index": len(self.chain) + 1,
                    "Timestamp": datetime.datetime.now(),
                    "Merkle root": mtree,
                    "previous_hash": self.hash(self.chain[-1]['Header']),
                },
                "Transaction": self.transactions[:3]  # 3 transactions
            }

        self.chain.append(block)
        del self.transactions[:3]
        return block

    # Create transaction
    def create_transaction(self):
        # Taking the inputs of the transaction data
        seller = int(input("Enter the Seller ID: "))
        buyer = int(input("Enter the Receiver ID: "))
        pid = int(input("Enter the Property ID: "))
        if (self.validate_transaction(seller, buyer, pid)):
            print("This Transaction is added and validated...")
            trans = {
                "Transaction_ID": str(uuid4()).replace('-', ''),
                "Timestamp": datetime.datetime.now(),
                "Seller ID": seller,
                "Buyer ID": buyer,
                "Property ID": pid,
            }
            self.transactions.append(trans)
            self.property_history[pid]["Owner"] = buyer
            self.property_history[pid]["History"].append(trans)
            self.users[seller]['Properties owned'].remove(pid)
            self.users[buyer]['Properties owned'].append(pid)
            print("Transaction validated")
            if (len(self.transactions) == 3):
                print("Creating a new block")
                self.create_timer()
        else:
            print("This transaction is not valid!")

    # Validate transaction
    def validate_transaction(self, seller, buyer, pid):
        for i in self.property_history.keys():
            if (i == pid):
                if (seller in self.users[j]["ID"] for j in range(len(self.users))):
                    if (buyer in self.users[k]["ID"] for k in range(len(self.users))):
                        if (self.property_history[i]['Owner'] == seller):
                            return True
        return False

    # Validate Chain
    def validate_chain(self):
        previous_block = self.chain[0]
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            if (current_block['Header']['previous_hash'] != self.hash(previous_block['Header'])):
                return False
            previous_block = current_block
        return True

    # Print block chain
    def print_blockchain(self):
        for i in range(len(self.chain)):
            print("Block", i+1, ":", self.chain[i])

    # Print property history
    def print_property_history(self, pid):
        for i in self.users.keys():
            if self.users[i]['ID'] == self.property_history[pid]['Owner']:
                print("The Owner of this property is: " +
                      str(self.users[i]['Name']))
        print("The transaction history of this property is: " +
              str(self.property_history[pid]['History']))

    # Hash Function

    def hash(self, block):
        strg = json.dumps(block, sort_keys=True, default=str).encode()
        return hashlib.sha256(strg).hexdigest()

    def create_timer(self):
        self.minimum = 100000
        for i in self.users.keys():
            # Generating a random number using the random package of Python.We consider the number(wait time) to be between 1 and 5 seconds.
            n = random.randint(1, 5)
            self.users[i]['wait-time'] = n
            # Finding out the minimum wait time
            self.minimum = min(self.minimum, n)
        # All nodes go for sleep. The node which has the least time would be the leader.
        print("Acheiving consensus.........................")
        # We keep the program to sleep for the specified minimum wait time in order to know the leader
        time.sleep(self.minimum)

        for i in self.users.keys():
            if (self.users[i]['wait-time'] == self.minimum):
                print(str(
                    self.users[i]['Name']) + " has the least wait time, thus the leader for the round of consensus and will mine the block.")
                self.create_new_block()
                break

    def print_nodes(self):
        print(self.users)


if __name__ == '__main__':
    mine = Land_Blockchain()
    # 4 options to perform different functions
    while True:
        print("1. Create a new user")
        print("2. Create a new transaction")
        print("3. Print the blockchain")
        print("4. Print the property history")
        print("5. Print the users")
        print("6. Validate Blockchain")
        print("7. Exit")
        choice = int(input("Enter your choice: "))
        if (choice == 1):
            mine.create_user()
        elif (choice == 2):
            mine.create_transaction()
        elif (choice == 3):
            mine.print_blockchain()
        elif (choice == 4):
            pid = int(input("Enter the property ID: "))
            mine.print_property_history(pid)
        elif (choice == 5):
            mine.print_nodes()
        elif (choice == 6):
            if (mine.validate_chain()):
                print("The Blockchain is valid!")
            else:
                print("The Blockchain is not valid!")
        elif (choice == 7):
            break
        else:
            print("Invalid choice")
