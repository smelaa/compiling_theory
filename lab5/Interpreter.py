
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
        # if isinstance(r1, str) and self.memory.contains(r1): # TODO co jest deklaracja, ale nie ma wartości
        #     r1 = self.memory.get(r1)
        # if isinstance(r2, str) and self.memory.contains(r2):
        #     r2 = self.memory.get(r2)

        if node.op == '+': # TODO do zmiany, wersja prymitywna
            return r1 + r2
        elif node.op == '-':
            return r1 - r2
        elif node.op == '*':
            return r1 * r2
        elif node.op == '/':
            return r1 / r2
        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval

    @when(AST.Assign)
    def visit(self, node):
        val = self.visit(node.val)
        if isinstance(node.name, AST.RefVar):
            name = node.name.name.name
            indexes = self.visit(node.name.index)
            curr_val = self.visit(node.name.name)
            curr_val = self.ref_assign(curr_val, indexes, val)
            self.memory.set(name, curr_val)
            # print(name, curr_val)
        else:
            name = node.name.name
            # print(name, val)
            if self.memory.contains(name):
                self.memory.set(name, val)
            else:
                self.memory.insert(name, val)

    def ref_assign(self, curr_val, indexes, val):
        if len(indexes) == 0:
            return val
        curr_val[indexes[0]] = self.ref_assign(curr_val[indexes[0]], indexes[1:], val)
        return curr_val

    @when(AST.Variable)
    def visit(self, node):
        if self.memory.contains(node.name):
            return self.memory.get(node.name)
        return node.name

    @when(AST.IntNum)
    def visit(self, node):
        return node.val

    @when(AST.FloatNum)
    def visit(self, node):
        return node.val

    @when(AST.String)
    def visit(self, node):
        return node.val[1:-1]

    @when(AST.UnaryExpr)
    def visit(self, node):
        val = self.visit(node.val)
        if node.op == '-':
            if isinstance(val, str) and self.memory.contains(val):
                val = self.memory.get(val)
            return - val
        else:
            #TODO transpozycja macierzy
            return val

    @when(AST.Vector)
    def visit(self, node):
        val = self.visit(node.val)
        return val

    @when(AST.Values)
    def visit(self, node):
        values = [self.visit(node.val)]
        if node.next != None:
            values += self.visit(node.next)
        return values

    @when(AST.RefVar)
    def visit(self, node):
        name = self.visit(node.name)
        indexes = self.visit(node.index)
        val = self.memory.get(name)
        for i in range(len(indexes)):
            val = val[indexes[i]]
        return val

    @when(AST.Index)
    def visit(self, node):
        indexes = [self.visit(node.index1)]
        if node.next != None:
            indexes += self.visit(node.next)
        return indexes

    @when(AST.Fid)
    def visit(self, node):
        val = self.visit(node.val)
        if node.fid == 'zeros':
            return [[0 for _ in range(val)] for _ in range(val)]
        if node.fid == 'ones':
            return [[1 for _ in range(val)] for _ in range(val)]
        res = [[0 for _ in range(val)] for _ in range(val)]
        for i in range(val):
            res[i][i] = 1
        return res

    @when(AST.For)
    def visit(self, node):
        self.memory.push(Memory())
        var = node.variable.name
        self.memory.insert(var, 0)
        start, end = self.visit(node.for_range)
        for i in range(start, end):
            self.memory.set(var, i)
            self.visit(node.program)
        self.memory.pop()

    @when(AST.Range)
    def visit(self, node):
        start = self.visit(node.start)
        end = self.visit(node.end)
        return start, end

    @when(AST.Print)
    def visit(self, node):
        self.visit(node.val)

    @when(AST.PrintValues)
    def visit(self, node):
        print(self.visit(node.val))
        if node.next != None:
            self.visit(node.next)

    # simplistic while loop interpretation
    @when(AST.While)
    def visit(self, node):
        self.memory.push(Memory())
        while self.visit(node.cond): # Kuta coś tu zwraca, nie wiem po co
            self.visit(node.program)
        self.memory.pop()

    @when(AST.If)
    def visit(self, node):
        self.memory.push(Memory)
        if self.visit(node.cond):
            self.visit(node.program)
        elif node.else_program != None:
            self.visit(node.else_program)

    @when(AST.Cond)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if node.op == '==':
            return left == right
        elif node.op == '<':
            return left < right
        elif node.op == '<=':
            return left <= right
        elif node.op == '>':
            return left > right
        elif node.op == '>=':
            return left >= right


