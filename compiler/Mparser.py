#!/usr/bin/python

import sys
import os
sys.path.append(os.getcwd()+"/..")
from compiling_theory.compiler import scanner, AST
import ply.yacc as yacc

tokens = scanner.tokens

precedence = (
    ("nonassoc", 'IFX'),
    ("nonassoc", 'ELSE'),
    ("left", "+", "-", "ADD"),
    ("left", "*", "/", "MUL"),
    ("nonassoc", "'", "UMINUS"),
)

def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
        exit()
    else:
        print("Unexpected end of input")

def p_program(p):
    """program : instructions_opt"""
    p[0] = p[1]

def p_instructions_opt(p):
    """instructions_opt : instructions
                        | empty"""
    p[0] = AST.Instructions(p[1])

def p_empty(p):
    """empty :"""
    p[0] = []


def p_instructions(p):
    """instructions : instructions program_ins
                    | program_ins"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_program_ins(p):
    """program_ins : PRINT print_value ';'
                | assign ';'
                | cond_instruction
                | while_instruction
                | for_instruction
                | '{' program '}'
                | BREAK ';'
                | CONTINUE ';'
                | RETURN operation ';'
                | COMMENT""" # jak dla mnie to to tu musi być, bo inaczej są błędy, na razie to tu zostawmy
    if p[1] == "break" or p[1] == "continue" : p[0] = AST.StatementList(AST.KeyWords(p[1]))
    elif len(p)==2 or len(p) == 3: p[0]=p[1]
    elif p[1] == "print": p[0] = AST.Print(p[2])
    elif p[1] == "return": p[0] = AST.Return(p[2])
    else: p[0] = p[2]

def p_print_value(p):
    """print_value : operation ',' print_value
            | operation"""
    if len(p) == 4: p[0] = AST.Values(p[1], p[3])
    else: p[0] = AST.Values(p[1])

def p_assign(p):
    """assign : id assign_operator operation
                | id '[' index ']' assign_operator operation"""
    if len(p) == 4 : p[0] = AST.Assign(p[2], p[1], p[3])
    else: p[0] = AST.RefAssign(p[5], p[1], p[3], p[6])

def p_assign_operator(p):
    """assign_operator : ADDASSIGN
                | SUBASSIGN
                | MULASSIGN
                | DIVASSIGN
                | '='"""
    p[0] = p[1]

def p_index(p):
    """index : INTNUM ',' index
            | INTNUM"""
    if len(p) == 4: p[0] = AST.Index(AST.IntNum(p[1]), p[3])
    else: p[0] = AST.Index(AST.IntNum(p[1]))

def p_vector(p):
    """vector : '[' vector_val ']'"""
    p[0] = AST.Vector(p[2])

def p_vector_val(p):
    """vector_val : operation ',' vector_val
                | operation"""
    if len(p) == 4 : p[0] = AST.Values(p[1], p[3])
    else: p[0] = AST.Values(p[1])

def p_operation(p):
    """operation : operation add_operator operation %prec ADD
                | operation mul_operator operation %prec MUL
                | '-' operation %prec UMINUS
                | operation "'" 
                | '(' operation ')'
                | id
                | INTNUM
                | FLOATNUM
                | fid '(' operation ')'
                | vector
                | string"""
    if len(p) == 5: p[0] = AST.Fid(p[1], p[3])
    elif len(p) == 4 and p[1] != '(' : p[0] = AST.BinExpr(p[2], p[1], p[3])
    elif len(p) == 4 : p[0] = p[2]
    elif len(p) == 3 and p[1] == '-': p[0] = AST.UnaryExpr(p[1], p[2])
    elif len(p) == 3: p[0] = AST.UnaryExpr(p[2], p[1])
    elif isinstance(p[1], int): p[0] = AST.IntNum(p[1])
    elif isinstance(p[1], float): p[0] = AST.FloatNum(p[1])
    else: p[0] = p[1]

def p_string(p):
    """string : STRING"""
    p[0] = AST.String(p[1])

def p_mul_operator(p):
    """mul_operator : '*'
                    | '/'
                    | DOTMUL
                    | DOTDIV"""
    p[0] = p[1]

def p_add_operator(p):
    """add_operator : '+'
                    | '-'
                    | DOTADD
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

def p_cond_instruction(p):
    """cond_instruction : IF '(' condition ')' program_ins %prec IFX
                        | IF '(' condition ')' program_ins ELSE program_ins"""
    if len(p) == 6: p[0] = AST.If(p[3], p[5])
    else: p[0] = AST.If(p[3], p[5], p[7])

def p_condition(p):
    """condition : operation comparison_operator operation"""
    p[0] = AST.Cond(p[2], p[1], p[3])

def p_comparison_operator(p):
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
    """range : operation ':' operation"""
    p[0] = AST.Range(p[1], p[3])

parser = yacc.yacc()

