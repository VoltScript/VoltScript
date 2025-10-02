#!/usr/bin/env python3

import sys
import os
from src.lexer import Lexer
from src.parser import Parser
from src.codegen import CodeGenerator

def compile_volt(input_file: str, output_file: str = None):
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    
    with open(input_file, 'r') as f:
        source_code = f.read()
    
    try:
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        codegen = CodeGenerator()
        cpp_code = codegen.generate(ast)
        
        if output_file is None:
            output_file = input_file.replace('.volt', '.cpp')
        
        with open(output_file, 'w') as f:
            f.write(cpp_code)
        
        print(f"Successfully compiled '{input_file}' to '{output_file}'")
        
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("VoltScript Compiler")
        print("Usage: python voltc.py <input.volt> [output.cpp]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    compile_volt(input_file, output_file)

if __name__ == "__main__":
    main()
