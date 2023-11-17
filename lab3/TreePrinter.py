from __future__ import print_function
import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)


    @addToClass(AST.Start)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|\t", end="")
        self.p1.printTree(indent)
        self.p2.printTree(indent)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|\t", end="")
        print(self.val)

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|\t", end="")
        print(self.val)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        for i in range(indent):
            print("|\t", end="")
        print(self.name)

    @addToClass(AST.BinExpr)
    def printTree(self, indent = 0):
        for i in range(indent):
            print("|\t", end="")
        print(self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Assign)
    def printTree(self, indent = 0):
        for i in range(indent):
            print("|\t", end="")
        print(self.op)
        print("|\t", self.name)
        self.val.printTree(indent + 1)

    @addToClass(AST.UnaryExpr)
    def printTree(self, indent = 0):
        for i in range(indent):
            print("|\t", end="")
        print(self.op)
        self.val.printTree(indent + 1)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass
        # fill in the body


    # define printTree for other classes
    # ...


