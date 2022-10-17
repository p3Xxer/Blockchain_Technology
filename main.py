import hashlib
import json
import random
import time
import datetime
import merkle_tree
from uuid import uuid4

# TODO add try except for all the functions
# TODO increase consensus time


class Land_Blockchain(object):
    # Constructor
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.users = {}
        self.property_history = {}
        self.node_ctr = 1
        self.prop_ctr = 1

    # Create user
    def create_user(self):
        print()
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
            print("The node was added to the blockchain\n")
            print(self.users[uid]['Name'] + "'s ID is " +
                  str(self.users[uid]['ID']) + "\n")
        except:
            print("Enter the correct format of data required to add a new node!\n")

    # Create New Block
    def create_new_block(self, previous_hash=None):
        mtree = merkle_tree.MerkleTree(self.hash(self.transactions[:3]))
        if (len(self.chain) == 0):
            block = {
                "Header": {
                    "Index": len(self.chain) + 1,
                    "Timestamp": datetime.datetime.now(),
                    "Merkle root": mtree.getRootHash(),
                    "previous_hash": 0,
                },
                "Transaction": self.transactions[:3]  # 3 transactions
            }
        else:
            block = {
                "Header": {
                    "Index": len(self.chain) + 1,
                    "Timestamp": datetime.datetime.now(),
                    "Merkle root": mtree.getRootHash(),
                    "previous_hash": self.hash(self.chain[-1]['Header']),
                },
                "Transaction": self.transactions[:3]  # 3 transactions
            }

        self.chain.append(block)
        del self.transactions[:3]
        return block

    # Create transaction
    def create_transaction(self):
        try:
            seller = int(input("\nEnter the Seller ID: "))
            buyer = int(input("Enter the Receiver ID: "))
            pid = int(input("Enter the Property ID: "))
            if (not self.validate_transaction(seller, buyer, pid)):
                print("\nThis Transaction is not valid\n")
                return
            print("\nThis Transaction is added and validated\n")
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
            self.users[seller]['Number of properties'] = self.users[seller]['Number of properties'] - 1
            self.users[buyer]['Properties owned'].append(pid)
            self.users[buyer]['Number of properties'] = self.users[buyer]['Number of properties'] + 1

            if (len(self.transactions) == 3):
                self.create_timer()
                print("\nCreating a new block\n")
        except:
            print("Enter the correct format of data required to add a new transaction!\n")

    # Validate Transaction
    def validate_transaction(self, seller, buyer, pid):
        if (seller == buyer):
            print("You cannot sell the property to yourself")
            return False
        if pid in self.property_history.keys():
            if seller in self.users.keys() and buyer in self.users.keys():
                if self.property_history[pid]['Owner'] == seller:
                    return True
                else:
                    print("\nThe seller does not own this property!")
        return False

    # Validate Chain
    def validate_chain(self):
        if (len(self.chain) == 0):
            return False
        previous_block = self.chain[0]
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            print("\nHash of Header of Block " + str(i-1) + " : " +
                  str(self.hash(previous_block['Header'])))
            print("Hash of Previous Block's Header stored in Block " + str(i) + " : ",
                  current_block['Header']['previous_hash'])
            if (current_block['Header']['previous_hash'] != self.hash(previous_block['Header'])):
                return False
            previous_block = current_block
        return True

    # Print Blockchain
    def print_blockchain(self):
        print()
        if (len(self.chain) == 0):
            print("Blockchain is empty, please add more transactions :)\n")
            return
        for i in range(len(self.chain)):
            print("Block", i+1, ":")
            print("Header: ", self.chain[i]['Header'])
            print("Transactions: ")
            for j in range(len(self.chain[i]['Transaction'])):
                print(self.chain[i]['Transaction'][j])
            print()
        print()

    # Print Property History
    def print_property_history(self, pid):
        try:
            print()
            for i in self.users.keys():
                if self.users[i]['ID'] == self.property_history[pid]['Owner']:
                    print("The Owner of this property is: " +
                          str(self.users[i]['Name']))
            print("The transaction history of this property is: ")
            for i in self.property_history[pid]['History']:
                print(i)
            print()

        except:
            print("\nPlease enter the correct inputs!\n")

    # Hash Function

    def hash(self, block):
        strg = json.dumps(block, sort_keys=True, default=str).encode()
        return hashlib.sha256(strg).hexdigest()

    # Create Timer for Achieving Consensus
    def create_timer(self):
        mini = 100000
        for i in self.users.keys():
            n = random.randint(1, 10)
            self.users[i]['wait-time'] = n
            mini = min(mini, n)

        print("\n-------------------Acheiving consensus-------------------\n")
        time.sleep(mini)

        for i in self.users.keys():
            if (self.users[i]['wait-time'] == mini):
                print(str(
                    self.users[i]['Name']) + " has the least wait time, thus the leader for this round of consensus will mine the block.\n")
                self.create_new_block()
                break

    # Print Users
    def print_nodes(self):
        print()
        for i in self.users.keys():
            print("User ID: ", i)
            print("Name: ", self.users[i]['Name'])
            print("Number of properties owned: ",
                  self.users[i]['Number of properties'])
            print("Property IDs: ", self.users[i]['Properties owned'])
        print()


if __name__ == '__main__':
    mine = Land_Blockchain()
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
                print("\nThe Blockchain is valid!\n")
            else:
                print("\nThe Blockchain is not valid!\n")
        elif (choice == 7):
            print("Hope you had a blast using LAND MINE!!")
            break
        else:
            print("Invalid choice")
