#!/usr/bin/python

from compiling_theory.lab1 import scanner
import ply.yacc as yacc

tokens = scanner.tokens

precedence = (
    # to fill ...
    ("nonassoc", 'IF'),
    ("nonassoc", 'ELSE'),
    ("nonassoc", 'EQ', 'NEQ', 'LT', 'GT', '<', '>'),
    ("left", '+', '-'),
    ("left", '*', '/'),
    ("left", 'DOTADD', 'DOTSUB'),
    ("left", 'DOTMUL', 'DOTDIV')
    # to fill ...
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
                | assign
                | cond_instruction
                | while_instruction
                | for_instruction
                | '{' program '}'
                | BREAK ';'
                | CONTINUE ';'
                | RETURN operation ';'
                | COMMENT"""


def p_value(p):
    """value : value ',' value
            | STRING
            | ID
            | operation"""

def p_assign(p):
    """assign : ID assign_operator operation ';'"""
    if p[2] == "=" : p[0] = p[3]
    elif p[2] == "+=" : p[0] = p[0] + p[3]
    elif p[2] == "-=" : p[0] = p[0] - p[3]
    elif p[2] == "*=" : p[0] = p[0] * p[2]
    elif p[2] == "/=" : p[0] = p[0] / p[2]

def p_assign_operators(p):
    """assign_operator : '='
                | ADDASSIGN
                | SUBASSIGN
                | MULASSIGN
                | DIVASSIGN"""

def p_number_operations(p):
    """operation : operation operator operation
                        | unit_operation"""
    if (len(p) == 2) : p[0] = p[1]
    elif p[2] == "+" : p[0] = p[1] + p[3]
    elif p[2] == "-" : p[0] = p[1] - p[3]
    elif p[2] == "*" : p[0] = p[1] * p[3]
    elif p[2] == "/" : p[0] = p[1] / p[3]
    elif p[2] == ".+" : p[0] = p[1] / p[3]
    elif p[2] == ".-" : p[0] = p[1] / p[3]
    elif p[2] == ".*" : p[0] = p[1] / p[3]
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
                        | '[' matrix_1 ']'"""

def p_fid(p):
    """fid : ZEROS
            | ONES
            | EYE"""

def p_matrix_1(p):
    """matrix_1 : '[' matrix_0 ']' ',' matrix_1
                | '[' matrix_0 ']'"""

def p_matrix_0(p):
    """matrix_0 : operation ',' matrix_0
                | operation"""

def p_cond_instruction(p):
    """cond_instruction : IF '(' condition ')' program_ins
                        | IF '(' condition ')' program_ins ELSE program_ins"""

def p_condition(p):
    """condition : operation comparison_operator operation
                | operation comparison_operator ID
                | ID comparison_operator operation
                | ID comparison_operator ID"""
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

# def p_instructions_opt_1(p):
#     """instructions_opt : instructions """
#
#
# def p_instructions_opt_2(p):
#     """instructions_opt : """
#
#
# def p_instructions_1(p):
#     """instructions : instructions instruction """
#
#
# def p_instructions_2(p):
#     """instructions : instruction """


# to finish the grammar
# ....


parser = yacc.yacc()

