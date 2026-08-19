import sys
import re

# Global dictionary to store variables
variables = {}

def evaluate_value(val):
    val = val.strip()
    
    # Check string literals
    if (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
        return val[1:-1]
        
    # Check digits directly
    if val.isdigit():
        return int(val)

    # Evaluate dynamic expression with variable substitution
    eval_expr = val
    for var_name, var_val in variables.items():
        # Replace variable with its representation
        eval_expr = re.sub(rf'\b{var_name}\b', repr(var_val), eval_expr)

    try:
        return eval(eval_expr)
    except Exception:
        if val in variables:
            return variables[val]
        return val

def mama_ai_guard(line, line_num):
    """Mama AI Assistant to detect syntax issues and recommend fixes"""
    print(f"\n[Mama AI Guard Alert on Line {line_num}]")
    print(f"--> Code: '{line.strip()}'")

    clean_line = line.strip().lower()
    
    if clean_line.startswith("mama say") and not (clean_line.endswith("'") or clean_line.endswith('"')):
        print("💡 Mama AI Suggestion: Did you forget to wrap string in quotes? Example: Mama say 'Hello'")
    elif ("mama check" in clean_line or "mama repeat" in clean_line) and not clean_line.endswith(":"):
        print("💡 Mama AI Suggestion: Block statements need a colon ':' at the end. Example: Mama check x > 10:")
    elif clean_line.startswith("mama") and not any(k in clean_line for k in ["say", "keep", "check", "repeat"]):
        print("💡 Mama AI Suggestion: Unknown command. Supported commands: 'Mama say', 'Mama keep', 'Mama check', 'Mama repeat'.")
    else:
        print("💡 Mama AI Suggestion: Check indentation or verify if the variable is defined.")

def extract_block(lines, start_index):
    """Extract indented block belonging to a control structure"""
    block = []
    i = start_index
    while i < len(lines):
        line = lines[i]
        # Empty lines or lines with indentation belong to the block
        if not line.strip() or line.startswith("    ") or line.startswith("\t"):
            # Strip 4 spaces or 1 tab of outer indentation level
            if line.startswith("    "):
                block.append(line[4:])
            elif line.startswith("\t"):
                block.append(line[1:])
            else:
                block.append(line)
            i += 1
        else:
            break
    return block, i

def parse_and_run(lines):
    i = 0
    while i < len(lines):
        raw_line = lines[i]
        line = raw_line.strip()
        
        # Ignore empty lines and comments
        if not line or line.startswith("#") or line.startswith("//"):
            i += 1
            continue

        # 1. Output: Mama say 'Text' or Mama say variable
        say_match = re.match(r"^Mama\s+say\s+(.*)$", line, re.IGNORECASE)
        if say_match:
            content = say_match.group(1).strip()
            # If not string, not digit, and not valid expr/var, invoke AI guard
            try:
                res = evaluate_value(content)
                print(res)
            except Exception:
                mama_ai_guard(raw_line, i + 1)
            i += 1
            continue

        # 2. Variable Assignment: Mama keep x = 10
        keep_match = re.match(r"^Mama\s+keep\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.*)$", line, re.IGNORECASE)
        if keep_match:
            var_name = keep_match.group(1).strip()
            var_value = keep_match.group(2).strip()
            variables[var_name] = evaluate_value(var_value)
            i += 1
            continue

        # 3. Loops: Mama repeat 3 times:
        repeat_match = re.match(r"^Mama\s+repeat\s+(.*?)\s+times\s*:\s*$", line, re.IGNORECASE)
        if repeat_match:
            times_val = evaluate_value(repeat_match.group(1).strip())
            block_lines, next_i = extract_block(lines, i + 1)
            
            try:
                count = int(times_val)
                for _ in range(count):
                    parse_and_run(block_lines)
            except ValueError:
                mama_ai_guard(raw_line, i + 1)
                
            i = next_i
            continue

        # 4. Conditionals: Mama check x > 5:
        check_match = re.match(r"^Mama\s+check\s+(.*?)\s*:\s*$", line, re.IGNORECASE)
        if check_match:
            condition_str = check_match.group(1).strip()
            if_block, next_i = extract_block(lines, i + 1)
            
            # Evaluate condition
            eval_cond = condition_str
            for var, val in variables.items():
                eval_cond = re.sub(rf'\b{var}\b', repr(val), eval_cond)
            
            try:
                condition_result = bool(eval(eval_cond))
            except Exception:
                condition_result = False

            else_block = []
            # Check for 'otherwise:' block right after 'check' block
            if next_i < len(lines) and lines[next_i].strip().lower().startswith("otherwise:"):
                else_block, next_i = extract_block(lines, next_i + 1)

            if condition_result:
                parse_and_run(if_block)
            else:
                parse_and_run(else_block)

            i = next_i
            continue

        # Syntax Error Fallback
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
