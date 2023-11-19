
import sys
import os
sys.path.append(os.getcwd()+"/..")
import ply.yacc as yacc
from compiling_theory.lab2 import Mparser
from AST import TreePrinter


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "lab3/example1.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()
    ast = parser.parse(text, lexer=Mparser.scanner.lexer)
    ast.printTree()