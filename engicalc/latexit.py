from sympy import Piecewise, And, Or, Symbol
import ast
from .subs import do_substitution
import numpy as np
import re



from sympy import sympify as sympy_sympify
def so(expr):
    """Wrapper for sympy.sympify with evaluate=False."""
    return sympy_sympify(expr, evaluate=False)

from sympy import latex as sympy_latex
def ltex(expr):
    """Wrapper for sympy.sympify with evaluate=False."""
    return sympy_latex(expr, mul_symbol='dot', ln_notation = True, order='none').replace('\\cdot', '\\')


def latexify_name(name):
    # Placeholder for substitution function, to be added later
    prepared = do_substitution(name)  # In the future, apply substitution(prepared)
    sympy_obj = so(prepared)
    return ltex(sympy_obj)

def latexify_expression(expression):
    # Placeholder for substitution function, to be added later
    prepared = do_substitution(expression) # In the future, apply substitution(prepared)
    sympy_obj = so(prepared)
    return ltex(sympy_obj)

def latexify_value(value_str, precision=4):
    """
    Converts a string representing a value to a LaTeX string using sympy.latex.
    The precision of floats can be adjusted with the precision argument.
    Rounds the value, splits by space, applies do_substitution, sympify, and latex to the RHS, then joins back.
    """
    if value_str is not None:
        val = value_str
        val = np.round(val, precision)
        # print(val)

        # replace blankspaces inside brackets with ,
        def replace_inside(match):
            inner = match.group(1)
            return inner.replace(' ', ',')
        pattern = r'(?<=\[)([^]]+)(?=\])'
        val = re.sub(pattern, replace_inside, str(val))
        # print(val)

        # replace blankspaces between number and unit with *
        pattern = r'(?<=\d|\])\s+(?=[A-Za-zµ%‰/])'
        val = re.sub(pattern, '*', str(val))
        # print(val)

        val = str(val).replace('*/', '/', 1) #dirty hack again

        val = do_substitution(val).replace('%', "Symbol('\\%')").replace('‰', "Symbol('‰')") # dirty hack for special signs
        val = so(val)
        val = ltex(val)
        return (val) 






