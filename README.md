# 🚀 Mama Language (v1.0.0)

An intuitive, Bengali keyword-based interpreted programming language built with Python. Designed to make coding fun, relatable, and accessible!

[![PyPI version](https://img.shields.io/pypi/v/mama-lang.svg)](https://pypi.org/project/mama-lang/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📦 Installation

Install Mama Language globally using `pip`:

```bash
pip install mama-lang
```

## ⚡ Quick Start & Interactive REPL
​To start the live interactive shell (REPL), simply open your terminal and run:
```bash
mama
```

#### To execute a .mama source file:
```bash
mama script.mama
```


## 📜 Syntax & Features
**​1. Printing Output (Mama say)**
```bash
Mama say 'Hello World!'
Mama say 100 + 50
```
**2. Variables & Constants (Mama keep)**
```bash
Mama keep name = 'Nabil'
Mama keep age = 22
Mama keep fruits = ['Apple', 'Banana', 'Mango']
```

**3. Conditionals & Logic (Mama check / otherwise)**
```bash
Mama check age >= 18 and status == 'active':
    Mama say 'Access Granted!'
otherwise:
    Mama say 'Access Denied!'
```

**4. Loops (Mama repeat)**
```bash
# Fixed iteration loop
Mama repeat 3 times:
    Mama say 'Looping...'
```
```bash
# Array For-Each loop
Mama repeat item in fruits:
    Mama say item
```


**5. Functions & Return (Mama do / Mama give / Mama call)**
```bash
Mama do addNumbers(a, b):
    Mama keep total = a + b
    Mama give total

Mama keep result = Mama call addNumbers(10, 20)
Mama say result
```

**6. Error Handling (Mama try / Mama catch)**
```bash
Mama try:
    Mama keep x = 10 / 0
Mama catch:
    Mama say 'Safely handled division by zero!'
```

**7. File Operations (Mama write / Mama read)**
```bash
Mama write 'data.txt' = 'Mama Language File System'
Mama keep content = Mama read 'data.txt'
Mama say content
```

**8. Web Data Fetching (Mama fetch)**
```bash
Mama keep response = Mama fetch '[https://api.github.com](https://api.github.com)'
Mama say response
```

**9. Module Import (Mama import)**
```bash
Mama import 'helper.mama'
Mama call helperFunction()
```
