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

x = test_func3(4)   
"""

def parse(code: str):
    """
    Parses the input code using ast and returns a list of tuples (syntax_type, content).
    syntax_type: 'name', 'assignment', 'function', 'if', or 'unknown'
    content: the source code of the detected object
    """
    results = []
    try:
        tree = ast.parse(code)
    except Exception as e:
        return [("error", str(e))]

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            # Get the function source code
            start = node.lineno - 1
            end = node.end_lineno if hasattr(node, 'end_lineno') else node.lineno
            lines = code.splitlines()
            func_code = '\n'.join(lines[start:end])
            results.append(("function", func_code))
        elif isinstance(node, ast.Assign):
            start = node.lineno - 1
            end = node.end_lineno if hasattr(node, 'end_lineno') else node.lineno
            lines = code.splitlines()
            assign_code = '\n'.join(lines[start:end])
            results.append(("assignment", assign_code))
        elif isinstance(node, ast.If):
            start = node.lineno - 1
            end = node.end_lineno if hasattr(node, 'end_lineno') else node.lineno
            lines = code.splitlines()
            if_code = '\n'.join(lines[start:end])
            results.append(("if", if_code))
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Name):
            results.append(("name", node.value.id))
        else:
            # fallback: try to get the code for unknown nodes
            start = getattr(node, 'lineno', 1) - 1
            end = getattr(node, 'end_lineno', start + 1)
            lines = code.splitlines()
            unknown_code = '\n'.join(lines[start:end])
            results.append(("unknown", unknown_code))
    return results

print(parse(input))

