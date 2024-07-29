from IPython.display import display, Markdown, Latex
import io
from contextlib import redirect_stdout
from sympy import Symbol, latex
import numpy as np


def put_out(offset: int = 0, precision: int = 2, rows: int = 3, horizontal: bool = True) -> None:
    """
    Renders the variables and their values as LaTeX equations in a Jupyter notebook.

    Args:
        offset (int): The number of previous cells to include for variable extraction. Defaults to 0.
        precision (int): The precision for numerical values. Defaults to 2.
        rows (int): Maximum number of equations per row in horizontal display. Defaults to 3.
        horizontal (bool): Whether to display equations horizontally or vertically. Defaults to True.

    Returns:
        None
    """
    
    ipy = get_ipython()
    out = io.StringIO()

    # Capture the history of executed commands
    with redirect_stdout(out):
        ipy.run_line_magic("history", f"{ipy.execution_count - offset}")

    # Extract variable names from the captured output
    lines = out.getvalue().replace(" ", "").split("\n")
    variable_names = [line.split("=")[0] for line in lines if "=" in line]

    # Get the current global variables from the IPython user namespace
    user_ns = ipy.user_ns
    variables = {name: user_ns[name] for name in variable_names if name in user_ns}


    def format_value(value):
        """Formats the value based on its type."""
        if isinstance(value, (int, float)):
            return round(value, precision)
        elif isinstance(value, np.ndarray):
            return np.array2string(np.round(value, precision), separator=",")
        elif hasattr(value, "magnitude"):
            magnitude = np.round(value.magnitude, precision)
            if isinstance(magnitude, np.ndarray):
                magnitude_str = np.array2string(magnitude, separator=",")
                return f"{magnitude_str} \\ {latex(Symbol(str(value.units)))}"
            else:
                return f"{magnitude} \\ {latex(Symbol(str(value.units)))}"
        else:
            return value


    # Format the variables and their values
    formatted_vars = {name: format_value(value) for name, value in variables.items()}

    if horizontal:
        # Horizontal display with aligned '=' signs
        var_list = list(formatted_vars.items())

        # check if there are less variables than rows. This results in clean aligning of the equations
        if len(var_list)<rows:
            rows = len(var_list)
        
        markdown_str = "$$\n\\begin{aligned}\n"
        # Iterate through the variables
        for i in range(0, len(var_list), rows):
                row = var_list[i : i + rows]
                row_str = " \\quad & ".join(
                    [f"{latex(Symbol(var_name))} & = {value}" for var_name, value in row]
                )
                # Add placeholders for missing variables in the row
                if len(row) < rows & rows!=1:
                    row_str += " \\quad & " * (rows - len(row)) + " \n"

                markdown_str += row_str + " \\\\ \n"
        # strip the last space
        if markdown_str.endswith(" \\\\ \n"):
            markdown_str = markdown_str[:-4]
        markdown_str += "\\end{aligned}\n$$"

    else:
        markdown_str = ""
        for var_name, value in formatted_vars.items():
            markdown_str += f"$${latex(Symbol(var_name))} = {value}$$\n\n"

    display(Markdown(markdown_str))
