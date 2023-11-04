#!/usr/bin/python

from compiling_theory.lab1 import scanner
import ply.yacc as yacc

tokens = scanner.tokens

precedence = (
    ("left", '+', '-'),
    ("left", '*', '/'),
    ("left", 'DOTADD', 'DOTSUB'),
    ("left", 'DOTMUL', 'DOTDIV'),
    ("nonassoc", 'IFX'),
    ("nonassoc", 'ELSE')
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")

def p_program(p):
    """program : program_ins program
                | program_ins"""

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


def p_value(p):
    """value : operation ',' value
            | operation"""

def p_assign(p):
    """assign : variable assign_operator operation"""
    if p[2] == "=" : p[0] = p[3]
    elif p[2] == "+=" : p[0] = p[0] + p[3]
    elif p[2] == "-=" : p[0] = p[0] - p[3]
    elif p[2] == "*=" : p[0] = p[0] * p[2]
    elif p[2] == "/=" : p[0] = p[0] / p[2]

def p_variable(p):
    """variable : ID
                | ID '[' index ']'"""

def p_index(p):
    """index : INTNUM
            | INTNUM ',' index"""

def p_assign_operators(p):
    """assign_operator : '='
                | ADDASSIGN
                | SUBASSIGN
                | MULASSIGN
                | DIVASSIGN"""

def p_number_operations(p):
    """operation : unit_operation operator operation
                        | unit_operation"""
    if (len(p) == 2) : p[0] = p[1]
    elif p[2] == "+" : p[0] = p[1] + p[3]
    elif p[2] == "-" : p[0] = p[1] - p[3]
    elif p[2] == "*" : p[0] = p[1] * p[3]
    elif p[2] == "/" : p[0] = p[1] / p[3]
    elif p[2] == ".+" : p[0] = p[1] + p[3]
    elif p[2] == ".-" : p[0] = p[1] - p[3]
    elif p[2] == ".*" : p[0] = p[1] * p[3]
    elif p[2] == "./" : p[0] = p[1] / p[3]

def p_operators(p):
    """operator : '+'
                | '-'
                | '*'
                | '/'
                | DOTADD
                | DOTSUB
                | DOTMUL
                | DOTDIV"""

def p_unit_operaions(p):
    """unit_operation : unit_operation "'"
                        | '-' unit_operation
                        | '(' operation ')'
                        | ID
                        | INTNUM
                        | FLOATNUM
                        | STRING
                        | fid '(' operation ')'
                        | '[' matrix ']'"""

def p_fid(p):
    """fid : ZEROS
            | ONES
            | EYE"""

def p_matrix(p):
    """matrix : operation ',' matrix
                | operation"""

def p_cond_instruction(p):
    """cond_instruction : IF '(' condition ')' program_ins %prec IFX
                        | IF '(' condition ')' program_ins ELSE program_ins"""

def p_condition(p):
    """condition : operation comparison_operator operation"""
    if p[2] == "==" : p[0] = p[1] == p[3]
    elif p[2] == "!=" : p[0] = p[1] != p[3]
    elif p[2] == "<" : p[0] = p[1] < p[3]
    elif p[2] == "<=" : p[0] = p[1] <= p[3]
    elif p[2] == ">" : p[0] = p[1] > p[3]
    elif p[2] == ">=" : p[0] = p[1] >= p[3]

def p_comparison_operators(p):
    """comparison_operator : EQ
                            | NEQ
                            | LT
                            | GT
                            | '<'
                            | '>'"""

def p_while_instruction(p):
    """while_instruction : WHILE '(' condition ')' program_ins"""

def p_for_instruction(p):
    """for_instruction : FOR ID '=' range program_ins"""

def p_range(p):
    """range : ID ':' ID
            | ID ':' INTNUM
            | INTNUM ':' ID
            | INTNUM ':' INTNUM"""

parser = yacc.yacc()

