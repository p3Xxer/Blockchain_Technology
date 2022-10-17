import hashlib

class Node:
    def __init__(self, left, right, value):
        self.left: Node = left
        self.right: Node = right
        self.value = value

class MerkleTree:
    def __init__(self, values):
        leaves = [Node(None, None, self.hash(e)) for e in values]
        if len(leaves) % 2 == 1:
            leaves.append(leaves[-1])
        self.root = self.buildTree(leaves)

    def hash(self, val):
        return hashlib.sha256(val.encode('utf-8')).hexdigest()

    def buildTree(self, nodes):
        if len(nodes) % 2 == 1:
            nodes.append(nodes[-1])
        half = len(nodes) // 2

        if len(nodes) == 2:
            return Node(nodes[0], nodes[1], self.hash(nodes[0].value + nodes[1].value))

        left = self.buildTree(nodes[:half])
        right = self.buildTree(nodes[half:])
        value = self.hash(left.value + right.value)
        return Node(left, right, value)

    def getRootHash(self):
        return self.root.value