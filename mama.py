import sys
import re

# Dictionary to store variables created by 'Mama keep'
variables = {}

def evaluate_value(val):
    val = val.strip()
    if val.isdigit():
        return int(val)
    if (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
        return val[1:-1]
    if val in variables:
        return variables[val]
    return val

def mama_ai_guard(line, line_num):
    """AI Assistant to analyze syntax mistakes and provide smart suggestions"""
    print(f"\n[Mama AI Guard Alert on Line {line_num}]")
    print(f"--> Code: '{line.strip()}'")

    # Suggestion for missing quotes in Mama say
    if line.strip().lower().startswith("mama say") and not (line.strip().endswith("'") or line.strip().endswith('"')):
        print("💡 Mama AI Suggestion: Did you forget to wrap your text in quotes? Example: Mama say 'Hello'")
    # Suggestion for missing colon in check or repeat
    elif ("mama check" in line.lower() or "mama repeat" in line.lower()) and not line.strip().endswith(":"):
        print("💡 Mama AI Suggestion: Block statements need a colon ':' at the end. Example: Mama check x > 10:")
    # Suggestion for typo in Mama keywords
    elif line.strip().lower().startswith("mama") and not any(k in line.lower() for k in ["say", "keep", "check", "repeat"]):
        print("💡 Mama AI Suggestion: Unknown Mama command. Valid commands are 'Mama say', 'Mama keep', 'Mama check', and 'Mama repeat'.")
    else:
        print("💡 Mama AI Suggestion: Check indentation or verify variable definitions before using them.")

def parse_and_run(lines):
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        raw_line = lines[i]
        
        # Ignore empty lines and comments
        if not line or line.startswith("#"):
            i += 1
            continue

        # 1. Handle Output: Mama say 'Text' or Mama say variable_name
        say_match = re.match(r"^Mama\s+say\s+(.*)$", line, re.IGNORECASE)
        if say_match:
            content = say_match.group(1).strip()
            # Check for unquoted plain text that isn't a variable
            if not ((content.startswith("'") and content.endswith("'")) or (content.startswith('"') and content.endswith('"'))) and content not in variables and not content.isdigit():
                mama_ai_guard(raw_line, i + 1)
            else:
                print(evaluate_value(content))
            i += 1
            continue

        # 2. Handle Variables: Mama keep variable_name = value
        keep_match = re.match(r"^Mama\s+keep\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.*)$", line, re.IGNORECASE)
        if keep_match:
            var_name = keep_match.group(1).strip()
            var_value = keep_match.group(2).strip()
            variables[var_name] = evaluate_value(var_value)
            i += 1
            continue

        # 3. Handle Loops: Mama repeat 5 times:
        repeat_match = re.match(r"^Mama\s+repeat\s+(.*?)\s+times\s*:\s*$", line, re.IGNORECASE)
        if repeat_match:
            times_val = evaluate_value(repeat_match.group(1).strip())
            
            block_lines = []
            i += 1
            while i < len(lines) and (lines[i].startswith("    ") or lines[i].startswith("\t")):
                block_lines.append(lines[i])
                i += 1
            
            try:
                count = int(times_val)
                for _ in range(count):
                    parse_and_run(block_lines)
            except ValueError:
                mama_ai_guard(raw_line, i)
            continue

        # 4. Handle Conditions: Mama check age > 18:
        check_match = re.match(r"^Mama\s+check\s+(.*?)\s*:\s*$", line, re.IGNORECASE)
        if check_match:
            condition_str = check_match.group(1).strip()
            
            for var in variables:
                condition_str = re.sub(rf'\b{var}\b', str(repr(variables[var])), condition_str)
            
            try:
                condition_result = eval(condition_str)
            except Exception:
                condition_result = False

            i += 1
            if condition_result:
                while i < len(lines) and (lines[i].startswith("    ") or lines[i].startswith("\t")):
                    parse_and_run([lines[i]])
                    i += 1
                if i < len(lines) and lines[i].strip().lower().startswith("otherwise:"):
                    i += 1
                    while i < len(lines) and (lines[i].startswith("    ") or lines[i].startswith("\t")):
                        i += 1
            else:
                while i < len(lines) and (lines[i].startswith("    ") or lines[i].startswith("\t")):
                    i += 1
                if i < len(lines) and lines[i].strip().lower().startswith("otherwise:"):
                    i += 1
                    while i < len(lines) and (lines[i].startswith("    ") or lines[i].startswith("\t")):
                        parse_and_run([lines[i]])
                        i += 1
            continue

        # Fallback to AI Assistant for Syntax Errors
        mama_ai_guard(raw_line, i + 1)
        i += 1

def run_mama_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            parse_and_run(lines)
    except FileNotFoundError:
        print(f"Mama Error: File '{filename}' not found!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mama.py <filename.mama>")
    else:
        run_mama_file(sys.argv[1])
