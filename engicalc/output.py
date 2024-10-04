import io
from contextlib import redirect_stdout
from sympy import sympify, latex, SympifyError, Symbol, Matrix
import numpy as np
from IPython.display import display, Markdown
import re

import ast
import io
from contextlib import redirect_stdout

import ast
import io
from contextlib import redirect_stdout

def cell_parser(offset: int = 0) -> dict:

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

    return variable_data



def format_value(value, precision: float = 2):
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

def format_symbolic(expr: str, evaluate: bool = False) -> str:
    """Formats the symbolic expression using sympy."""
    try:
        symbolic_expr = sympify(expr, evaluate=evaluate)
        return latex(symbolic_expr)
    except (SympifyError, TypeError, ValueError):
        return expr

def substitute_numpy(expr: str) -> str:
    replacements_numpy = {
        'np.': '', 
        'array': 'Matrix',
    }
    for key, value in replacements_numpy.items():
        expr = expr.replace(key, value)
    return expr

def substitute_pint(expr: str) -> str:
    replacements_pint = {
        '.m': '',
        '.magnitude': '',
    }

    # Replace unit registry and unit conversions with a space
    expr = re.sub(r'un\.\w+', ' ', expr)
    expr = re.sub(r'ureg\.\w+', ' ', expr)
    expr = re.sub(r'\.to\([^\)]+\)', '', expr)  # Remove unit conversions

    # Apply other replacements
    for key, value in replacements_pint.items():
        expr = expr.replace(key, value)
    
    return expr

def format_equation(line: str, rhs_value, symbolic: bool = True, evaluate: bool = False, precision: float = 2) -> str:
    """Builds a Markdown equation from a parsed assignment line."""
    # Split the line by the '=' sign
    lhs, rhs = line.split('=')
    
    # Strip any leading/trailing whitespace
    lhs = lhs.strip()
    rhs = rhs.strip()
    
    # Substitute numpy and pint expressions
    lhs = substitute_numpy(lhs)
    lhs = substitute_pint(lhs)
    rhs = substitute_numpy(rhs)
    rhs = substitute_pint(rhs)
    
    # Format the left-hand side and right-hand side symbolically
    lhs_symbolic = format_symbolic(lhs, evaluate=evaluate)
    rhs_symbolic = format_symbolic(rhs, evaluate=evaluate)
    
    # Format the numerical value
    rhs_value_formatted = format_value(rhs_value, precision)
    
    # Construct the Markdown equation
    if symbolic:
        equation = f"{lhs_symbolic} = {rhs_symbolic} = {rhs_value_formatted}"
    else:
        equation = f"{lhs_symbolic} = {rhs_value_formatted}"
    
    return equation

def build_equations(parsed_lines: list, symbolic: bool = True, evaluate: bool = False, precision: float = 2) -> list:
    """Builds a list of Markdown equations from parsed assignment lines."""
    equations = []

    for line_type, line, rhs_value in parsed_lines:
        if line_type == 'assignment':
            equation = format_equation(line, rhs_value, symbolic, evaluate, precision)
            equations.append(equation)
    
    return equations

def put_out(precision: float = 2, symbolic: bool = True, offset: int = 0, rows: int = 1, evaluate: bool = False):
    """Constructs and displays the final Markdown output."""
    parsed_lines = cell_parser(offset)
    equations = build_equations(parsed_lines, symbolic=symbolic, evaluate=evaluate, precision=precision)

    print(equations)