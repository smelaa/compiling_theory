import sys
import os
sys.path.append(os.getcwd()+"/..")
from compiling_theory.compiler import Mparser, scanner

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "lab2/example1.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()
    parser.parse(text, lexer=scanner.lexer)
