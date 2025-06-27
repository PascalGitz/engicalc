import ast
from latex import latexify_name, latexify_expression, latexify_conditional



class Conditional:
    def __init__(self, conditional_str):
        self.name, self.expression, self.value = split(conditional_str)
        self.latex_name = latexify_name(self.name)
        self.latex_expression = latexify_conditional(self.expression)
        self.latex_value = self.value

def split(parsed_str):
    """
    Splits a conditional string into name, expression (list of (condition, expr)), and value (from user_ns).
    - name: variable assigned in all branches
    - expression: list of (condition, expr) tuples
    - value: value of the variable in user_ns (if present), else None
    """
    tree = ast.parse(parsed_str)
    # Find the first If node
    if_node = next((node for node in tree.body if isinstance(node, ast.If)), None)
    branches = []
    name = None
    # Helper to extract assignment from a node's body
    def get_assign_info(body):
        for stmt in body:
            if isinstance(stmt, ast.Assign):
                target = stmt.targets[0]
                if hasattr(target, 'id'):
                    return target.id, ast.unparse(stmt.value)
        return None, None
    # Main if branch
    n, expr = get_assign_info(if_node.body)
    name = n
    branches.append((ast.unparse(if_node.test), expr))
    # Elif/Else branches
    orelse = if_node.orelse
    while orelse:
        first = orelse[0]
        if isinstance(first, ast.If):
            n, expr = get_assign_info(first.body)
            branches.append((ast.unparse(first.test), expr))
            orelse = first.orelse
        else:
            n, expr = get_assign_info(orelse)
            branches.append(("else", expr))
            break
    # Get value from user_ns
    value = None
    from IPython import get_ipython
    ip = get_ipython()
    if ip is not None and hasattr(ip, 'user_ns') and name:
        value = ip.user_ns.get(name, None)
    return name, branches, value