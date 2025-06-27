from latex import latexify_name, latexify_expression

class Assignment:
    def __init__(self, assignment_str):
        self.name, self.expression, self.value = split_assignment(assignment_str)
        self.latex_name = latexify_name(self.name)
        self.latex_expression = latexify_expression(self.expression)
        self.latex_value = self.value



def split_assignment(assignment_str):
    """
    Splits an assignment string into name, expression, and value.
    - name: variable name (lhs of '=' )
    - expression: rhs of '='
    - value: value of the variable in user_ns (if present), else None
    """
    lhs, rhs = assignment_str.split('=', 1)
    name = lhs.strip()
    expression = rhs.strip()
    value = None
    from IPython import get_ipython
    ip = get_ipython()
    if ip is not None and hasattr(ip, 'user_ns'):
        value = ip.user_ns.get(name, None)
    return name, expression, value