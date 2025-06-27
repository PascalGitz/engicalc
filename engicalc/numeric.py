from IPython import get_ipython
from sympy import Symbol, Eq

def numeric_eval(expr):
    """
    Given a sympy object (from do_sympify), returns the numeric value by evaluating the right-hand side
    of the object with symbol values from the IPython user namespace.
    For function calls like x = f_c(2,3), if subs on rhs does not yield a numeric value, try lhs.
    """
    ipy = get_ipython()
    if ipy is None:
        raise RuntimeError("Not running inside an IPython environment.")
    user_ns = ipy.user_ns
    if expr is None:
        raise ValueError("Input sympy object is None.")
    # Always use the right-hand side if expr is Eq
    if isinstance(expr, Eq):
        rhs = expr.rhs
        lhs = expr.lhs
        symbols_rhs = rhs.free_symbols
        subs = {s: user_ns.get(str(s), s) for s in symbols_rhs}
        try:
            numeric = rhs.subs(subs)
            # If still symbolic, try lhs
            if numeric == rhs:
                symbols_lhs = lhs.free_symbols
                subs_lhs = {s: user_ns.get(str(s), s) for s in symbols_lhs}
                numeric = lhs.subs(subs_lhs)
            return numeric
        except Exception as e:
            raise ValueError(f"Error evaluating the numeric value: {e}")
    else:
        symbols = expr.free_symbols
        subs = {s: user_ns.get(str(s), s) for s in symbols}
        try:
            numeric = expr.subs(subs)
            return numeric
        except Exception as e:
            raise ValueError(f"Error evaluating the numeric value: {e}")