import sys
import re

# Dictionary to store variables created by 'Mama keep'
variables = {}

def parse_and_run(line):
    line = line.strip()
    
    # Ignore empty lines and comments
    if not line or line.startswith("#"):
        return

    # 1. Handle Output: Mama say 'Text' or Mama say variable_name
    say_match = re.match(r"^Mama\s+say\s+(.*)$", line, re.IGNORECASE)
    if say_match:
        content = say_match.group(1).strip()
        
        # Check if the content is wrapped in single or double quotes (String)
        if (content.startswith("'") and content.endswith("'")) or (content.startswith('"') and content.endswith('"')):
            print(content[1:-1])
        # Check if it's a stored variable name
        elif content in variables:
            print(variables[content])
        else:
            print(f"Mama AI Suggestion: Variable '{content}' is not defined. Did you forget quotes or definition?")
        return

    # 2. Handle Variables: Mama keep variable_name = value
    keep_match = re.match(r"^Mama\s+keep\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.*)$", line, re.IGNORECASE)
    if keep_match:
        var_name = keep_match.group(1).strip()
        var_value = keep_match.group(2).strip()
        
        # Evaluate integer or remove quotes for string
        if var_value.isdigit():
            variables[var_name] = int(var_value)
        elif (var_value.startswith("'") and var_value.endswith("'")) or (var_value.startswith('"') and var_value.endswith('"')):
            variables[var_name] = var_value[1:-1]
        else:
            variables[var_name] = var_value
        return

    # Fallback Error Handling
    print(f"Mama Syntax Error: Invalid command -> '{line}'")
    print("Mama AI Suggestion: Check if you meant 'Mama say' or 'Mama keep'.")

def run_mama_file(filename):
    try:
        with open(filename, 'r') as file:
            for line in file:
                parse_and_run(line)
    except FileNotFoundError:
        print(f"Mama Error: File '{filename}' not found!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mama.py <filename.mama>")
    else:
        run_mama_file(sys.argv[1])
