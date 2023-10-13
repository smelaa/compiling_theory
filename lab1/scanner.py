import ply.lex as lex

reserved = ()

tokens = [
    # 'PLUS',
    # 'MINUS',
    # 'TIMES',
    # 'DIVIDE',
    'DOTADD',
    'DOTSUB',
    'DOTMUL',
    'DOTDIV',
    # 'ASSIGN',
    'ADDASSIGN',
    'SUBASSIGN',
    'MULASSIGN',
    'DIVASSIGN',
    # 'LE',
    # 'GE',
    'LT',
    'GT',
    'NEQ',
    'EQ',
    # 'LPARENCIR',
    # 'RPARENCIR',
    # 'LPARENSQ',
    # 'RPARENSQ',
    # 'LBRACE',
    # 'RBRACE',
    'ID',
    'INTNUM',
    # 'RANGE',
    # 'TRANSPOSE',
    # 'COMMA',
    # 'SEMICOLON',
    'FLOATNUM',
    'STRING',
    'COMMENT'
]

# t_PLUS = r'\+'
# t_MINUS = r'-'
# t_TIMES = r'\*'
# t_DIVIDE = r'/'
# t_LPAREN = r'\('
# t_RPAREN = r'\)'
t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\.\/'
t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'\/='
t_LT = r'<='
t_GT = r'>='
t_NEQ = r'!='
t_EQ = r'=='

t_ignore = ' \t'

literals = "+-*/=<>()[]{}',;"

def t_ID(t):
    r'[a-zA-Z_]\w*'
    return t

def t_FLOATNUM(t): # zamieniając kolejność z t_INTNUM już nie działa -> do sprawdzenia
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'".*"'
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("line %d: illegal character '%s'" % (t.lineno, t.value[0]))
    t.lexer.skip(1)

lexer=lex.lex()
