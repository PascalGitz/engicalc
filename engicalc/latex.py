from sympify import sympify_assignment
from numeric import numeric_value
from parsing import parse

def latex_assignment(parsed_tuple, show_name=True, show_symbolic=True, show_numeric=True):
    """
    Returns a LaTeX string for an assignment in the form:
    name = symbolic = numeric
    Each part can be toggled with the show_* arguments.
    - parsed_tuple: a tuple (type, content) as returned by parse(code)
    - show_name: whether to show the variable name
    - show_symbolic: whether to show the symbolic expression
    - show_numeric: whether to show the numeric value
    """
    typ, assignment_str = parsed_tuple
    if typ != "assignment":
        raise ValueError("Input tuple must be of type 'assignment'.")
    name, symbolic = sympify_assignment(parsed_tuple)
    numeric = numeric_value(parsed_tuple)
    parts = []
    if show_name:
        parts.append(f"{name}")
    if show_symbolic:
        parts.append(f"{symbolic}")
    if show_numeric:
        parts.append(f"{numeric}")
    return r" = ".join(parts)
