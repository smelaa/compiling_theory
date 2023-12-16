# !/usr/bin/python
from compiling_theory.compiler import AST
from compiling_theory.compiler.SymbolTable import SymbolTable, Symbol


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)

    def print_error(self, lineno, msg):
        print(f'Error on line {lineno}: {msg}')


class TypeChecker(NodeVisitor):
    matrix_ops = ['.+', '.-', '.*', './', '==', '!=']
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
        '.+': {
            ('vector', 'vector'): 'vector',
        },
        '.-': {
            ('vector', 'vector'): 'vector',
        },
        '.*': {
            ('vector', 'vector'): 'vector',
        },
        './': {
            ('vector', 'vector'): 'vector',
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
            ('vector', 'vector'): 'boolean',
            ('str', 'str'): 'boolean',
        },
        '!=': {
            ('int', 'int'): 'boolean',
            ('int', 'float'): 'boolean',
            ('float', 'int'): 'boolean',
            ('float', 'float'): 'boolean',
            ('vector', 'vector'): 'boolean',
            ('str', 'str'): 'boolean',
        },
    }

    ops_cond = {
        '>': {
            ('int', 'int'),
            ('int', 'float'),
            ('float', 'int'),
            ('float', 'float'),
        },
        '<': {
            ('int', 'int'),
            ('int', 'float'),
            ('float', 'int'),
            ('float', 'float'),
        },

        '<=': {
            ('int', 'int'),
            ('int', 'float'),
            ('float', 'int'),
            ('float', 'float'),
        },
        '>=': {
            ('int', 'int'),
            ('int', 'float'),
            ('float', 'int'),
            ('float', 'float'),
        },
        '==': {
            ('int', 'int'),
            ('int', 'float'),
            ('float', 'int'),
            ('float', 'float'),
            ('vector', 'vector'),
            ('str', 'str'),
        },
        '!=': {
            ('int', 'int'),
            ('int', 'float'),
            ('float', 'int'),
            ('float', 'float'),
            ('vector', 'vector'),
            ('str', 'str'),
        },
    }

    def __init__(self):
        super().__init__()
        self.current_scope = SymbolTable(None, 'program')

    def visit_Instructions(self, node):
        for elem in node.instructions:
            self.visit(elem)

    def visit_BinExpr(self, node):
        val1 = self.visit(node.left)
        val2 = self.visit(node.right)  
        op = node.op

        if val1.type == 'vector' and val2.type != 'vector' or val1.type != 'vector' and val2.type == 'vector':
            self.print_error(node.lineno, f"Operations between {val1.type} and {val2.type} cannot be performed")
            return Symbol('', 'unknown')
        elif val1.type == 'vector' and val2.type == 'vector':
            if op not in self.matrix_ops:
                self.print_error(node.lineno, f"{op} does not support matrix operations")
                Symbol('', 'unknown')
            if val1.shape != val2.shape:
                self.print_error(node.lineno, f"Matrix must be the same shape (got {val1.shape}, {val2.shape})")
                Symbol('', 'unknown')
            elem_type = val1.elem_type
            if node.op[1] == '/':
                elem_type = 'float'
            return Symbol('', self.ops_with_ret_type[op][(val1.type, val2.type)], elem_type, val1.shape)
        elif (val1.type, val2.type) in self.ops_with_ret_type[op]:
            if op not in self.scalar_ops:
                self.print_error(node.lineno, f"{op} does not support scalar operations")
                return Symbol('', 'unknown')
            return Symbol('', self.ops_with_ret_type[op][(val1.type, val2.type)])
        self.print_error(node.lineno, f"Cannot perform {op} on {(val1.type, val2.type)}, incompatible types")
        return Symbol('', 'unknown')

    def visit_IntNum(self, node):
        return Symbol('', 'int')

    def visit_FloatNum(self, node):
        return Symbol('', 'float')

    def visit_Variable(self, node):
        name = node.name

        var = self.current_scope.get(name)
        if var is None:
            self.print_error(node.lineno, "Variable referenced before assignment")
            return Symbol('', 'unknown')

        return var

    def visit_String(self, node):
        return Symbol('', 'string')

    def visit_Assign(self, node):
        if node.op != '=':
            expr = AST.BinExpr(node.op[0], node.name, node.val)
            self.visit(AST.Assign('=', node.name, expr))
        else:
            val = self.visit(node.val)
            if val.type == 'unknown':
                return

            if isinstance(node.name, AST.RefVar):
                curr = self.visit(node.name)
                if curr.type == 'unknown':
                    return
                if curr.shape != val.shape:
                    self.print_error(node.lineno, f"Wrong shape ({curr.shape}, {val.shape})")
                if curr.elem_type != val.elem_type:
                    self.print_error(node.lineno,
                        f"Variable types are static. Cannot assign {val.type} to variable of type {curr.type}")
                name = node.name.name.name
            else:
                curr = self.current_scope.get(node.name.name)
                name = node.name.name
            if curr != None:
                if curr.type != val.type:
                    self.print_error(node.lineno,
                                     f"Variable types are static. Cannot assign {val.type} to variable of type {curr.type}")
                else:
                    self.current_scope.put(name, val)
            else:
                if val.type != 'unknown':
                    self.current_scope.put(name, val)

    def visit_UnaryExpr(self, node):
        if node.op == "'":
            val = self.visit(node.val)
            if val.type != 'vector':
                self.print_error(node.lineno, f"Only matrices can be transposed")
                return Symbol('', 'unknown')
            else:
                return Symbol('', 'vector', val.elem_type, reversed(val.shape))
        else:  # node.op=='-'
            val = self.visit(node.val)
            if val.type != 'vector' and val.type not in self.numeric_types:
                self.print_error(node.lineno, f"Only numeric types and matrices can be negated.")
                return Symbol('', 'unknown')
            else:
                return val

    def visit_Vector(self, node):
        return self.visit(node.val)

    def visit_Values(self, node):
        val = self.visit(node.val)
        if val.shape != None:
            elem_type = val.elem_type
            elem_shape = val.shape
            shape = [1] + elem_shape
        else:
            if val.type not in self.numeric_types:
                self.print_error(node.lineno, f"Only numeric types can be vector element")
                return Symbol('', 'unknown')
            elem_type = val.type
            shape = [1]

        if node.next != None:
            next_val = self.visit(node.next)

            if next_val.type == 'unknown':
                return next_val

            if val.shape != None and next_val.shape != None and val.shape != next_val.shape[1:]:
                self.print_error(node.lineno, f"Wrong shape ({next_val.shape[1:]}, {val.shape})")
                return Symbol('', 'unknown')

            if elem_type != next_val.elem_type:
                self.print_error(node.lineno, f"Wrong type ({next_val.elem_type}, {elem_type})")
                return Symbol('', 'unknown')

            shape[0] += next_val.shape[0]
        return Symbol('', 'vector', elem_type, shape)

    def visit_RefVar(self, node):
        vector = self.current_scope.get(node.name.name)
        if vector == None:
            self.print_error(node.lineno, "Variable referenced before assignment")
            return Symbol('', 'unknown')

        index = self.visit(node.index)
        if index.type == 'unknown':
            return index
        if len(vector.shape) < len(index.shape):
            self.print_error(node.lineno, f"To many index (vector shape: {vector.shape}, index: {index.shape})")
            return Symbol('', 'unknown')
        for i in range(len(index.shape)):
            if vector.shape[i] <= index.shape[i]:
                self.print_error(node.lineno,
                                 f"Index out of range (vector shape: {vector.shape}, index: {index.shape})")
                return Symbol('', 'unknown')
        if len(vector.shape) == len(index.shape):
            return Symbol('', vector.elem_type)
        return Symbol('', 'vector', vector.elem_type, vector.shape[len(index.shape):])

    def visit_Index(self, node):
        index = self.visit(node.index1)
        if index.type != 'int':
            self.print_error(node.lineno, f"Indexes must be int (got {index.type})")
            return Symbol('', 'unknown')
        if node.index1.val < 0:
            self.print_error(node.lineno, f"Indexes cannot be negativ (got {node.index1.val})")
            return Symbol('', 'unknown')
        all_index = [node.index1.val]
        if node.next != None:
            next_index = self.visit(node.next)
            if next_index.type == 'unknown':
                return next_index
            all_index += next_index.shape
        return Symbol('', 'ref', None, all_index)

    def visit_Fid(self, node):
        type = self.visit(node.val).type
        if type != 'int':
            self.print_error(node.lineno, f"Parameter of {node.fid} must be integer")
            return Symbol('', 'unknown')
        return Symbol('', 'vector', 'int', [node.val.val, node.val.val])

    def visit_For(self, node):
        self.current_scope = self.current_scope.pushScope('for')
        self.visit(node.for_range)
        symbol = Symbol(node.variable.name, 'int')
        self.current_scope.put(node.variable.name, symbol)
        self.visit(node.program)
        self.current_scope = self.current_scope.popScope()

    def visit_Range(self, node):
        start = self.visit(node.start)
        end = self.visit(node.end)

        if start.type != 'int' or end.type != 'int':
            self.print_error(node.lineno, f"Range operator accepts (int, int), got {(start.type, end.type)}")

    def visit_Print(self, node):
        self.visit(node.val)

    def visit_PrintValues(self, node):
        self.visit(node.val)
        if node.next != None:
            self.visit(node.next)

    def visit_KeyWords(self, node):
        scope = self.current_scope
        while scope and scope.name not in ['while', 'for']:
            scope = scope.getParentScope()
        if scope is None:
            self.print_error(node.lineno, f"{node.key_word} out of loop scope")

    def visit_Return(self, node):
        self.visit(node.val)

    def visit_While(self, node):
        self.current_scope = self.current_scope.pushScope('while')
        self.visit(node.cond)
        self.visit(node.program)
        self.current_scope = self.current_scope.popScope()

    def visit_If(self, node):
        self.current_scope = self.current_scope.pushScope('if')
        self.visit(node.cond)
        self.visit(node.program)
        self.current_scope = self.current_scope.popScope()
        if node.else_program is not None:
            self.current_scope = self.current_scope.pushScope('else')
            self.visit(node.else_program)
            self.current_scope = self.current_scope.popScope()

    def visit_Cond(self, node):
        val1 = self.visit(node.left)
        val2 = self.visit(node.right)
        op = node.op

        if not (val1.type, val2.type) in self.ops_cond[op]:
            self.print_error(node.lineno, f"{op} does not support {(val1.type, val2.type)}")
