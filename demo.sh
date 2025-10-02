#!/bin/bash

echo "=========================================="
echo "VoltScript Compiler Demo"
echo "=========================================="
echo ""

echo "Compiling examples/hello.volt..."
python voltc.py examples/hello.volt
echo ""

echo "Generated C++ code:"
cat examples/hello.cpp
echo ""

echo "Compiling C++ and running..."
g++ examples/hello.cpp -o examples/hello
./examples/hello
echo ""

echo "=========================================="
echo "Try compiling your own VoltScript files:"
echo "  python voltc.py your_file.volt"
echo "=========================================="
