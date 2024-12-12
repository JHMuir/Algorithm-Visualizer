class TreeAlgorithms:
    def __init__(self):
        self.curr_node = None
        self.tree = None

    class Node:
        def __init__(self, value):
            self.value = value
            self.left = None
            self.right = None

    def create_sample_tree(self):
        self.tree = self.Node(5)
        self.tree.left = self.Node(30)
        self.tree.right = self.Node(70)
        self.tree.left.left = self.Node(20)
        self.tree.left.right = self.Node(40)
        self.tree.right.left = self.Node(60)
        self.tree.right.right = self.Node(80)

    def inorder_traversal(self, node):
        """In-Order Traversal"""
        if node:
            print(node.value)
            self.current_node = node
            yield from self.inorder_traversal(node.left)
            yield node
            yield from self.inorder_traversal(node.right)

    def preorder_traversal(self, node):
        """Pre-Order Traversal"""
        if node:
            print(node.value)
            self.current_node = node
            yield node
            yield from self.preorder_traversal(node.left)
            yield from self.preorder_traversal(node.right)

    def postorder_traversal(self, node):
        """Post-Order Traversal"""
        if node:
            print(node.value)
            self.current_node = node
            yield from self.postorder_traversal(node.left)
            yield from self.postorder_traversal(node.right)
            yield node
