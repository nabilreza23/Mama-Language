import sys
import re

# Global dictionary to store variables
variables = {}

def safe_input(prompt=""):
    """Handles standard input safely for both CLI and GitHub Actions CI"""
    try:
        return input(prompt)
    except EOFError:
        print(f"{prompt} (CI Auto Input: 20)")
        return "20"

def evaluate_value(val):
    val = val.strip()
    
    # String literals
    if (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
        return val[1:-1]
        
    # Pure numbers
    if val.isdigit():
        return int(val)

    # Dynamic expression evaluation with variables
    eval_expr = val
    for var_name, var_val in list(variables.items()):
        eval_expr = re.sub(rf'\b{var_name}\b', repr(var_val), eval_expr)

    try:
        return eval(eval_expr)
    except Exception:
        if val in variables:
            return variables[val]
        return val

def mama_ai_guard(line, line_num):
    """Mama AI Guard for intelligent error diagnosis"""
    print(f"\n[Mama AI Guard Alert on Line {line_num}]")
    print(f"--> Code: '{line.strip()}'")

    clean_line = line.strip().lower()
    
    if clean_line.startswith("mama say") and not (clean_line.endswith("'") or clean_line.endswith('"')):
        print("💡 Mama AI Suggestion: Wrap text in quotes, e.g., Mama say 'Hello'")
    elif clean_line.startswith("mama take") and "=" not in clean_line:
        print("💡 Mama AI Suggestion: Correct syntax is -> Mama take age = 'Enter age: '")
    elif ("mama check" in clean_line or "mama repeat" in clean_line) and not clean_line.endswith(":"):
        print("💡 Mama AI Suggestion: Missing colon ':' at the end of statement.")
    else:
        print("💡 Mama AI Suggestion: Check syntax or verify if variables are properly defined.")

def extract_block(lines, start_index):
    """Extracts indented code block"""
    block = []
    i = start_index
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.startswith("    ") or line.startswith("\t"):
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
        
        if not line or line.startswith("#") or line.startswith("//"):
            i += 1
            continue

        # 1. User Input: Mama take age = 'Enter your age: '
        take_match = re.match(r"^Mama\s+take\s+([a-zA-Z_][a-zA-Z0-9_]*)(?:\s*=\s*(.*))?$", line, re.IGNORECASE)
        if take_match:
            var_name = take_match.group(1).strip()
            prompt_msg = take_match.group(2)
            prompt_str = evaluate_value(prompt_msg) if prompt_msg else ""
            
            user_val = safe_input(str(prompt_str))
            variables[var_name] = evaluate_value(user_val)
            i += 1
            continue

        # 2. Output: Mama say 'Hello' or Mama say x + 5
        say_match = re.match(r"^Mama\s+say\s+(.*)$", line, re.IGNORECASE)
        if say_match:
            content = say_match.group(1).strip()
            try:
                res = evaluate_value(content)
                print(res)
            except Exception:
                mama_ai_guard(raw_line, i + 1)
            i += 1
            continue

        # 3. Variable Assignment: Mama keep score = 10 + 20
        keep_match = re.match(r"^Mama\s+keep\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.*)$", line, re.IGNORECASE)
        if keep_match:
            var_name = keep_match.group(1).strip()
            var_value = keep_match.group(2).strip()
            variables[var_name] = evaluate_value(var_value)
            i += 1
            continue

        # 4. Loops: Mama repeat 3 times:
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

        # 5. Conditionals: Mama check age >= 18:
        check_match = re.match(r"^Mama\s+check\s+(.*?)\s*:\s*$", line, re.IGNORECASE)
        if check_match:
            condition_str = check_match.group(1).strip()
            if_block, next_i = extract_block(lines, i + 1)
            
            eval_cond = condition_str
            for var, val in variables.items():
                eval_cond = re.sub(rf'\b{var}\b', repr(val), eval_cond)
            
            try:
                condition_result = bool(eval(eval_cond))
            except Exception:
                condition_result = False

            else_block = []
            if next_i < len(lines) and lines[next_i].strip().lower().startswith("otherwise:"):
                else_block, next_i = extract_block(lines, next_i + 1)

            if condition_result:
                parse_and_run(if_block)
            else:
                parse_and_run(else_block)

            i = next_i
            continue

        mama_ai_guard(raw_line, i + 1)
        i += 1

def run_mama_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            parse_and_run(lines)
    except FileNotFoundError:
        print(f"Mama Error: File '{filename}' not found!")

def main():
    if len(sys.argv) < 2:
        print("Usage: mama <filename.mama>")
    else:
        run_mama_file(sys.argv[1])

if __name__ == "__main__":
    main()
