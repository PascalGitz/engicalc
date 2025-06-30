import inspect
from sympy import sympify, latex, SympifyError, Symbol, Matrix
import numpy as np
import IPython
import re

from engicalc.units import ureg, units
from engicalc.parsing import *



# Units substitution
replacements_units = {}
for unit in units.items():
    formatted_unit = r"\\mathrm{" + str(unit[1]) + "}"
    replacements_units[unit[0]] = f'Symbol("{formatted_unit.replace("deg", "°")}")'



# special characters.
replacements_specials ={
        #special characters
        'diam': r'\\oslash',
        'eps':'varepsilon', #convenience
        'infty': r'\\infty',
        'sum':r'\\sum',
}






def format_value(value, precision: float):
    """Formats the value based on its type."""
    # change the unit format to latex
    ureg.formatter.default_format = "~L"

    if isinstance(value, (int, float)):
        return round(value, precision)
    
    elif isinstance(value, np.ndarray):
        # Handle numpy arrays as matrices
        rounded_value = np.round(value, precision)
        matrix = Matrix(rounded_value.tolist())
        return latex(matrix)
    
    elif isinstance(value, list):
        # Handle lists as vectors
        formatted_list = [format_value(item, precision) for item in value]
        return formatted_list
    
    elif hasattr(value, "magnitude"):

        # replace the degree sign
        units = str(value.units)
        units = units.replace('deg','°')

        # Handle Pint quantities
        magnitude = np.round(value.magnitude, precision)
        if isinstance(magnitude, np.ndarray):
            # Handle numpy arrays of Pint quantities as matrices
            return f"{latex(Matrix(magnitude.tolist()))} \\ {latex(Symbol(units))}"
        else:
            # Handle scalar Pint quantities
            return f"{magnitude} \\ {latex(Symbol(units))}"
    else:
        return value

def format_symbolic(expr: str, evaluate: bool) -> str:
    """Formats the symbolic expression using sympy by applying a structured substitution process."""
    try:
        expr = apply_substitutions(expr)
        symbolic_expr = sympify(expr, evaluate=evaluate)
        return latex(symbolic_expr, mul_symbol='dot', order='none')
    except (SympifyError, TypeError, ValueError):
        return expr

def apply_substitutions(expr: str) -> str:
    """Applies all necessary substitutions in a structured order."""
    possible_prefixes = get_possible_prefixes()  # Retrieve module prefixes

    expr = substitute_numpy_functions(expr)  # Convert NumPy functions dynamically
    expr = substitute_pint_methods(expr, possible_prefixes)
    expr = substitute_units(expr, possible_prefixes)
    expr = substitute_special_characters(expr)

    return expr

def get_possible_prefixes() -> set:
    """Retrieve dynamically imported module prefixes, including NumPy's alias."""
    user_ns = IPython.get_ipython().user_ns  # Get global namespace
    possible_prefixes = {name for name, obj in user_ns.items() if inspect.ismodule(obj)}

    # Identify the alias used for NumPy
    for name, obj in user_ns.items():
        if obj is np:
            possible_prefixes.add(name)  # Add NumPy alias dynamically
    return possible_prefixes

def get_numpy_alias() -> str:
    """Detect the alias used for NumPy dynamically, filtering out direct 'numpy' imports."""
    user_ns = IPython.get_ipython().user_ns  # Get global namespace

    for name, obj in user_ns.items():
        try:
            # Ensure it's a module AND originates from NumPy
            if isinstance(obj, type(np)) and obj.__name__ == "numpy" and name != "numpy":
                return name  # Return the alias, NOT 'numpy'
        except AttributeError:
            continue  # Ignore non-modules
    
    return "numpy"  # NumPy alias not found


def substitute_numpy_functions(expr: str) -> str:
    """Replace NumPy functions with their SymPy equivalents, using the detected alias."""
    
    numpy_alias = get_numpy_alias()  # Detect NumPy alias dynamically

    if numpy_alias:
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
            f'{numpy_alias}.dot': '*',  # Convert matrix multiplication
            f'{numpy_alias}.pi': 'pi',  # Convert matrix multiplication
        }

        for np_func, sympy_func in numpy_to_sympy.items():
            expr = expr.replace(np_func, sympy_func)  # Replace dynamically
        
    return expr


def substitute_pint_methods(expr: str, possible_prefixes: set) -> str:
    """Handles `.m` and `.magnitude`, keeping `.m` if it has a valid prefix."""
    
    # Step 1: Remove `.magnitude`
    expr = re.sub(r'\.magnitude\b', '', expr)
    
    # Step 2: Explicitly check prefixes instead of using a regex pattern
    tokens = expr.split()  # Split expression into tokens for processing
    cleaned_tokens = []
    
    for token in tokens:
        # If the token has `.m`, check if the prefix is in possible_prefixes
        if ".m" in token:
            prefix = token.split(".")[0]  # Extract prefix before `.m`
            if prefix not in possible_prefixes:  
                token = token.replace(".m", "")  # Remove `.m` only if prefix isn't valid
        
        cleaned_tokens.append(token)
    
    expr = " ".join(cleaned_tokens)  # Reconstruct expression
    
    # Step 3: Remove `.to(...)` unit conversions
    expr = re.sub(r'\.to\(\s*[^)]*\)', '', expr)
    
    return expr

def substitute_units(expr: str, possible_prefixes: set) -> str:
    """Replace unit names with corresponding SymPy symbols, handling dynamic prefixes."""
    sorted_keys = sorted(replacements_units.keys(), key=len, reverse=True)
    for key in sorted_keys:
        pattern = rf'\b(?:{"|".join(possible_prefixes)})?\.{key}\b|\b{key}\b'
        expr = re.sub(pattern, replacements_units[key], expr)
    return expr

def substitute_special_characters(expr: str) -> str:
    """Wrap special variable names in SymPy Symbol() and replace special characters."""

    def replace_variables(match):
        var_name = match.group(0)
        for entry in global_expressions:
            if var_name == entry['variable_name']:
                return f'Symbol("{var_name}")'
        return var_name

    expr = re.sub(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', replace_variables, expr)
    
    for key, value in replacements_specials.items():
        expr = expr.replace(key, value)
    
    return expr
