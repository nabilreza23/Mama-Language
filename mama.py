import sys
import re
import os

global_scope = {}

class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get(name)
        return None

    def set(self, name, value):
        self.vars[name] = value

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

def evaluate_expr(expr, env):
    expr = str(expr).strip()
    if not expr:
        return None
        
    if (expr.startswith("'") and expr.endswith("'")) or (expr.startswith('"') and expr.endswith('"')):
        return expr[1:-1]
        
    if expr.isdigit():
        return int(expr)
    try:
        return float(expr) if '.' in expr else int(expr)
    except ValueError:
        pass

    # Array evaluation
    if expr.startswith('[') and expr.endswith(']'):
        items = expr[1:-1].split(',')
        return [evaluate_expr(item, env) for item in items if item.strip()]

    # Built-in helper: length check e.g. length(my_list)
    len_match = re.match(r"^length\((.*?)\)$", expr, re.IGNORECASE)
    if len_match:
        target = evaluate_expr(len_match.group(1), env)
        if isinstance(target, (list, str)):
            return len(target)
        return 0

    eval_str = expr
    eval_str = re.sub(r'\band\b', ' and ', eval_str, flags=re.IGNORECASE)
    eval_str = re.sub(r'\bor\b', ' or ', eval_str, flags=re.IGNORECASE)

    tokens = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', eval_str)
    for token in set(tokens):
        if token in ['and', 'or', 'not', 'True', 'False', 'None']:
            continue
        val = env.get(token)
        if val is not None:
            eval_str = re.sub(rf'\b{token}\b', repr(val), eval_str)

    try:
        return eval(eval_str)
    except Exception:
        val = env.get(expr)
        return val if val is not None else expr

def mama_ai_guard(line, line_num, err_details=""):
    """Mama AI Smart Assistant"""
    print(f"\n🚨 [Mama AI Guard Alert on Line {line_num}]")
    print(f"--> Code: '{line.strip()}'")
    clean = line.strip().lower()

    if clean.startswith("mama write") and "=" not in clean:
        print("💡 Suggestion: Use format -> Mama write 'filename.txt' = 'content'")
    elif clean.startswith("mama read") and not clean.endswith("'") and not clean.endswith('"'):
        print("💡 Suggestion: Pass filename in quotes -> Mama keep text = Mama read 'file.txt'")
    else:
        print(f"💡 Suggestion: Check logic/syntax. Details: {err_details}")

def extract_block(lines, start_index):
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

