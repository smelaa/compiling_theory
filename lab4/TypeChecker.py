#!/usr/bin/python
from compiling_theory.AST import Node

class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, Node):
                            self.visit(item)
                elif isinstance(child, Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    #def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)

    def print_error(self, lineno, msg):
        print(f'Error on line {lineno}: {msg}')


class TypeChecker(NodeVisitor):
    matrix_ops = ['.+', '.-', '.*', './']
    scalar_ops = ['+', '-', '*', '/', '<', '>', '==', '>=', '<=']
    numeric_types = ['int', 'float']

    ops_with_ret_type = {
        '+': {
            ('int', 'int'): 'int',
            ('int', 'float'): 'float',
            ('float', 'int'): 'float',
            ('float', 'float'): 'float',
            ('str', 'str'): 'str',
        },
        '-': {
            ('int', 'int'): 'int',
            ('int', 'float'): 'float',
            ('float', 'int'): 'float',
            ('float', 'float'): 'float',
        },
        '*': {
            ('int', 'int'): 'int',
            ('int', 'float'): 'float',
            ('float', 'int'): 'float',
            ('float', 'float'): 'float',
            ('str', 'int'): 'str',
            ('int', 'str'): 'str'
        },
        '/': {
            ('int', 'int'): 'float',
            ('int', 'float'): 'float',
            ('float', 'int'): 'float',
            ('float', 'float'): 'float',
        },
        '>': {
            ('int', 'int'): 'boolean',
            ('int', 'float'): 'boolean',
            ('float', 'int'): 'boolean',
            ('float', 'float'): 'boolean',
        },
        '<': {
            ('int', 'int'): 'boolean',
            ('int', 'float'): 'boolean',
            ('float', 'int'): 'boolean',
            ('float', 'float'): 'boolean',
        },

        '<=': {
            ('int', 'int'): 'boolean',
            ('int', 'float'): 'boolean',
            ('float', 'int'): 'boolean',
            ('float', 'float'): 'boolean',
        },
        '>=': {
            ('int', 'int'): 'boolean',
            ('int', 'float'): 'boolean',
            ('float', 'int'): 'boolean',
            ('float', 'float'): 'boolean',
        },
        '==': {
            ('int', 'int'): 'boolean',
            ('int', 'float'): 'boolean',
            ('float', 'int'): 'boolean',
            ('float', 'float'): 'boolean',
        },
        '!=': {
            ('int', 'int'): 'boolean',
            ('int', 'float'): 'boolean',
            ('float', 'int'): 'boolean',
            ('float', 'float'): 'boolean',
        },
        '.+': {
            ('matrix', 'matrix'): 'matrix',
        },
        '.-': {
            ('matrix', 'matrix'): 'matrix',
        },
        '.*': {
            ('matrix', 'matrix'): 'matrix',
        },
        './': {
            ('matrix', 'matrix'): 'matrix',
        },
    }

    def visit_BinExpr(self, node): #TODO
                                          # alternative usage,
                                          # requires definition of accept method in class Node
        type1 = self.visit(node.left)     # type1 = node.left.accept(self) 
        type2 = self.visit(node.right)    # type2 = node.right.accept(self)
        op    = node.op

        if type1 == 'matrix' and type2 !='matrix' or type1 !='matrix' and type2 =='matrix':
            self.print_error(node.lineno, f"Operations between {type1} and {type2} cannot be performed") 
            return 'unknown'
        elif type1 == 'matrix' and type2 == 'matrix':
            if op not in self.matrix_ops:
                self.print_error(node.lineno, f"{op} does not support matrix operations") 
                return 'unknown'
            #TODO: sprawdz wymiary
        elif (type1, type2) in self.ops_with_ret_type[op]:
            if op not in self.scalar_ops:
                self.print_error(node.lineno, f"{op} does not support scalar operations") 
                return 'unknown'
            return self.ops_with_ret_type[op][(type1, type2)]
        self.print_error(node.lineno, f"Cannot perform {op} on {(type1, type2)}, incompatible types") 
        return 'unknown' 

    def visit_IntNum(self, node):
        return 'int'

    def visit_FloatNum(self, node):
        return 'float'

    def visit_Variable(self, node):
        name=node.name

        var = self.current_scope.get(name)
        if var is None:
            self.print_error(node.lineno, "Variable referenced before assignment")
            return 'unknown'
        
        return var.type


    def visit_String(self, node):
        return 'str'

    def visit_Assign(self, node):
        pass

    def visit_UnaryExpr(self, node):
        pass

    def visit_Vector(self, node):
        #return 'matrix'  and shape
        pass

    def visit_Values(self, node):
        pass

    def visit_RefAssign(self, node):
        pass

    def visit_Index(self, node):
        pass

    def visit_Fid(self, node):
        pass

    def visit_For(self, node):
        pass

    def visit_Range(self, node):
        pass

    def visit_Print(self, node):
        pass

    def visit_Range(self, node):
        pass

    def visit_KeyWords(self, node):
        pass

    def visit_Return(self, node):
        pass

    def visit_While(self, node):
        pass

    def visit_If(self, node):
        pass

    def visit_Cond(self, node):
        pass