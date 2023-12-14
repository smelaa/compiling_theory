
import sys
import os
sys.path.append(os.getcwd()+"/..")
from compiling_theory.compiler import AST
from compiling_theory.compiler import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *

sys.setrecursionlimit(10000)

class Interpreter(object):

    def __init__(self):
        self.memory =  MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Instructions)
    def visit(self, node):
        for elem in node.instructions:
            self.visit(elem)

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = self.visit(node.left)
        r2 = self.visit(node.right)
        if isinstance(r1, str) and self.memory.contains(r1): # TODO co jest deklaracja, ale nie ma wartości
            r1 = self.memory.get(r1)
        if isinstance(r2, str) and self.memory.contains(r2):
            r2 = self.memory.get(r2)

        if node.op == '+': # TODO do zmiany, wersja prymitywna
            return r1 + r2
        elif node.op == '-':
            return r1 - r2
        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval

    @when(AST.Assign)
    def visit(self, node):
        name = self.visit(node.name)
        val = self.visit(node.val)
        print(name, val)
        if self.memory.contains(name):
            self.memory.set(name, val)
        else:
            self.memory.insert(name, val)

    @when(AST.Variable)
    def visit(self, node):
        return node.name

    @when(AST.IntNum)
    def visit(self, node):
        return node.val

    @when(AST.FloatNum)
    def visit(self, node):
        return node.val

    @when(AST.String)
    def visit(self, node):
        return node.val

    # simplistic while loop interpretation
    @when(AST.While)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            r = node.body.accept(self)
        return r


