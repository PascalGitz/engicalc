from .latexit import latexify_name, latexify_expression, latexify_value

class Name:
    def __init__(self, name_str, show_name=True, show_expression=True, show_value=True, precision=4):
        self.show_name = show_name
        self.show_expression = show_expression  
        self.show_value = show_value
        self.precision = precision

        self.name, self.value = split(name_str)
        self.latex_name = latexify_name(self.name)
        self.latex_value = latexify_value(self.value, self.precision)
        self.latex_equation = self.build_latex_equation()
        
    def build_latex_equation(self):
        parts = []
        if self.show_name:
            parts.append(self.latex_name)
        if self.show_value and self.latex_value is not None:
            parts.append(self.latex_value)
        return "=".join(parts)


def split(name_str):
    """
    Splits an assignment string into name, expression, and value.
    - name: variable name (lhs of '=' )
    - expression: rhs of '='
    - value: value of the variable in user_ns (if present), else None
    """
    name = name_str
    from IPython import get_ipython
    ip = get_ipython()
    if ip is not None and hasattr(ip, 'user_ns'):
        value = ip.user_ns.get(name, None)
    return name,  value