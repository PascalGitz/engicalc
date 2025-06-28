import re
from sympy import Symbol
from units import units 

def do_substitution(input_str):
    """
    Applies all substitution functions to the input string and returns the result.
    """
    s = substitute_numpy(input_str)
    s = substitute_pint(s)
    s = substitute_specials(s)
    s = substitute_units(s)
    return s

def substitute_numpy(input_str):
    """
    Replaces numpy functions in the input string with their sympy equivalents, using detected numpy alias.
    """
    imports = get_import_aliases()
    numpy_alias = None
    for alias, module in imports.items():
        if module == 'numpy':
            numpy_alias = alias
            break
    if numpy_alias is None:
        numpy_alias = 'np'  # fallback if not found

    numpy_to_sympy = {
        f'{numpy_alias}.sin': 'sin',
        f'{numpy_alias}.asin': 'asin',
        f'{numpy_alias}.cos': 'cos',
        f'{numpy_alias}.acos': 'acos',
        f'{numpy_alias}.tan': 'tan',
        f'{numpy_alias}.atan': 'atan',
        f'{numpy_alias}.exp': 'exp',
        f'{numpy_alias}.log': 'log',
        f'{numpy_alias}.sqrt': 'sqrt',
        f'{numpy_alias}.abs': 'Abs',
        f'{numpy_alias}.array': 'Matrix',
        f'{numpy_alias}.dot': '*',
        f'{numpy_alias}.pi': 'pi',
    }
    
    result = input_str
    for np_func, sympy_func in numpy_to_sympy.items():
        result = re.sub(rf'\b{re.escape(np_func)}\b', sympy_func, result)
    return result

def substitute_specials(input_str):
    """
    Identifies variable names in a string and replaces special substrings inside them using replacements_specials.
    The entire variable name is wrapped in Symbol("...") if any special substring is present (after replacement).
    """
    replacements_specials = {
        'diam': r'\\oslash',
        'eps': 'varepsilon',
        'infty': r'\\infty',
        'sum': r'\\sum',
    }
    var_pattern = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
    def repl(match):
        var = match.group(0)
        replaced = var
        for special, replacement in replacements_specials.items():
            if special in replaced:
                replaced = replaced.replace(special, replacement)
        if replaced != var:
            return f'Symbol("{replaced}")'
        return var
    return re.sub(var_pattern, repl, input_str)



def get_import_aliases():
    """
    Retrieves all package imports and their aliases from the user_ns.
    Returns a dict: {alias: module_name}
    """
    imports = {}
    from IPython import get_ipython
    ip = get_ipython()
    if ip is not None and hasattr(ip, 'user_ns'):
        user_ns = ip.user_ns
        for var, val in user_ns.items():
            # Check if the variable is a module
            if hasattr(val, '__name__'):
                imports[var] = val.__name__
    return imports

def substitute_units(input_str):
    """
    Replaces unit names (with engicalc alias if present) with nonitalic representations using a static units dict.
    Removes the alias + '.' from the string.
    Works for units directly after numbers or operators (e.g., 3*deg, 5deg, etc.).
    Wraps the formatted unit in a Symbol container.
    """
    # Dynamically get the engicalc alias
    imports = get_import_aliases()
    engicalc_alias = None
    for alias, module in imports.items():
        if module == 'engicalc':
            engicalc_alias = alias
            break
    # Remove alias + '.' from string
    if engicalc_alias:
        input_str = re.sub(f"{engicalc_alias}\\.", "", input_str)
    # Use the provided units dict (keys as replacors)
    for unit_name, unit_variable in units.items():
        formatted_unit = r"\\\\mathrm{\\\\ "+str(unit_variable).replace('deg', '°') + "}"
        symbol_unit = f'Symbol("{formatted_unit}")'
        # Match unit at word boundary or after number/operator
        input_str = re.sub(rf'(?<![a-zA-Z_]){re.escape(unit_name)}(?![a-zA-Z_])', symbol_unit, input_str)
    return input_str

def substitute_pint(input_str):
    """
    Removes .m, .magnitude, and .to(xx) from the input string using regex.
    """
    # Remove .m and .magnitude
    s = re.sub(r'\.magnitude', '', input_str)
    s = re.sub(r'\.m\b', '', s)
    # Remove .to(anything)
    s = re.sub(r'\.to\([^)]*\)', '', s)
    return s