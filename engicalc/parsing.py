import ast

input = """var_test
assign_test = var_test + 10

def test_func():
    assign_test2 = var_test + 20
    return assign_test2 

def test_func2():
    assign_test2 = var_test + 34
    return assign_test2 

# this is a comment
def test_func3(a):
    assign_test2 = var_test + 34*a
    
    return assign_test2 

if condition_test == True:
    assign_test3 = var_test + 30

elif condition_test == False:
    assign_test3 = var_test + 40

else:
    assign_test3 = var_test + 50

x = test_func3(4)   
test_func3(5)
"""

def get_code(node, lines):
    start = getattr(node, 'lineno', 1) - 1
    end = getattr(node, 'end_lineno', start + 1)
    return '\n'.join(lines[start:end])

def parse(code: str,):
    """
    Parses the input code using ast and returns a list of tuples (syntax_type, content).
    syntax_type: 'name', 'assignment', 'function', 'if', 'call', or 'unknown'
    content: the source code of the detected object
    """
    results = []
    try:
        tree = ast.parse(code)
    except Exception as e:
        return [("error", str(e))]

    lines = code.splitlines()

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            results.append(("function", get_code(node, lines)))
        elif isinstance(node, ast.Assign):
            results.append(("assignment", get_code(node, lines)))
        elif isinstance(node, ast.If):
            results.append(("conditional", get_code(node, lines)))
        elif isinstance(node, ast.Expr):
            # Detect function call
            if isinstance(node.value, ast.Call):
                # Get the function call as code
                results.append(("call", get_code(node, lines)))
            elif isinstance(node.value, ast.Name):
                results.append(("name", node.value.id))
            else:
                results.append(("expression", get_code(node, lines)))
        else:
            results.append(("unknown", get_code(node, lines)))
    return results


def cell_content() -> str:
    """
    Returns the content of the current Jupyter notebook cell as a string.
    """
    try:
        from IPython import get_ipython
        ip = get_ipython()
        if ip is None:
            raise RuntimeError("Not running inside an IPython environment.")
        # Use ip.history_manager to get the last input (current cell)
        cell = ip.history_manager.input_hist_raw[-1]
        return cell
    except Exception as e:
        raise RuntimeError(f"Could not retrieve cell content: {e}")

if __name__ == "__main__":
    # If running as a script, parse the input code
    print("Input code:")
    print(input)
    print("\nParsed output:")
    print(parse(input))
