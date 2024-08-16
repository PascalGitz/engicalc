from IPython.display import display, Markdown, Latex
import io
import re
from contextlib import redirect_stdout
from sympy import Symbol, latex
import numpy as np


special_characters = {
    "diam": r"\oslash",
    "strich": r"'",
    "sum": r"\sum",
}



def format_value(value, precision:float = 2):
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
        

def format_name(name: str, symbols: dict = special_characters) -> str:
    """Formats the input string with specific LaTeX replacements while handling exceptions for underscores."""
    
    # Regex to find words, underscores, and numbers separately
    name_parts = re.findall(r'[a-zA-Z]+|_|\d+', name)
    
    result_parts = []
    i = 0

    while i < len(name_parts):
        part = name_parts[i]
        
        # Handle the 'sum_' exception
        if part == 'sum' and i+1 < len(name_parts) and name_parts[i+1] == '_':
            result_parts.append(symbols.get(part, part))
            i += 1  # Skip the underscore after 'sum'

        # Handle the '_strich' exception
        elif part == '_' and i+1 < len(name_parts) and name_parts[i+1] == 'strich':
            result_parts.append(symbols.get(name_parts[i+1], name_parts[i+1]))
            i += 1  # Skip both underscore and 'strich'

        # Replace regular parts using the dictionary
        elif part in symbols:
            result_parts.append(symbols[part])
        
        # Preserve numbers and non-matching underscores
        else:
            result_parts.append(part)
        
        i += 1
    

    # Join all parts back together
    name_replaced = ''.join(result_parts)
    
    return name_replaced


def put_out(offset: int = 0, rows: int = 3,) -> None:
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
    # check if the global variables are in the output
    variables = {name: user_ns[name] for name in variable_names if name in user_ns}

    # Format the variables and their values 
    formatted_vars = {format_name(name, special_characters): format_value(value) for name, value in variables.items()}

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

    display(Markdown(markdown_str))


def dict_to_markdown_table(data: dict) -> str:
    if not data:
        return ""
    
    # Extract keys and values
    items = list(data.items())
    rows = []
    
    # Pair items into rows with 4 columns (2 key-value pairs per row)
    for i in range(0, len(items), 2):
        row = []
        for j in range(2):
            if i + j < len(items):
                key, value = items[i + j]
                if type(value) != str:
                    row.extend([str(key), '$'+str(value)+'$'])
                else:
                    row.extend([str(key), str(value)])
            else:
                row.extend(["-", "-"])  # Fill empty cells for incomplete rows
        rows.append(row)
    
    # Headers for the 4 columns
    headers = ["Bezeichnung", "Wert", "Bezeichnung", "Wert"]
    
    # Calculate column widths
    col_widths = [max(len(row[i]) for row in [headers] + rows) for i in range(4)]
    
    # Create the markdown table
    table = []
    
    # Header row
    header_row = "| " + " | ".join(headers[i].ljust(col_widths[i]) for i in range(4)) + " |"
    table.append(header_row)
    
    # Divider
    divider = "| " + " | ".join("-" * col_widths[i] for i in range(4)) + " |"
    table.append(divider)
    
    # Data rows
    for row in rows:
        row_str = "| " + " | ".join(row[i].ljust(col_widths[i]) for i in range(4)) + " |"
        table.append(row_str)
    
    return "\n".join(table)

