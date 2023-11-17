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

    @addToClass(AST.String)
    def printTree(self, indent = 0):
        print_indent(indent)
        print(self.val)

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
        self.name.printTree(indent + 1)
        self.val.printTree(indent + 1)

    @addToClass(AST.UnaryExpr)
    def printTree(self, indent = 0):
        for i in range(indent):
            print("|\t", end="")
        print(self.op)
        self.val.printTree(indent + 1)

    @addToClass(AST.Vector)
    def printTree(self, indent = 0):
        for i in range(indent):
            print("|\t", end="")
        print("VECTOR")
        self.val.printTree(indent + 1)

    @addToClass(AST.Values)
    def printTree(self, indent = 0):
        self.val.printTree(indent)
        if self.next != None:
            self.next.printTree(indent)

    @addToClass(AST.RefAssign)
    def printTree(self, indent = 0):
        for i in range(indent):
            print("|\t", end="")
        print(self.op)
        print("|\tREF")
        self.name.printTree(indent + 2)
        self.index.printTree(indent + 2)
        self.val.printTree(indent + 1)

    @addToClass(AST.Index)
    def printTree(self, indent = 0):
        self.index1.printTree(indent)
        self.index2.printTree(indent)

    @addToClass(AST.Fid)
    def printTree(self, indent = 0):
        for i in range(indent):
            print("|\t", end="")
        print(self.fid)
        self.val.printTree(indent + 1)

    @addToClass(AST.For)
    def printTree(self, indent = 0):
        print_indent(indent)
        print(self.op)
        self.variable.printTree(indent + 1)
        self.for_range.printTree(indent + 1)
        self.program.printTree(indent + 1)

    @addToClass(AST.Range)
    def printTree(self, indent = 0):
        print_indent(indent)
        print("RANGE")
        self.start.printTree(indent + 1)
        self.end.printTree(indent + 1)

    @addToClass(AST.Print)
    def printTree(self, indent = 0):
        print_indent(indent)
        print("PRINT")
        self.val.printTree(indent + 1)

    @addToClass(AST.KeyWords)
    def printTree(self, indent = 0):
        print_indent(indent)
        print(self.key_word)

    @addToClass(AST.Return)
    def printTree(self, indent = 0):
        print_indent(indent)
        print("RETURN")
        self.val.printTree(indent + 1)

    @addToClass(AST.While)
    def printTree(self, indent = 0):
        print_indent(indent)
        print("WHILE")
        self.cond.printTree(indent + 1)
        self.program.printTree(indent + 1)

    @addToClass(AST.If)
    def printTree(self, indent = 0):
        print_indent(indent)
        print("IF")
        self.cond.printTree(indent + 1)
        print_indent(indent)
        print("THEN")
        self.program.printTree(indent + 1)
        if self.else_program != None:
            print_indent(indent)
            print("ELSE")
            self.else_program.printTree(indent + 1)

    @addToClass(AST.Cond)
    def printTree(self, indent = 0):
        print_indent(indent)
        print(self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)


    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass
        # fill in the body


def print_indent(indent):
    for i in range(indent):
        print("|\t", end="")