from sympy import sympify, latex


def latexify_name(name):
    # Placeholder for substitution function, to be added later
    prepared = name  # In the future, apply substitution(prepared)
    sympy_obj = sympify(prepared, mul)
    return latex(sympy_obj)

def latexify_expression(expression):
    # Placeholder for substitution function, to be added later
    prepared = expression  # In the future, apply substitution(prepared)
    sympy_obj = sympify(prepared)
    return latex(sympy_obj)