def run_ast(lines, env):
    i = 0
    while i < len(lines):
        raw_line = lines[i]
        line = raw_line.strip()

        if not line or line.startswith("#") or line.startswith("//"):
            i += 1
            continue

        try:
            # Output
            if line.lower().startswith("mama say"):
                content = line[8:].strip()
                res = evaluate_expr(content, env)
                print(res)
                i += 1
                continue

            # File Write: Mama write 'filename.txt' = 'content'
            write_match = re.match(r"^Mama\s+write\s+(.*?)\s*=\s*(.*)$", line, re.IGNORECASE)
            if write_match:
                fname = evaluate_expr(write_match.group(1).strip(), env)
                content = evaluate_expr(write_match.group(2).strip(), env)
                with open(str(fname), 'w') as f:
                    f.write(str(content))
                i += 1
                continue

            # File Read & Storage: Mama keep content = Mama read 'filename.txt'
            if "mama read" in line.lower():
                target_var = line.split("=")[0].replace("Mama keep", "").strip() if "=" in line else None
                fname_expr = line[line.lower().find("mama read") + 9:].strip()
                fname = evaluate_expr(fname_expr, env)
                if os.path.exists(str(fname)):
                    with open(str(fname), 'r') as f:
                        file_data = f.read()
                    if target_var:
                        env.set(target_var, file_data)
                    else:
                        print(file_data)
                else:
                    print(f"Mama Error: File '{fname}' not found!")
                i += 1
                continue

            # For-Each Loop over Array: Mama repeat item in list_var:
            foreach_match = re.match(r"^Mama\s+repeat\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+in\s+(.*?)\s*:\s*$", line, re.IGNORECASE)
            if foreach_match:
                item_var = foreach_match.group(1).strip()
                list_target = evaluate_expr(foreach_match.group(2).strip(), env)
                block_lines, next_i = extract_block(lines, i + 1)

                if isinstance(list_target, list):
                    for val in list_target:
                        local_env = Environment(parent=env)
                        local_env.set(item_var, val)
                        run_ast(block_lines, local_env)
                i = next_i
                continue

            # Count Loop: Mama repeat 3 times:
            repeat_match = re.match(r"^Mama\s+repeat\s+(.*?)\s+times\s*:\s*$", line, re.IGNORECASE)
            if repeat_match:
                times_val = int(evaluate_expr(repeat_match.group(1).strip(), env))
                block_lines, next_i = extract_block(lines, i + 1)
                for _ in range(times_val):
                    run_ast(block_lines, env)
                i = next_i
                continue

            # Variable Storage
            keep_match = re.match(r"^Mama\s+keep\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.*)$", line, re.IGNORECASE)
            if keep_match:
                var_name = keep_match.group(1).strip()
                val_expr = keep_match.group(2).strip()
                env.set(var_name, evaluate_expr(val_expr, env))
                i += 1
                continue

            # Functions Definition & Execution
            func_match = re.match(r"^Mama\s+do\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)\s*:\s*$", line, re.IGNORECASE)
            if func_match:
                func_name = func_match.group(1).strip()
                params = [p.strip() for p in func_match.group(2).split(',') if p.strip()]
                block_lines, next_i = extract_block(lines, i + 1)
                env.set(f"__func_{func_name}__", (params, block_lines))
                i = next_i
                continue

            if line.lower().startswith("mama give"):
                ret_val = evaluate_expr(line[9:].strip(), env)
                raise ReturnException(ret_val)

            if "mama call" in line.lower():
                call_str = line[line.lower().find("mama call") + 9:].strip()
                c_match = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)$", call_str)
                if c_match:
                    f_name = c_match.group(1).strip()
                    args = [evaluate_expr(a.strip(), env) for a in c_match.group(2).split(',') if a.strip()]
                    func_data = env.get(f"__func_{f_name}__")
                    
                    if func_data:
                        f_params, f_body = func_data
                        local_env = Environment(parent=env)
                        for p_name, p_arg in zip(f_params, args):
                            local_env.set(p_name, p_arg)
                        try:
                            run_ast(f_body, local_env)
                        except ReturnException as ret:
                            if "=" in line:
                                target_var = line.split("=")[0].replace("Mama keep", "").strip()
                                env.set(target_var, ret.value)
                        i += 1
                        continue

            # Conditionals
            check_match = re.match(r"^Mama\s+check\s+(.*?)\s*:\s*$", line, re.IGNORECASE)
            if check_match:
                cond_expr = check_match.group(1).strip()
                if_block, next_i = extract_block(lines, i + 1)
                else_block = []
                
                if next_i < len(lines) and lines[next_i].strip().lower().startswith("otherwise:"):
                    else_block, next_i = extract_block(lines, next_i + 1)

                if bool(evaluate_expr(cond_expr, env)):
                    run_ast(if_block, env)
                else:
                    run_ast(else_block, env)

                i = next_i
                continue

            mama_ai_guard(raw_line, i + 1)
            i += 1

        except ReturnException as r:
            raise r
        except Exception as e:
            mama_ai_guard(raw_line, i + 1, str(e))
            i += 1

def run_mama_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            global_env = Environment()
            run_ast(lines, global_env)
    except FileNotFoundError:
        print(f"Mama Error: File '{filename}' not found!")

def main():
    if len(sys.argv) < 2:
        print("Usage: python mama.py <filename.mama>")
    else:
        run_mama_file(sys.argv[1])

if __name__ == "__main__":
    main()
