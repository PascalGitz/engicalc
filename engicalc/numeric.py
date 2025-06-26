def numeric_value(parsed_tuple):
    """
    Given a parsed assignment tuple, returns the numeric value of the assigned variable from the given namespace (defaults to globals()).
    """
    ipy = get_ipython()
    user_ns = ipy.user_ns
    typ, value = parsed_tuple
    if typ == 'assignment':
        if '=' not in value:
            raise ValueError("Assignment does not contain '=' sign.")
        lhs, rhs = value.split('=', 1)
        lhs = lhs.strip()
        rhs = rhs.strip()
        try:
            # Evaluate the right-hand side expression
            rhs_value = eval(rhs, user_ns)

            return rhs_value
        except Exception as e:
            raise ValueError(f"Error evaluating the expression '{rhs}': {e}")