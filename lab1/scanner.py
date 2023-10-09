import ply.lex as lex

reserved = ()

tokens = [
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'DOTADD',
    'DOTSUB',
    'DOTMUL',
    'DOTDIV',
    'ASSIGN',
    'ADDASSIGN',
    'SUBASSIGN',
    'MULASSIGN',
    'DIVASSIGN',
    'LE',
    'GE',
    'LT',
    'GT',
    'NEQ',
    'EQ',
    'LPARENCIR',
    'RPARENCIR',
    'LPARENSQ',
    'RPARENSQ',
    'LBRACE',
    'RBRACE',
    'NUMBER',
    'RANGE',
    'TRANSPOSE',
    'COMMA',
    'SEMICOLON',
]

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore = ' \t'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("line %d: illegal character '%s'" % (t.lineno, t.value[0]))
    t.lexer.skip(1)

lexer=lex.lex()
