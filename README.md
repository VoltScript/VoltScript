# VoltScript Compiler

## Overview
VoltScript is an experimental open-source programming language compiler that translates VoltScript source code to C++. The compiler includes a lexer, parser, and code generator that outputs standard C++ code which can then be compiled with any C++ compiler.

The project features both a **web-based compiler** for browser-based editing and a **command-line compiler** for batch processing.

## Project Structure
```
.
├── src/
│   ├── lexer.py          # Tokenizer for VoltScript syntax
│   ├── parser.py         # Parser that builds Abstract Syntax Tree
│   ├── ast_nodes.py      # AST node definitions
│   └── codegen.py        # Code generator that outputs C++
├── templates/
│   └── index.html        # Web compiler UI
├── static/
│   ├── style.css         # Web compiler styles
│   └── script.js         # Web compiler functionality
├── examples/
│   ├── hello.volt        # Basic example with variables and print
│   ├── loop.volt         # While and for loop examples
│   ├── conditional.volt  # If-else conditional examples
│   └── equality.volt     # Equality operator examples
├── app.py                # Flask web application
├── voltc.py              # Command-line compiler
└── demo.sh               # CLI demo script
```

## Current Features
- **Data Types**: int, float, string, bool
- **Variables**: Declaration and assignment
- **Operators**: Arithmetic (+, -, *, /, %), comparison (==, !=, <, >, <=, >=), logical (&&, ||, !)
- **Control Flow**: if-else statements, while loops, for loops
- **Built-in Functions**: print()
- **Comments**: Single-line comments (//)

## Usage

### Web Compiler (Recommended)
The web interface is the easiest way to use VoltScript. Simply run the app and write code in your browser:
- Write VoltScript code in the left panel
- Click "Compile" to see generated C++ in the right panel
- Try example programs using the quick-load buttons

### Command-Line Compiler
Compile a VoltScript file to C++:
```bash
python voltc.py <input.volt> [output.cpp]
```

Run the CLI demo:
```bash
bash demo.sh
```

## Example
VoltScript code:
```volt
int x = 10;
int y = 20;
int sum = x + y;
print(sum);
```

Generated C++ code:
```cpp
#include <iostream>
#include <string>

int main() {
    int x = 10;
    int y = 20;
    int sum = (x + y);
    std::cout << sum << std::endl;
    return 0;
}
```

## Recent Changes
- 2025-10-02: Initial compiler implementation with lexer, parser, and code generator
- 2025-10-02: Added support for basic language constructs and control flow
- 2025-10-02: Created example programs and CLI demo workflow
- 2025-10-02: Built web-based compiler with Flask backend and interactive UI
- 2025-10-02: Fixed equality operator (==, !=) tokenization bug
