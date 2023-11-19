
#TODO: wiele klas jest bardzo podobnych, pytanie czy można je połączyć czy takie rozróżnienie będzie potrzebne dalej
# (np. żeby sprawdzić czy coś jest rzeczywiście warunkiem zwracającym true/false a nie zwykłym obliczeniem

#TODO: Czy można tak ręcznie wypisywać np. VECTOR lub RETURN czy powinno być to robbione jakoś inaczej

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

class String(Node): # podobne do varaible
    def __init__(self, val):
        self.val = val

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

class Vector(Node):
    def __init__(self, val):
        self.val = val

class Values(Node):
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

class For(Node):
    def __init__(self, op, variable, for_range, program):
        self.op = op
        self.variable = variable
        self.for_range = for_range
        self.program = program

class Range(Node):
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Print(Node): # bardzo podobne do Vector, tylko Vector wypisuje na ekran VECTOR, a print PRINT
    def __init__(self, val):
        self.val = val

class KeyWords(Node):
    def __init__(self, key_word):
        self.key_word = key_word

class Return(Node): # analogicznie jak z Vector i Return
    def __init__(self, val):
        self.val = val

class While(Node):
    def __init__(self, cond, program):
        self.cond = cond
        self.program = program

class If(Node):
    def __init__(self, cond, program, else_program = None):
        self.cond = cond
        self.program = program
        self.else_program = else_program

class Cond(Node): # podobne do BinaryExpr, pytanie czy nie będzie potrzbne później (tak jak pisałem na górze)
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

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

    @addToClass(String)
    def printTree(self, indent = 0):
        print_indent(indent)
        print(self.val)

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

    @addToClass(Values)
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

    @addToClass(For)
    def printTree(self, indent = 0):
        print_indent(indent)
        print(self.op)
        self.variable.printTree(indent + 1)
        self.for_range.printTree(indent + 1)
        self.program.printTree(indent + 1)

    @addToClass(Range)
    def printTree(self, indent = 0):
        print_indent(indent)
        print("RANGE")
        self.start.printTree(indent + 1)
        self.end.printTree(indent + 1)


    @addToClass(Print)
    def printTree(self, indent = 0):
        print_indent(indent)
        print("PRINT")
        self.val.printTree(indent + 1)

    @addToClass(KeyWords)
    def printTree(self, indent = 0):
        print_indent(indent)
        print(self.key_word)

    @addToClass(Return)
    def printTree(self, indent = 0):
        print_indent(indent)
        print("RETURN")
        self.val.printTree(indent + 1)

    @addToClass(While)
    def printTree(self, indent = 0):
        print_indent(indent)
        print("WHILE")
        self.cond.printTree(indent + 1)
        self.program.printTree(indent + 1)

    @addToClass(If)
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

    @addToClass(Cond)
    def printTree(self, indent = 0):
        print_indent(indent)
        print(self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

def print_indent(indent):
    for i in range(indent):
        print("|\t", end="")