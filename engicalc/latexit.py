from sympy import sympify, latex, Piecewise
import ast
from sympy import And, Or
from subs import do_substitution


def latexify_name(name):
    # Placeholder for substitution function, to be added later
    prepared = do_substitution(name)  # In the future, apply substitution(prepared)
    sympy_obj = sympify(prepared)
    return latex(sympy_obj, mul_symbol='dot', order='none')

def latexify_expression(expression):
    # Placeholder for substitution function, to be added later
    prepared = do_substitution(expression)  # In the future, apply substitution(prepared)
    sympy_obj = sympify(prepared)
    return latex(sympy_obj, mul_symbol='dot', order='none')

def latexify_conditional(expr_cond_list):
    """
    Takes a list of (condition, expression) tuples, parses conditions to sympy logic,
    constructs a sympy.Piecewise, and returns its LaTeX representation.
    """
    sympy_tuples = []
    for cond, expr in expr_cond_list:
        cond_obj = _parse_condition_to_sympy(cond) if cond != 'else' else True
        expr_obj = sympify(do_substitution(expr))
        sympy_tuples.append((expr_obj, cond_obj))
    pw = Piecewise(*sympy_tuples)
    return latex(pw, mul_symbol='dot', order='none')

def _parse_condition_to_sympy(cond_str):
    """
    Parse a Python condition string into a sympy logical expression using ast.
    """
    cond_str = do_substitution(cond_str)
    tree = ast.parse(cond_str, mode='eval')
    def _convert(node):
        if isinstance(node, ast.BoolOp):
            values = [_convert(v) for v in node.values]
            if isinstance(node.op, ast.And):
                return And(*values)
            elif isinstance(node.op, ast.Or):
                return Or(*values)
        elif isinstance(node, ast.Compare):
            left = sympify(do_substitution(ast.unparse(node.left)))
            rights = [sympify(do_substitution(ast.unparse(comp))) for comp in node.comparators]
            ops = node.ops
            result = left
            for op, right in zip(ops, rights):
                if isinstance(op, ast.Lt):
                    result = result < right
                elif isinstance(op, ast.LtE):
                    result = result <= right
                elif isinstance(op, ast.Gt):
                    result = result > right
                elif isinstance(op, ast.GtE):
                    result = result >= right
                elif isinstance(op, ast.Eq):
                    result = result == right
                elif isinstance(op, ast.NotEq):
                    result = result != right
            return result
        else:
            return sympify(do_substitution(ast.unparse(node)))
    return _convert(tree.body)

def latexify_value(value_str, precision=4):
    """
    Converts a string representing a value to a LaTeX string using sympy.latex.
    The precision of floats can be adjusted with the precision argument.
    Rounds the value, splits by space, applies do_substitution, sympify, and latex to the RHS, then joins back.
    """
    if value_str is not None:
        val = value_str
        val = round(val, precision)
        parts = str(val).split(' ', 1)
        if len(parts) == 2:
            lhs, rhs = parts
            rhs = do_substitution(rhs)
            rhs = sympify(rhs)
            rhs = latex(rhs, mul_symbol='dot', order='none')
            formatted = f"{lhs} \ {rhs}"
        else:
            formatted = str(val)
        return formatted





