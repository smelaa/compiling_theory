#!/usr/bin/python

from compiling_theory.lab1 import scanner
import ply.yacc as yacc

tokens = scanner.tokens

precedence = (
    ("nonassoc", 'IFX'),
    ("nonassoc", 'ELSE'),
    ("left", 'DOTADD', 'DOTSUB'),
    ("left", 'DOTMUL', 'DOTDIV'),
    ("left", '+', '-'),
    ("left", '*', '/')
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


def p_value(p): # TODO: zmienić wartości do drukowania
    """value : all_operations ',' value
            | all_operations"""

def p_assign(p):
    # """assign : variable assign_operator operation"""
    # TODO: pozmieniać if-else
    """assign : id_assign
                | matrix_assign"""
    if (len(p) == 4) : p[0] = p[3]
    else : p[0] = p[1]
    # if p[2] == "=" : p[0] = p[3]
    # elif p[2] == "+=" : p[0] = p[0] + p[3]
    # elif p[2] == "-=" : p[0] = p[0] - p[3]
    # elif p[2] == "*=" : p[0] = p[0] * p[2]
    # elif p[2] == "/=" : p[0] = p[0] / p[2]

def p_id_assign(p):
    """id_assign : ID '=' all_operations
                | ID assign_operator operation"""

def p_all_operations(p):
    """all_operations : operation
                    | STRING"""

def p_matrix_assign(p):
    """matrix_assign : ID '[' index ']' assign_operator operation
                    | ID '[' index ']' '=' operation"""

# def p_numeric_assign(p):
    # """numeric_assign : variable numeric_assign_operator numeric_operation"""
    # if p[2] == "=" : p[0] = p[3]
    # elif p[2] == "+=" : p[0] = p[0] + p[3]
    # elif p[2] == "-=" : p[0] = p[0] - p[3]
    # elif p[2] == "*=" : p[0] = p[0] * p[2]
    # elif p[2] == "/=" : p[0] = p[0] / p[2]


# def p_variable(p):
#     """variable : ID
#                 | ID '[' index ']'"""

def p_index(p):
    """index : INTNUM
            | INTNUM ',' index"""

def p_assign_operator(p):
    """assign_operator : ADDASSIGN
                | SUBASSIGN
                | MULASSIGN
                | DIVASSIGN"""

# def p_assign_operators(p):
#     """assign_operator : '='
#                 | ADDASSIGN
#                 | SUBASSIGN
#                 | MULASSIGN
#                 | DIVASSIGN"""

def p_numeric_operations(p):
    """numeric_operation : numeric_operation numeric_operator numeric_operation
                            | '-' numeric_operation
                            | '(' numeric_operation ')'
                            | ID
                            | INTNUM
                            | FLOATNUM"""
    if (len(p) == 2) : p[0] = p[1]
    # elif p[1] == '-' : p[0] = 0 - p[2]
    elif p[2] == "+" : p[0] = p[1] + p[3]
    elif p[2] == "-" : p[0] = p[1] - p[3]
    elif p[2] == "*" : p[0] = p[1] * p[3]
    elif p[2] == "/" : p[0] = p[1] / p[3]


def p_numeric_operator(p):
    """numeric_operator : '+'
                | '-'
                | '*'
                | '/'"""

# def p_matrix_assign(p):
#     """matrix_assign : variable '=' matrix_operation"""
#     p[0] = p[3]

def p_matrix_operation(p):
    """matrix_operation : matrix_operation matrix_operator matrix_operation
                        | matrix_operation "'"
                        | '(' matrix_operation ')'
                        | ID
                        | fid '(' numeric_operation ')'
                        | '[' matrix ']'"""

def p_matrix_operator(p):
    """matrix_operator : DOTADD
                     | DOTSUB
                     | DOTMUL
                     | DOTDIV"""

def p_operation(p):
    """operation : numeric_operation
                | matrix_operation"""
    p[0] = p[1]
    # if (len(p) == 2) : p[0] = p[1]
    # elif p[2] == "+" : p[0] = p[1] + p[3]
    # elif p[2] == "-" : p[0] = p[1] - p[3]
    # elif p[2] == "*" : p[0] = p[1] * p[3]
    # elif p[2] == "/" : p[0] = p[1] / p[3]
    # elif p[2] == ".+" : p[0] = p[1] + p[3]
    # elif p[2] == ".-" : p[0] = p[1] - p[3]
    # elif p[2] == ".*" : p[0] = p[1] * p[3]
    # elif p[2] == "./" : p[0] = p[1] / p[3]

# def p_operators(p):
#     """operator : '+'
#                 | '-'
#                 | '*'
#                 | '/'
#                 | DOTADD
#                 | DOTSUB
#                 | DOTMUL
#                 | DOTDIV"""

# def p_unit_operaions(p):
#     """unit_operation : unit_operation "'" -> matrix
#                         | '-' unit_operation -> numeric
#                         | '(' operation ')' -> numeric, matrix
#                         | ID -> numeric, matrix
#                         | INTNUM -> numeric
#                         | FLOATNUM -> numeric
#                         | STRING -> other
#                         | fid '(' operation ')' -> matrix(numeric)
#                         | '[' matrix ']' -> matrix"""

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
    """range : numeric_operation ':' numeric_operation"""

parser = yacc.yacc()


#TODO : czy w () można dawać tez macierze i string

