from IPython import get_ipython
from sympy import Symbol, Eq

def numeric_eval(expr):
    """
    Given a sympy Eq object, looks up the lhs name in the IPython user namespace and returns its numeric value.
    If not found, returns None.
    """
    ipy = get_ipython()
    if ipy is None:
        raise RuntimeError("Not running inside an IPython environment.")
    user_ns = ipy.user_ns
    if expr is None:
        raise ValueError("Input sympy object is None.")
    if isinstance(expr, Eq):
        lhs = expr.lhs
        lhs_name = str(lhs)
        return user_ns.get(lhs_name, None)
    else:
        raise ValueError("Input must be a sympy Eq object for variable lookup.")