# ⚡ VoltScript

**The Electrical Language for Embedded Minds**  

VoltScript is an experimental open-source programming language (DSL) designed for **electrical engineers, students, and makers** who want to write simple, readable code for development boards like **ESP32, STM32, and Raspberry Pi Pico** — without diving into low-level boilerplate.  

VoltScript makes embedded programming feel like writing electrical logic instead of wiring complex code.  

---

## ✨ Features
- Simple **Python-based parser & compiler** → Converts `.volt` code to C++ for microcontrollers.  
- **Cross-platform** → Works on multiple development boards via PlatformIO.  
- **Beginner-friendly syntax** → Close to natural electrical logic.  
- Open-source, extensible, and built for the community.  

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
Here’s the updated **README.md** adapted for **VoltScript** ⚡ — with the one-line description and no mention of Arduino anywhere:

---

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Write VoltScript Code

Example: `led_blink.volt`

```volt
output LED pin=13;

loop {
    LED = HIGH;
    wait 1s;
    LED = LOW;
    wait 1s;
}
```

### 4. Compile to C++

```bash
python parser.py led_blink.volt -o led_blink.cpp
```

---

## 🔍 Example Programs

### ✅ Motor Control

```volt
output Motor pin=5;
input Sensor pin=2;

loop {
    if Sensor == HIGH {
        Motor = ON;
    } else {
        Motor = OFF;
    }
}
```

Generated C++:

```cpp
int Motor = 5;
int Sensor = 2;

void setup() {
  pinMode(Motor, OUTPUT);
  pinMode(Sensor, INPUT);
}

void loop() {
  if (digitalRead(Sensor) == HIGH) {
    digitalWrite(Motor, HIGH);
  } else {
    digitalWrite(Motor, LOW);
  }
}
```

---

## 🐍 Python Parser (Overview)

VoltScript uses a **Python-based parser & transpiler**.

* **Lexer/Parser** → Reads `.volt` syntax.
* **AST (Abstract Syntax Tree)** → Represents logic (outputs, inputs, loops, conditions).
* **Code Generator** → Translates AST to C++ code.

File: `parser.py`

```python
import sys

def parse_volt_code(code: str) -> str:
    lines = code.splitlines()
    cpp_lines = [
        "#include <Arduino.h>\n",
        "void setup() {}\n",
        "void loop() {}\n"
    ]
    for line in lines:
        if line.startswith("output"):
            parts = line.split()
            var, pin = parts[1], parts[-1].replace(";", "")
            cpp_lines.insert(1, f"int {var} = {pin};\n")
            cpp_lines.insert(2, f"void setup() {{ pinMode({var}, OUTPUT); }}\n")
        if "wait" in line:
            time = line.split()[1].replace("s;", "")
            cpp_lines.insert(-1, f"delay({int(time)*1000});\n")
    return "".join(cpp_lines)

if __name__ == "__main__":
    infile = sys.argv[1]
    outfile = sys.argv[3]
    with open(infile) as f:
        code = f.read()
    cpp_code = parse_volt_code(code)
    with open(outfile, "w") as f:
        f.write(cpp_code)
```

---

## 🤝 Contributing

We welcome contributions from the community!

* Fork the repo
* Create a feature branch
* Submit a pull request 🚀

---

## 📜 License

VoltScript is released under the **MIT License**.

---

## ⚡ Vision

“**Just as electricity powers machines, VoltScript powers ideas with code.**”

```

---

👉 Do you also want me to **expand the parser** so it supports not just `output` and `wait`, but also `input` and `if/else` blocks for real conditions?
```

