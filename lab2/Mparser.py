#!/usr/bin/python

#TODO: poukładać jakoś te if-elif w dłuższych instrukcjach i jeszcze to przepatrzeć

from compiling_theory.lab1 import scanner
from compiling_theory.lab3 import AST
import ply.yacc as yacc

tokens = scanner.tokens

precedence = (
    ("nonassoc", 'IFX'),
    ("nonassoc", 'ELSE'),
    ("left", 'MATRIX_ADD'),
    ("left", 'MATRIX_MUL'),
    ("nonassoc", "'"),
    ("left", '+', '-'),
    ("left", '*', '/'),
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
        exit()
    else:
        print("Unexpected end of input")

def p_program(p):
    """program : program_ins program
                | program_ins"""
    if len(p) == 2 : p[0] = p[1]
    else: p[0] = AST.Start(p[1], p[2])

def p_program_instrucitons(p):
    """program_ins : PRINT value ';'
                | assign ';'
                | cond_instruction
                | while_instruction
                | for_instruction
                | '{' program '}'
                | BREAK ';'
                | CONTINUE ';'
                | RETURN operation ';'
                | COMMENT"""
    if p[1] == "break" or p[1] == "continue" : p[0] = AST.KeyWords(p[1])
    elif len(p)==2 or len(p) == 3: p[0]=p[1]
    elif p[1] == "print": p[0] = AST.Print(p[2])
    elif p[1] == "return": p[0] = AST.Return(p[2])
    else: p[0] = p[2]

def p_value(p):
    """value : all_operations ',' value
            | all_operations"""
    if len(p) == 4: p[0] = AST.Values(p[1], p[3])
    else: p[0] = AST.Values(p[1])

def p_assign(p):
    """assign : id_assign
                | matrix_assign"""
    p[0] = p[1]


def p_id_assign(p):
    """id_assign : id '=' all_operations
                | id assign_operator operation"""
    p[0] = AST.Assign(p[2], p[1], p[3])

def p_all_operations(p):
    """all_operations : operation
                    | string"""
    p[0] = p[1]

def p_string(p):
    """string : STRING"""
    p[0] = AST.String(p[1])

def p_assign_operator(p):
    """assign_operator : ADDASSIGN
                | SUBASSIGN
                | MULASSIGN
                | DIVASSIGN"""
    p[0] = p[1]
def p_operation(p):
    """operation : numeric_operation
                | matrix_operation"""
    p[0] = p[1]

def p_matrix_assign(p):
    """matrix_assign : id '[' multiple_index ']' '=' numeric_operation
                    | id '[' multiple_index ']' assign_operator numeric_operation
                    | id '[' single_index ']' '=' vector"""
    p[0] = AST.RefAssign(p[5], p[1], p[3], p[6])

def p_multiple_index(p):
    """multiple_index : INTNUM ',' INTNUM"""
    p[0] = AST.Index(AST.IntNum(p[1]), AST.IntNum(p[3]))

def p_single_index(p):
    """single_index : INTNUM"""
    p[0] = AST.IntNum(p[1])

def p_vector(p):
    """vector : '[' vector_val ']'"""
    p[0] = AST.Vector(p[2])

def p_vector_val(p):
    """vector_val : numeric_operation ',' vector_val
                | numeric_operation"""
    if len(p) == 4 : p[0] = AST.Values(p[1], p[3])
    else: p[0] = AST.Values(p[1])

def p_numeric_operations(p):
    """numeric_operation : numeric_operation '+' numeric_operation
                            | numeric_operation '-' numeric_operation
                            | numeric_operation '*' numeric_operation
                            | numeric_operation '/' numeric_operation
                            | '-' numeric_operation
                            | '(' numeric_operation ')'
                            | id
                            | INTNUM
                            | FLOATNUM"""
    if len(p) == 4 and p[1] != '(' : p[0] = AST.BinExpr(p[2], p[1], p[3])
    elif len(p) == 4 : p[0] = p[2]
    elif len(p) == 3 : p[0] = AST.UnaryExpr(p[1], p[2])
    elif isinstance(p[1], int): p[0] = AST.IntNum(p[1])
    elif isinstance(p[1], float): p[0] = AST.FloatNum(p[1])
    else: p[0] = p[1]

def p_matrix_operation(p):
    """matrix_operation : matrix_operation matrix_operator_mul matrix_operation %prec MATRIX_MUL
                        | matrix_operation matrix_operator_add matrix_operation %prec MATRIX_ADD
                        | matrix_operation "'"
                        | '(' matrix_operation ')'
                        | id_form
                        | fid '(' numeric_operation ')'
                        | '[' matrix ']'"""
    if len(p) == 5:
        p[0] = AST.UnaryExpr(p[1], p[3])
    elif len(p) == 4 and p[1] != '(' and p[1] != '[':
        p[0] = AST.BinExpr(p[2], p[1], p[3])
    elif len(p) == 4 and p[1] == '(':
        p[0] = p[2]
    elif len(p) == 4:
        p[0] = AST.Vector(p[2])
    elif len(p) == 3:
        p[0] = AST.UnaryExpr(p[2], p[1])
    else: p[0] = p[1]
def p_id_form(p):
    """id_form : id "'"
                | id matrix_operator_mul matrix_operation %prec MATRIX_MUL
                | matrix_operation matrix_operator_mul id %prec MATRIX_MUL
                | id matrix_operator_mul id %prec MATRIX_MUL
                | id matrix_operator_add matrix_operation %prec MATRIX_ADD
                | matrix_operation matrix_operator_add id %prec MATRIX_ADD
                | id matrix_operator_add id %prec MATRIX_ADD"""
    if len(p) == 4:
        p[0] = AST.BinExpr(p[2], p[1], p[3])
    else: p[0] = AST.UnaryExpr(p[2], p[1])

def p_matrix_mul(p):
    """matrix_operator_mul : DOTMUL
        | DOTDIV"""
    p[0] = p[1]

def p_matrix_add(p):
    """matrix_operator_add : DOTADD
        | DOTSUB"""
    p[0] = p[1]

def p_id(p):
    """id : ID"""
    p[0] = AST.Variable(p[1])

def p_fid(p):
    """fid : ZEROS
            | ONES
            | EYE"""
    p[0] = p[1]

def p_matrix(p):
    """matrix : vector ',' matrix
                | vector"""
    if len(p) == 4: p[0] = AST.Values(p[1], p[3])
    else: p[0] = AST.Values(p[1])


def p_cond_instruction(p):
    """cond_instruction : IF '(' condition ')' program_ins %prec IFX
                        | IF '(' condition ')' program_ins ELSE program_ins"""
    if len(p) == 6: p[0] = AST.If(p[3], p[5])
    else: p[0] = AST.If(p[3], p[5], p[7])

def p_condition(p):
    """condition : operation comparison_operator operation"""
    p[0] = AST.Cond(p[2], p[1], p[3])

def p_comparison_operators(p):
    """comparison_operator : EQ
                            | NEQ
                            | LT
                            | GT
                            | '<'
                            | '>'"""
    p[0] = p[1]

def p_while_instruction(p):
    """while_instruction : WHILE '(' condition ')' program_ins"""
    p[0] = AST.While(p[3], p[5])

def p_for_instruction(p):
    """for_instruction : FOR id '=' range program_ins"""
    p[0] = AST.For(p[1], p[2], p[4], p[5])

def p_range(p):
    """range : numeric_operation ':' numeric_operation"""
    p[0] = AST.Range(p[1], p[3])

parser = yacc.yacc()

