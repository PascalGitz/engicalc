from IPython.display import display, Markdown
import io
from contextlib import redirect_stdout
import numpy as np
from sympy import Matrix, latex, Symbol, sympify, SympifyError
import re

def cell_parser(offset=0) -> list:
    ipy = get_ipython()
    out = io.StringIO()

    # Capture the history of executed commands
    with redirect_stdout(out):
        ipy.run_line_magic("history", f"{ipy.execution_count - offset}")

    # Extract variable names and expressions from the captured output
    lines = out.getvalue().split("\n")

    parsed_lines = []
    conditional_stack = []

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith(('if', 'elif', 'else')):
            conditional_stack.append(stripped_line)
            parsed_lines.append(('conditional', stripped_line))
        elif '=' in stripped_line:
            if conditional_stack:
                current_conditional = conditional_stack[-1]
                parsed_lines.append(('assignment', stripped_line, current_conditional))
            else:
                parsed_lines.append(('assignment', stripped_line, None))
        else:
            parsed_lines.append(('other', stripped_line))

    return parsed_lines

def build_conditional_equation(parsed_lines: list, symbolic: bool = True) -> str:
    """Builds a Latex equation for conditionals and their corresponding assignments."""
    equations = []
    current_conditional = None

    for line_type, line, *conditional in parsed_lines:
        if line_type == 'conditional':
            current_conditional = line
        elif line_type == 'assignment':
            equation = build_equation(line, symbolic)
            if current_conditional:
                equation = f"{current_conditional}\n{equation}"
                current_conditional = None  # Reset after using
            equations.append(equation)
    
    return "\n".join(equations)

def build_equation(line: str, symbolic: bool = True) -> str:
    """Builds a Latex equation from a parsed assignment line."""
    # Split the line by the '=' sign
    lhs, rhs = line.split('=')
    
    # Strip any leading/trailing whitespace
    lhs = lhs.strip()
    rhs = rhs.strip()
    
    # Format the left-hand side and right-hand side symbolically
    lhs_symbolic = format_symbolic(lhs)
    rhs_symbolic = format_symbolic(rhs)
    
    # Evaluate the right-hand side to get the numerical value
    try:
        rhs_value = eval(rhs)
        rhs_value_formatted = format_value(rhs_value)
    except Exception as e:
        rhs_value_formatted = f"Error evaluating: {e}"
    
    # Construct the Latex equation
    if symbolic:
        equation = f"{lhs_symbolic} = {rhs_symbolic} = {rhs_value_formatted}"
    else:
        equation = f"{lhs_symbolic} = {rhs_value_formatted}"
    
    return equation

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

    # Replace unit registry and unit conversions with ''
    expr = re.sub(r'un\.\w+', '', expr)
    expr = re.sub(r'ureg\.\w+', '', expr)
    expr = re.sub(r'\.to\([^\)]+\)', '', expr)  # Remove unit conversions

    # Apply other replacements
    for key, value in replacements_pint.items():
        expr = expr.replace(key, value)
    
    return expr

def put_out(precision: float = 2, symbolic: bool = True, offset: int = 0, rows: int = 1, evaluate: bool = False):
    """Constructs and displays the final Markdown output."""
    parsed_lines = cell_parser(offset)
    equations = build_conditional_equation(parsed_lines, symbolic==symbolic, evaluate=evaluate, precision=precision)

    # Horizontal display with aligned '=' signs
    var_list = list(enumerate(equations))

    if len(var_list) == 0:
        return 
    elif len(var_list) < rows:
        rows = len(var_list)

    markdown_str = "$$\n\\begin{aligned}\n"
    for i in range(0, len(var_list), rows):
        row = var_list[i : i + rows]
        row_str = " \\quad & ".join(
            [f"{var_name} & = {expr_and_result}" for var_name, expr_and_result in row]
        )
        if len(row) < rows and rows != 1:
            row_str += " \\quad & " * (rows - len(row)) + " \n"

        markdown_str += row_str + " \\\\ \n"

    if markdown_str.endswith(" \\\\ \n"):
        markdown_str = markdown_str[:-4]
    markdown_str += "\\end{aligned}\n$$"

    display(Markdown(markdown_str))

