from sympy import sympify, Eq, Piecewise, latex
from engicalc.parsing import parse
from IPython.display import display, Markdown
import re



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

def sympify_call(parsed_tuple):
    """
    If the parsed tuple is of type 'call', sympifies the value and returns the sympy object.
    """
    typ, value = parsed_tuple
    if typ == 'call':
        return sympify(value)
    else:
        raise ValueError("Input tuple is not of type 'call'.")

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
        return Eq(lhs_sym, rhs_sym)
    else:
        raise ValueError("Input tuple is not of type 'assignment'.")

def sympify_conditional(parsed_tuple):
    """
    If the parsed tuple is of type 'conditional', parses the value for if-elif-else structure and returns a Piecewise sympy object.
    """
    typ, value = parsed_tuple
    if typ != 'conditional':
        raise ValueError("Input tuple is not of type 'conditional'.")
    pattern = re.compile(r'(?P<type>if|elif|else)\s*(?P<cond>[^:]*):\n(?P<body>(?:[ \t]+.+\n?)*)', re.MULTILINE)
    matches = list(pattern.finditer(value))
    pieces = []
    for m in matches:
        cond_type = m.group('type')
        cond = m.group('cond').strip()
        body = m.group('body').strip()
        # Use parse and do_sympify to handle the body
        parsed_body = parse(body)
        sympified_body = do_sympify(parsed_body)
        # Use the first sympified object if multiple are returned
        body_obj = sympified_body[0] if sympified_body else None
        if cond_type == 'else':
            pieces.append((body_obj, True))
        else:
            pieces.append((body_obj, sympify(cond)))
    return Piecewise(*pieces)

def sympify_function(parsed_tuple):
    """
    If the parsed tuple is of type 'function', extracts the function name and return statement,
    creates an assignment, and sympifies it. Also parses the body for additional sympy objects.
    """
    typ, value = parsed_tuple
    if typ != 'function':
        raise ValueError("Input tuple is not of type 'function'.")
    # Extract function name
    name_match = re.match(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', value)
    if not name_match:
        raise ValueError("Could not extract function name.")
    func_name = name_match.group(1)
    # Extract return statement (assumes 'return ...' is in the function body)
    return_match = re.search(r'return\s+(.+)', value)
    if not return_match:
        raise ValueError("No return statement found in function body.")
    return_expr = return_match.group(1).strip()
    # Create assignment string
    assignment_str = f"{func_name} = {return_expr}"
    assignment_obj = sympify_assignment(('assignment', assignment_str))
    # Optionally, parse the rest of the body for additional sympy objects
    body_match = re.search(r'def[\s\S]*?:\n([\s\S]*)', value)
    if body_match:
        body = body_match.group(1)
        parsed_body = parse(body)
        sympified_body = do_sympify(parsed_body)
        return [assignment_obj] + sympified_body
    else:
        return [assignment_obj]

def do_sympify(parsed_tuples):
    """
    Takes a list of parsed tuples and returns a list of sympified objects by dispatching to the correct sympify function.
    """
    result = []
    for parsed in parsed_tuples:
        typ = parsed[0]
        if typ == 'name':
            result.append(sympify_name(parsed))
        elif typ == 'expr':
            result.append(sympify_expr(parsed))
        elif typ == 'call':
            result.append(sympify_call(parsed))
        elif typ == 'assignment':
            result.append(sympify_assignment(parsed))
        elif typ == 'conditional':
            result.append(sympify_conditional(parsed))
        elif typ == 'function':
            result.extend(sympify_function(parsed))
        else:
            result.append(sympify_unknown(parsed))
    return result



if __name__ == "__main__":
    # Example usage
    parsed_tuple_name = ('name', 'test__2_3')
    parsed_tuple_expr = ('expr', '2*x + 3')
    parsed_tuple_call = ('call', 'test__2_3(x, y)')
    parsed_tuple_unknown = ('unknown', 'some*random&expression')
    parsed_tuple_assignment = ('assignment', 'a = 2*test_2__3 + 3')
    parsed_tuple_conditional = ('conditional', 'if x > 0:\n    a = 2*x + 3\nelif x < 0:\n    a = -2*x - 3\nelse:\n    a = 0')
    parsed_tuple_function = ('function', 'def test_func(x):\n    return 2*x + 3')
    try:
        result_name = sympify_name(parsed_tuple_name)
        print(f"Sympy object of name: {latex(result_name)}")

        result_expr = sympify_expr(parsed_tuple_expr)
        print(f"Sympy object of expr: {latex(result_expr)}")

        result_call = sympify_call(parsed_tuple_call)
        print(f"Sympy object of call: {latex(result_call)}")

        result_unknown = sympify_unknown(parsed_tuple_unknown)
        print(f"Sympy object of unknown: {latex(result_unknown)}")

        result_assignment = sympify_assignment(parsed_tuple_assignment)
        print(f"Sympy object of assignment: {latex(result_assignment)}")

        result_conditional = sympify_conditional(parsed_tuple_conditional)
        print(f"Sympy object of conditional: {latex(result_conditional)}")

        result_function = sympify_function(parsed_tuple_function)
        print(f"Sympy object of function: {latex(result_function)}")
    except ValueError as e:
        print(e)
