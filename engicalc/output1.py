from IPython.display import display, Markdown, Latex
import io
import re
from contextlib import redirect_stdout
from sympy import Symbol, latex, Matrix, sympify, SympifyError
import sympy as sp
import numpy as np
from tabulate import tabulate


def parse_cell_variables(offset: int = 0) -> dict:
    """
    Parses the cell history to extract variable names, their corresponding expressions, and values.
    For Pint objects, strips the units and only uses the magnitudes in expressions.

    Args:
        offset (int): The number of previous cells to include for variable extraction. Defaults to 0.

    Returns:
        dict: A dictionary with 'variable_name', 'expression', and 'result' for each variable.
    """
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
            magnitude_str = np.array2string(magnitude, separator=",")
            return f"{latex(Matrix(magnitude.tolist()))} \\ {latex(Symbol(str(value.units)))}"
        else:
            # Handle scalar Pint quantities
            return f"{magnitude} \\ {latex(Symbol(str(value.units)))}"
    else:
        return value

def format_expression(expression: str, evaluate=True) -> str:
    """
    Formats a string expression into a SymPy expression and returns it as a LaTeX formatted string.
    Handles `Pint` and `numpy` objects by preprocessing the expression to ensure compatibility with SymPy.

    Args:
        expression (str): The mathematical expression as a string.

    Returns:
        str: The LaTeX formatted version of the expression or the original string if sympify fails.
    """
    # Preprocess the expression to replace Pint/numpy specific syntax
    expression = preprocess_expression(expression)

    try:
        # Convert the string to a SymPy expression
        sympy_expr = sympify(expression, evaluate=evaluate)

        # Convert the SymPy expression to LaTeX format for display
        latex_expr = latex(sympy_expr)

        return latex_expr

    except:
        # If the expression cannot be parsed, return the original string
        return expression

def preprocess_expression(expression: str) -> str:
    """
    Preprocesses the input expression to replace Pint and numpy-specific functions with SymPy-compatible equivalents.

    Args:
        expression (str): The original expression string.

    Returns:
        str: The preprocessed expression.
    """
    # Replace numpy functions with equivalent sympy functions if needed
    # Example replacements: you can expand this as per your needs
    numpy_to_sympy = {
        'np.': '', 
        'array': 'Matrix',
    }
    pint_to_sympy = {
        '.m': '',
        '.magnitude': '',
    }

    for key in numpy_to_sympy.keys():
        expression = expression.replace(key, numpy_to_sympy[key])
    
    expression = re.sub(r'un\.\w+', '1', expression)
    expression = re.sub(r'ureg\.\w+', '1', expression)
    expression = re.sub(r'\.to\([^\)]+\)', '', expression)  # Remove unit conversions

    for key in pint_to_sympy.keys():
        expression = expression.replace(key, pint_to_sympy[key])

    # Function to replace 'diam' with the symbol and append any suffix
    def replace_diam(match):
        return f"Symbol('\\oslash{match.group(1)}')"

    # Use regex to find and replace 'diam' with the symbol and append any suffix
    expression = re.sub(r'diam(_\w+)', replace_diam, expression)

    return expression


    return expression

def put_out(precision: int = 2, symbolic: bool = False, offset: int = 0, rows: int = 3, evaluate=True, tablefmt: str = 'pipe') -> None:
    """
    Renders the variables, their expressions, and their values as LaTeX equations in a Jupyter notebook.
    If the expression and result are the same, the expression will be omitted, or if manually specified via the
    'show_expression' parameter, only the result can be shown.

    Args:
        precision (int): The precision for numerical values. Defaults to 2.
        offset (int): The number of previous cells to include for variable extraction. Defaults to 0.
        rows (int): Maximum number of equations per row in horizontal display. Defaults to 3.
        symbols (dict): Dictionary of symbols for LaTeX formatting.
        tablefmt (str): Table format for Markdown rendering. Defaults to 'pipe'.
        show_expression (bool): If True, show the whole equation (variable = expression = result).
                                If False, show only the variable and the result (variable = result).

    Returns:
        None
    """
    variables = parse_cell_variables(offset)
    formatted_vars = {}

    for variable in variables:
        var_name = variable['variable_name']
        result = variable['result']

        # Format the variable name, expression (using SymPy), and result with precision
        formatted_name = format_expression(var_name)
        formatted_result = format_value(result, precision=precision)

        if symbolic:
            expression = variable['expression']
            formatted_expr = format_expression(expression, evaluate)  # Use the new format_expression function
            # Show the full equation (variable = expression = result)
            formatted_vars.update({
                formatted_name: f"{formatted_expr} = {formatted_result}"
            })
        else:
            # Show only the result (variable = result)
            formatted_vars.update({
                formatted_name: f"{formatted_result}"
            })

    # Horizontal display with aligned '=' signs
    var_list = list(formatted_vars.items())

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
    print(markdown_str)
    display(Markdown(markdown_str))

def dict_to_markdown_table(dict:dict, precision:int=2, tablefmt: str='pipe'):
    # Convert dictionary to list of lists with appropriate headers
    formatted_data = [['$'+str(format_name(key))+'$', '$'+str(format_value(value, precision))+'$'] for key, value in dict.items()]
    headers = ['Bezeichnung', 'Wert']

    # Generate the Markdown table
    markdown_table = tabulate(formatted_data, headers=headers, tablefmt=tablefmt)

    return markdown_table