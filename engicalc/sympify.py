from sympy import sympify, Eq, Piecewise, And, Or
from engicalc.parsing import parse
import ast


def sympify_assignment(value):
    """
    Splits at '=', sympifies lhs as name and rhs as expression, and returns sympy.Eq(lhs, rhs).
    """
    if '=' not in value:
        raise ValueError("Assignment does not contain '=' sign.")
    lhs, rhs = value.split('=', 1)
    lhs = lhs.strip()
    rhs = rhs.strip()
    lhs_sym = sympify(lhs)
    rhs_sym = sympify(rhs)
    return Eq(lhs_sym, rhs_sym)

def sympify_conditional(value):
    """
    Parses a multi-branch conditional assignment (if/elif/else), each with a single assignment.
    Handles 'and'/'or' conditions by converting them to sympy logical expressions.
    Extracts the assignment name, each condition, and each expression, builds a Piecewise, and returns Eq(lhs, Piecewise(...)).
    """

    def parse_condition(test_node):
        # Recursively convert ast.BoolOp to sympy And/Or
        if isinstance(test_node, ast.BoolOp):
            op = test_node.op
            values = [parse_condition(v) for v in test_node.values]
            if isinstance(op, ast.And):
                return And(*values)
            elif isinstance(op, ast.Or):
                return Or(*values)
        elif isinstance(test_node, ast.Compare):
            return sympify(ast.unparse(test_node).strip())
        elif isinstance(test_node, ast.Name):
            return sympify(test_node.id)
        else:
            return sympify(ast.unparse(test_node).strip())

    tree = ast.parse(value)
    node = tree.body[0]
    if not isinstance(node, ast.If):
        raise ValueError("Not a conditional statement (if/elif/else block).")
    pieces = []
    name = None
    def handle_branch(assign_node, cond):
        nonlocal name
        assign_str = ast.unparse(assign_node).strip()
        eq_obj = sympify_assignment(assign_str)
        lhs = eq_obj.lhs
        rhs = eq_obj.rhs
        if name is None:
            name = lhs
        elif name != lhs:
            raise ValueError("All assignments in the conditional must assign to the same variable.")
        pieces.append((rhs, cond))
    current = node
    while True:
        # Handle if/elif
        if len(current.body) != 1 or not isinstance(current.body[0], ast.Assign):
            raise ValueError("Each conditional body must contain a single assignment.")
        cond = parse_condition(current.test)
        handle_branch(current.body[0], cond)
        if current.orelse:
            if isinstance(current.orelse[0], ast.If):
                current = current.orelse[0]
            else:
                # else block
                if len(current.orelse) != 1 or not isinstance(current.orelse[0], ast.Assign):
                    raise ValueError("Else block must contain a single assignment.")
                handle_branch(current.orelse[0], True)
                break
        else:
            break
    return Eq(name, Piecewise(*pieces))

def sympify_function(value):
    """
    Uses ast to extract the function name, parameters, and return statement. Creates an assignment from the function name (with parameters) and return value, sympifies it, and sympifies the rest of the body. Returns all sympified objects.
    """
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
    assignment_obj = sympify_assignment(assignment_str)
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
        typ, value = parsed
        if typ == 'assignment':
            obj = sympify_assignment(value)
            result.append(obj)
        elif typ == 'conditional':
            obj = sympify_conditional(value)
            result.append(obj)
        elif typ == 'function':
            objs = sympify_function(value)
            result.extend(objs)

    return result

