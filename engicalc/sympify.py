from sympy import sympify, Eq, Piecewise, latex
from engicalc.parsing import parse
import ast

def sympify_name(parsed_tuple):
    """
    If the parsed tuple is of type 'name', sympifies the value and returns the sympy object.
    """
    typ, value = parsed_tuple
    if typ == 'name':
        return sympify(value)
    else:
        raise ValueError("Input tuple is not of type 'name'.")

def sympify_expr(parsed_tuple):
    """
    If the parsed tuple is of type 'expr', sympifies the value and returns the sympy object.
    """
    typ, value = parsed_tuple
    if typ == 'expr':
        return sympify(value)
    else:
        raise ValueError("Input tuple is not of type 'expr'.")


def sympify_unknown(parsed_tuple):
    """
    Tries to sympify the value of an 'unknown' parsed tuple. If successful, returns the sympy object, otherwise returns the raw string.
    """
    typ, value = parsed_tuple
    if typ == 'unknown':
        try:
            return sympify(value)
        except Exception:
            return value
    else:
        raise ValueError("Input tuple is not of type 'unknown'.")

def sympify_assignment(parsed_tuple):
    """
    If the parsed tuple is of type 'assignment', splits at '=', sympifies lhs as name and rhs as expression, and returns sympy.Eq(lhs, rhs).
    """
    typ, value = parsed_tuple
    if typ == 'assignment':
        if '=' not in value:
            raise ValueError("Assignment does not contain '=' sign.")
        lhs, rhs = value.split('=', 1)
        lhs = lhs.strip()
        rhs = rhs.strip()
        lhs_sym = sympify_name(('name', lhs))
        rhs_sym = sympify_expr(('expr', rhs))
        return (lhs_sym, rhs_sym)
    else:
        raise ValueError("Input tuple is not of type 'assignment'.")

def sympify_conditional(parsed_tuple):
    """
    If the parsed tuple is of type 'conditional', uses ast to detect conditionals and their bodies.
    Recursively parses and sympifies the body for nested conditionals. Returns a Piecewise sympy object.
    Uses ast.unparse for all code extraction (Python 3.9+ required).
    """
    typ, value = parsed_tuple
    if typ != 'conditional':
        raise ValueError("Input tuple is not of type 'conditional'.")
    # Parse the code with ast
    tree = ast.parse(value)
    pieces = []
    for node in tree.body:
        if isinstance(node, ast.If):
            # Get the condition as code
            cond_code = ast.unparse(node.test)
            # Get the body as code
            body_code = '\n'.join([ast.unparse(stmt) for stmt in node.body])
            parsed_body = parse(body_code)
            sympified_body = do_sympify(parsed_body)
            body_obj = sympified_body[0] if sympified_body else None
            pieces.append((body_obj, sympify(cond_code)))
            # Handle orelse (elif/else)
            orelse = node.orelse
            while orelse:
                first = orelse[0]
                if isinstance(first, ast.If):
                    elif_cond = ast.unparse(first.test)
                    body_code = '\n'.join([ast.unparse(stmt) for stmt in first.body])
                    parsed_body = parse(body_code)
                    sympified_body = do_sympify(parsed_body)
                    body_obj = sympified_body[0] if sympified_body else None
                    pieces.append((body_obj, sympify(elif_cond)))
                    orelse = first.orelse
                else:
                    # else block
                    body_code = '\n'.join([ast.unparse(stmt) for stmt in orelse])
                    parsed_body = parse(body_code)
                    sympified_body = do_sympify(parsed_body)
                    body_obj = sympified_body[0] if sympified_body else None
                    pieces.append((body_obj, True))
                    break
    return Piecewise(*pieces)

def sympify_function(parsed_tuple):
    """
    If the parsed tuple is of type 'function', uses ast to extract the function name, parameters, and return statement.
    Creates an assignment from the function name (with parameters) and return value, sympifies it, and sympifies the rest of the body.
    Returns all sympified objects.
    """
    typ, value = parsed_tuple
    if typ != 'function':
        raise ValueError("Input tuple is not of type 'function'.")
    # Parse the function code with ast
    tree = ast.parse(value)
    func_node = next((node for node in tree.body if isinstance(node, ast.FunctionDef)), None)
    if func_node is None:
        raise ValueError("No function definition found.")
    func_name = func_node.name
    # Get parameter names
    params = [arg.arg for arg in func_node.args.args]
    param_str = ','.join(params)
    # Find the return statement
    return_expr = None
    for stmt in func_node.body:
        if isinstance(stmt, ast.Return):
            return_expr = ast.unparse(stmt.value)
            break
    if return_expr is None:
        raise ValueError("No return statement found in function body.")
    # Create assignment string with parameters
    assignment_str = f"{func_name}({param_str}) = {return_expr}"
    assignment_obj = sympify_assignment(('assignment', assignment_str))
    # Optionally, parse and sympify the rest of the body (excluding return)
    body_code = '\n'.join([
        ast.unparse(stmt)
        for stmt in func_node.body if not isinstance(stmt, ast.Return)
    ])
    parsed_body = parse(body_code)
    sympified_body = do_sympify(parsed_body)
    return [assignment_obj] + sympified_body


def do_sympify(parsed_tuples):
    """
    Takes a list of parsed tuples and returns a list of sympified objects by dispatching to the correct sympify function.
    """
    result = []
    for parsed in parsed_tuples:
        typ = parsed[0]
        if typ == 'name':
            obj = sympify_name(parsed)
            result.append(obj)
        elif typ == 'expr':
            obj = sympify_expr(parsed)
            result.append(obj)
        elif typ == 'assignment':
            obj = sympify_assignment(parsed)
            result.append(obj)
        elif typ == 'conditional':
            obj = sympify_conditional(parsed)
            result.append(obj)
        elif typ == 'function':
            objs = sympify_function(parsed)
            result.extend(objs)
        else:
            obj = sympify_unknown(parsed)
            result.append(obj)
    return result

