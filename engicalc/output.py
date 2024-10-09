import io
from contextlib import redirect_stdout
from sympy import sympify, latex, SympifyError, Symbol, Matrix
import numpy as np
from IPython.display import display, Markdown
import re


defined_variable_names = []


def cell_parser(offset: int) -> dict:

    ipy = get_ipython()
    out = io.StringIO()

    # Capture the history of executed commands
    with redirect_stdout(out):
        ipy.run_line_magic("history", f"{ipy.execution_count - offset}")

    # Get the current variables and their values from the user namespace
    user_ns = ipy.user_ns

    # Extract variable names and expressions from the captured output
    lines = out.getvalue().replace(" ", "").split("\n")
    variable_data = []

    for line in lines:
        if "=" in line:
            # Split by '=' to separate the variable name and the expression
            variable_name, expression = line.split('=', 1)

            if variable_name in user_ns:
                result = user_ns[variable_name]
                variable_data.append({
                    'variable_name': variable_name,
                    'expression': expression,
                    'result': result
                })
                defined_variable_names.append(variable_name)

        # Also capture single variable names without an assignment, that have been previously defined
        elif line in user_ns:
            variable_name = line
            result = user_ns[variable_name]
            variable_data.append({
                'variable_name': variable_name,
                'expression': variable_name,  # Expression is just the variable name
                'result': result
            })

    return variable_data

def format_value(value, precision: float):
    """Formats the value based on its type."""
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
        # Handle Pint quantities
        magnitude = np.round(value.magnitude, precision)
        if isinstance(magnitude, np.ndarray):
            # Handle numpy arrays of Pint quantities as matrices
            return f"{latex(Matrix(magnitude.tolist()))} \\ {latex(Symbol(str(value.units)))}"
        else:
            # Handle scalar Pint quantities
            return f"{magnitude} \\ {latex(Symbol(str(value.units)))}"
    else:
        return value

def format_symbolic(expr: str, evaluate: bool) -> str:
    """Formats the symbolic expression using sympy."""
    try:
        # do the package substitution
        expr = substitute_numpy(expr)
        expr = substitute_pint(expr)
        expr = substitute_engicalc(expr)
        expr = substitute_special_characters(expr)
        symbolic_expr = sympify(expr, evaluate=evaluate)
        return latex(symbolic_expr, mul_symbol = 'dot')
    except (SympifyError, TypeError, ValueError):
        return expr

def substitute_numpy(expr: str) -> str:
    replacements = {
        'np.': '', 
        'array': 'Matrix',
    }
    for key, value in replacements.items():
        expr = expr.replace(key, value)
    return expr

def substitute_pint(expr: str) -> str:
    replacements = {
        '.m': '',
        '.magnitude': '',
    }

    # Replace unit registry and unit conversions with a space
    expr = re.sub(r'\.to\([^\)]+\)', '', expr)  # Remove unit conversions
    expr = re.sub(r'[\*/]?\s*un\.\w+(\*\*\d+)?', '', expr)
    expr = re.sub(r'[\*/]?\s*ureg\.\w+(\*\*\d+)?', '', expr)

    # Apply other replacements
    for key, value in replacements.items():
        expr = expr.replace(key, value)
    
    return expr

def substitute_special_characters(expr: str) -> str:
    replacements = {
        'com': ',',
        'diam': '\oslash',
        'apos':"^'",

    }

    # Function to wrap all variable names in sympy.Symbol()
    def replace_variables(match):
        var_name = match.group(0)
        if var_name in defined_variable_names:
            # Return a sympy-compatible symbol expression
            return f'Symbol("{var_name}")'
        else:
            return var_name
        
    # Use regex to find all valid variable names (e.g., alphanumeric and underscores)
    # Modify this regex if you have specific naming conventions
    expr = re.sub(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', replace_variables, expr)

    # Apply other replacements
    for key, value in replacements.items():
        expr = expr.replace(key, value)
    
    return expr

def substitute_engicalc(expr: str) -> str:
    replacements = {

    }

    # Replace unit registry and unit conversions with a space
    expr = re.sub(r'ecc.', '', expr)

    # Apply other replacements
    for key, value in replacements.items():
        expr = expr.replace(key, value)
    
    return expr

def build_equation(assignment:dict, precision: float, symbolic: bool, numeric: bool, evaluate: bool):
    var = format_symbolic(assignment['variable_name'], evaluate=evaluate)
    expression = format_symbolic(assignment['expression'], evaluate=evaluate)    
    result = format_value(assignment['result'], precision=precision)

    if symbolic == False:
        equation = f'{var}& = {result}'
    if numeric == False:
        equation = f'{var}& = {expression}'
    if numeric ==True and symbolic == True:
        equation = f'{var}& = {expression} = {result}'

    return equation

def put_out(precision: float = 2, symbolic: bool = False, evaluate: bool = False, numeric: bool = True, offset: int = 0, rows: int = 3):
    """Constructs and displays the final Markdown output."""
    parsed_lines = cell_parser(offset)
    equations = [build_equation(assignment = eq, symbolic=symbolic, numeric = numeric,  precision=precision, evaluate=evaluate) for eq in parsed_lines]

    markdown_str = "$$\n\\begin{aligned}\n"
    for i in range(0, len(equations), rows):
        row = equations[i : i + rows]
        row_str = " \\quad & ".join(
            [f"{eq}" for eq in row]
        )
        if len(row) < rows and rows != 1:
            row_str += " \\quad & " * (rows - len(row)) + " \n"

        markdown_str += row_str + " \\\\ \n"

    if markdown_str.endswith(" \\\\ \n"):
        markdown_str = markdown_str[:-4]
    markdown_str += "\\end{aligned}\n$$"
    display(Markdown(markdown_str))
