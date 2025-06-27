from sympify import sympify_assignment, sympify_conditional
from numeric import *
from parsing import parse
from sympy import latex

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
    typ, value = parsed_tuple
    if typ == 'assignment':
        name, symbolic = sympify_assignment(parsed_tuple)
        numeric = numeric_value(parsed_tuple)
        parts = []
        if show_name:
            parts.append(f"{latex(name)}")
        if show_symbolic:
            parts.append(f"{latex(symbolic)}")
        if show_numeric:
            parts.append(f"{numeric}")
        return r" = ".join(parts)

def latex_conditional(parsed_tuple):
    """
    Returns a LaTeX string for a conditional assignment in the form:
    symbolic_conditional = numeric_value
    - parsed_tuple: a tuple (type, content) as returned by parse(code)
    Detects if the tuple is a conditional assignment.
    """
    typ, value = parsed_tuple
    # Detect if the assignment is a conditional (contains 'if' and 'else')
    if typ == 'conditional':
        symbolic = sympify_conditional(parsed_tuple)
        numeric = numeric_conditional(parsed_tuple)
        return f"{latex(symbolic)} = {latex(numeric)}"

def do_latex(parsed_tuples):
    """
    Takes a list of parsed tuples and returns a list of LaTeX strings by dispatching to the correct latex function.
    """
    result = []
    for parsed in parsed_tuples:
        typ = parsed[0]
        if typ == 'assignment':
            obj = latex_assignment(parsed)
            result.append(obj)
        elif typ == 'conditional':
            obj = latex_conditional(parsed)
            result.append(obj)
        # Optionally, add more types if needed
    return result
