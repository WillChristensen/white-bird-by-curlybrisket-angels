import sys

class RedBlackTree:
    class Underflow(Exception):
        def __init__(self, data = None):
            super().__init__(data)

    class Nodes(object):
        def __init__(self, data=None, color=None, value=None, dictionary=None):
            self.key = data
            self.color = color
            self.left = value
            self.right = value
            self.parent = value
            self.dictionary = dictionary

        def __eq__(self, other):
            return self.__dict__ == other.__dict__

    def __init__(self):
        self.size = 0
        self.root = self.Nodes(None, 'BLACK', None) #Starts as a Sentinel for first insert
        self.NIL = self.Nodes(None, 'BLACK', None) #The Sentinel
        self.travelList = []
        self.bestList = []
        self.bestTotal = 0

    def get_root(self):
        return self.root

    def left_rotate(self, x): #Node x
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x): #Node x
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(self, value, dictionary):
        y = self.NIL
        x = self.root
        z = self.Nodes(value, 'RED', self.NIL, dictionary)
        while x != self.NIL:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == self.NIL:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.left = self.NIL
        z.right = self.NIL
        z.color = 'RED'
        self.RB_insert_fixup(z)
        self.size = self.size + 1

    def RB_insert_fixup(self, z):
        while z.parent.color == 'RED':
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == 'RED':
                    z.parent.color = 'BLACK'
                    y.color = 'BLACK'
                    z.parent.parent.color = 'RED'
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = 'BLACK'
                    z.parent.parent.color = 'RED'
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == 'RED':
                    z.parent.color = 'BLACK'
                    y.color = 'BLACK'
                    z.parent.parent.color = 'RED'
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = 'BLACK'
                    z.parent.parent.color = 'RED'
                    self.left_rotate(z.parent.parent)
        self.root.color = 'BLACK'

    def remove(self, z): #Add transplant and minimum
        z = self.tree_search(self.root, z)
        y = z
        y_original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.tree_minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 'BLACK':
            self.RB_delete_fixup(x)
        self.size = self.size - 1

    def RB_delete_fixup(self, x):
        while x != self.root and x.color == 'BLACK':
            if x == x.parent.left:
                w = x.parent.right
                if w.color == 'RED':
                    w.color = 'BLACK'
                    x.parent.color = 'RED'
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == 'BLACK' and w.right.color == 'BLACK':
                    w.color = 'RED'
                    x = x.parent
                else:
                    if w.right.color == 'BLACK':
                        w.left.color = 'BLACK'
                        w.color = 'RED'
                        self.right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = 'BLACK'
                    w.right.color = 'BLACK'
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == 'RED':
                    w.color = 'BLACK'
                    x.parent.color = 'RED'
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == 'BLACK' and w.left.color == 'BLACK':
                    w.color = 'RED'
                    x = x.parent
                else:
                    if w.left.color == 'BLACK':
                        w.right.color = 'BLACK'
                        w.color = 'RED'
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = 'BLACK'
                    w.left.color = 'BLACK'
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 'BLACK'

    def transplant(self, u, v):
        if u.parent == self.NIL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def tree_minimum(self, x):
        while x.left != self.NIL:
            x = x.left
        return x

    def tree_maximum(self, x):
        while x.right != self.NIL:
            x = x.right
        return x

    def MaxMin(self, action):
        if action == "max":
            value = self.tree_maximum(self.root)
            print(value.key)
        else:
            value = self.tree_minimum(self.root)
            print(value.key)

    def tree_search(self, x, k): # key is the number we're searching for
        if x == self.NIL or k == x.key:
            return x
        if k < x.key:
            return self.tree_search(x.left, k)
        else:
            return self.tree_search(x.right, k)        

    def inorder_tree_walk(self, x): #List in order
        if x != self.NIL:
            self.inorder_tree_walk(x.left)
            self.travelList.append(str(x.key))
            self.inorder_tree_walk(x.right)

    def to_list_preorder(self, x):
        if x != self.NIL:
            self.travelList.append(str(x.key))
            self.to_list_preorder(x.left)
            self.to_list_preorder(x.right)

    def to_list_postorder(self, x):
        if x != self.NIL:
            self.to_list_postorder(x.left)
            self.to_list_postorder(x.right)
            self.travelList.append(str(x.key))

    def to_string(self, travel):
        if travel == "inprint":
            self.inorder_tree_walk(self.root)
        elif travel == "preprint":
            self.to_list_preorder(self.root)
        elif travel == "postprint":
            self.to_list_postorder(self.root)
        else:
            final = self.best_path_value(self.root)
            print(final)
            return

        print(" ".join(self.travelList))
        self.travelList = [] 

    def search(self, k):
        if self.tree_search(self.root, k) == self.NIL:
            print("NotFound")
        else:
            print("Found")       

    def is_empty(self):
        if self.size == 0:
            return True
        else:
            return False

    def best_path_value(self, x):
        if x is None:
            return 0

        L = self.best_path_value(x.left)
        R = self.best_path_value(x.right)

        return max(L, R) + str(x.key).count('5')

"""
def driver():
    b = RedBlackTree()
    with open(sys.argv[1]) as f:
        n = int(f.readline().strip())
        for _ in range(n):
            in_data = f.readline().strip().split()
            action, value_option = in_data[0], in_data[1:]
            if action == "insert":
                value = int(value_option[0])
                b.insert(value)
            elif action == "remove":
                try:
                    value = int(value_option[0])
                    b.remove(value)
                except Exception as UnderflowError:
                    print("TreeError")
            elif action == "inprint":
                if b.is_empty() == True:
                    print("Empty")
                else:
                    b.to_string(action)
            elif action == "max":
                if b.is_empty() == True:
                    print("Empty")
                else:
                    b.MaxMin(action)
            elif action == "min":
                if b.is_empty() == True:
                    print("Empty")
                else:
                    b.MaxMin(action)
            elif action == "search":
                if b.is_empty() == True:
                    print("NotFound")
                else:
                    value = int(value_option[0])
                    b.search(value)
            elif action == "preprint":
                if b.is_empty() == True:
                    print("Empty")
                else:
                    b.to_string(action)
            elif action == "postprint":
                if b.is_empty() == True:
                    print("Empty")
                else:
                    b.to_string(action)
            elif action == "bpv":
                if b.is_empty() == True:
                    print("TreeError")
                else:
                    b.to_string(action)

if __name__ == "__main__":
    driver()
"""
