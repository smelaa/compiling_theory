#!/usr/bin/python

class Symbol:
    def __init__(self, name, type, elem_type = None, shape = None):
        self.name = name
        self.type = type
        self.elem_type = elem_type
        self.shape = shape

#
class VariableSymbol(Symbol):

    def __init__(self, name, type):
        self.name = name
        self.type = type



class SymbolTable(object):

    def __init__(self, parent, name): # parent scope and symbol table name
        self.parent_scope=parent
        self.name=name
        self.symbols = dict()

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.symbols[name]=symbol

    def get(self, name): # get variable symbol or fundef from <name> entry
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent_scope is not None:
            return self.parent_scope.get(name)
        return None

    def getParentScope(self):
        return self.parent_scope

    def pushScope(self, name):
        return SymbolTable(self, name)

    def popScope(self):
        return self.getParentScope()


