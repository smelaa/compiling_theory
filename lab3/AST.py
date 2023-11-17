

from __future__ import print_function

class Node(object):
    pass

class Start(Node):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

class IntNum(Node):
    def __init__(self, val):
        self.val = val

class FloatNum(Node):

    def __init__(self, val):
        self.val = val


class Variable(Node):
    def __init__(self, name):
        self.name = name


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class Assign(Node):
    def __init__(self, op, name, val):
        self.op = op
        self.name = name
        self.val = val

class UnaryExpr(Node):
    def __init__(self, op, val):
        self.op = op
        self.val = val

class BracketExpr(Node): #TODO -> dodać metodę do wypisania
    def __init__(self, val):
        self.bracket = "()"
        self.val = val

class Vector(Node):
    def __init__(self, val):
        self.val = val

class VectorValues(Node):
    def __init__(self, val, next = None):
        self.val = val
        self.next = next

class RefAssign(Node):
    def __init__(self, op, name, index, val):
        self.op = op
        self.name = name
        self.index = index
        self.val = val

class Index(Node):
    def __init__(self, index1, index2):
        self.index1 = index1
        self.index2 = index2

class Fid(Node):
    def __init__(self, fid, val):
        self.fid = fid
        self.val = val

# ...
# fill out missing classes
# ...

class Error(Node):
    def __init__(self):
        pass



def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:

    @addToClass(Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)


    @addToClass(Start)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|\t", end="")
        self.p1.printTree(indent)
        self.p2.printTree(indent)

    @addToClass(IntNum)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|\t", end="")
        print(self.val)

    @addToClass(FloatNum)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|\t", end="")
        print(self.val)

    @addToClass(Variable)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|\t", end="")
        print(self.name)

    @addToClass(BinExpr)
    def printTree(self, indent = 0):
        for i in range(indent):
            print("|\t", end="")
        print(self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(Assign)
    def printTree(self, indent = 0):
        for i in range(indent):
            print("|\t", end="")
        print(self.op)
        self.name.printTree(indent + 1)
        self.val.printTree(indent + 1)

    @addToClass(UnaryExpr)
    def printTree(self, indent = 0):
        for i in range(indent):
            print("|\t", end="")
        print(self.op)
        self.val.printTree(indent + 1)

    @addToClass(Vector)
    def printTree(self, indent = 0):
        for i in range(indent):
            print("|\t", end="")
        print("VECTOR")
        self.val.printTree(indent + 1)

    @addToClass(VectorValues)
    def printTree(self, indent = 0):
        self.val.printTree(indent)
        if self.next != None:
            self.next.printTree(indent)

    @addToClass(RefAssign)
    def printTree(self, indent = 0):
        for i in range(indent):
            print("|\t", end="")
        print(self.op)
        print("|\tREF")
        self.name.printTree(indent + 2)
        self.index.printTree(indent + 2)
        self.val.printTree(indent + 1)

    @addToClass(Index)
    def printTree(self, indent = 0):
        self.index1.printTree(indent)
        self.index2.printTree(indent)

    @addToClass(Fid)
    def printTree(self, indent = 0):
        for i in range(indent):
            print("|\t", end="")
        print(self.fid)
        self.val.printTree(indent + 1)

    @addToClass(Error)
    def printTree(self, indent=0):
        pass
        # fill in the body

    # define printTree for other classes
    # ...


