<div align="center">

# 🚀 Mama Language (v1.0.0)

***An intuitive, Bengali keyword-based interpreted programming language built with Python.***

Designed to make coding fun, highly relatable, and accessible for everyone!

[![PyPI Version](https://img.shields.io/pypi/v/mama-lang.svg?style=for-the-badge&color=ff69b4)](https://pypi.org/project/mama-lang/)
[![Build Status](https://img.shields.io/github/actions/workflow/status/nabilreza23/Mama-Language/test-mama.yml?branch=main&style=for-the-badge&logo=github)](https://github.com/nabilreza23/Mama-Language/actions)
[![PyPI Downloads](https://img.shields.io/pypi/dm/mama-lang?style=for-the-badge&color=blue)](https://pypi.org/project/mama-lang/)
[![Python Version](https://img.shields.io/pypi/pyversions/mama-lang?style=for-the-badge&logo=python&logoColor=white)](https://pypi.org/project/mama-lang/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

</div>




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


## 🛠️ Built-in Helpers
`​length(list_or_string)` : Returns the total number of items or length.
​
## 🤝 Contributing
​Feel free to open issues or pull requests on GitHub.
​
## 📄 License
​This project is licensed under the MIT License.
