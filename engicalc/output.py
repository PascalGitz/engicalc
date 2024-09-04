from IPython.display import display, Markdown, Latex
import io
import re
from contextlib import redirect_stdout
from sympy import Symbol, latex, Matrix
import numpy as np
from tabulate import tabulate

# Define special characters and symbols
special_characters = {
    "diam": r"\oslash",
    "apos": r"'",
    "sum": r"\sum",
    "comma": r",",
    "txt": r"\text"
}

def parse_cell_variables(offset: int = 0) -> dict:
    """
    Parses the cell history to extract variable names and their corresponding values.

    Args:
        offset (int): The number of previous cells to include for variable extraction. Defaults to 0.

    Returns:
        dict: A dictionary with variable names as keys and their corresponding values from the user namespace.
    """
    ipy = get_ipython()
    out = io.StringIO()

    # Capture the history of executed commands
    with redirect_stdout(out):
        ipy.run_line_magic("history", f"{ipy.execution_count - offset}")

    # Extract variable names from the captured output
    lines = out.getvalue().replace(" ", "").split("\n")
    variable_names = []
    
    for line in lines:
        if "=" in line:
            variable_names.append(line.split('=')[0])
        else:
            variable_names.append(line)
    # Get the current global variables from the IPython user namespace
    user_ns = ipy.user_ns

    variables = {name: user_ns[name] for name in variable_names if name in user_ns}

    return variables



def format_name(name: str, symbols: dict = special_characters) -> str:
    """Formats the input string with specific LaTeX replacements, handles underscores, and converts 'txt_' prefix to plain text."""
    
    # Regex to find words, underscores, and numbers separately
    name_parts = re.findall(r'[a-zA-Z]+|_|\d+', name)

    
    result_parts = []
    i = 0

    while i < len(name_parts):
        part = name_parts[i]
        
        # Handle the 'sum_' exception
        if part == 'sum' and i + 1 < len(name_parts) and name_parts[i + 1] == '_':
            result_parts.append(symbols.get(part, part))
            i += 1  # Skip the underscore after 'sum'
        
        # Handle the 'sum_' exception
        if part == 'txt' and i + 1 < len(name_parts) and name_parts[i + 1] == '_':
            result_parts.append(symbols.get(part, part))
            result_parts.append('{')
            result_parts.append(name_parts[i+2])
            result_parts.append('}')
            i += 3  # Skip the underscore after 'txt'
        
        # # Handle the 'txt' exception
        # if part == 'txt' and i + 2 < len(name_parts) and name_parts[i + 1] == '_' and name_parts[i + 2] == '_':
        #     result_parts.append(symbols.get(part, part))  # Append the symbol for 'txt' or 'txt' itself
        #     result_parts.append('{')  # Replace the first '_' with '{'
        #     result_parts.append('}')  # Replace the second '_' with '}'
        #     i += 1  # Skip the next two underscores and move to the part after them
        #     print(result_parts)
            

        # Handle the '_strich' exception
        elif part == '_' and i + 1 < len(name_parts) and name_parts[i + 1] == 'apos':
            result_parts.append(symbols.get(name_parts[i + 1], name_parts[i + 1]))
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
    
    # make a symbol out of it
    name_replaced = latex(Symbol(name_replaced))

    return name_replaced
    
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

def dict_to_markdown_table(dict:dict, symbols: dict= special_characters, precision:int=2, tablefmt: str='pipe'):
    # Convert dictionary to list of lists with appropriate headers
    formatted_data = [['$'+str(format_name(key))+'$', '$'+str(format_value(value, precision))+'$'] for key, value in dict.items()]
    headers = ['Bezeichnung', 'Wert']

    # Generate the Markdown table
    markdown_table = tabulate(formatted_data, headers=headers, tablefmt=tablefmt)

    return markdown_table



def put_out(precision: int = 2, offset: int = 0, rows: int = 3, symbols: dict = special_characters, tablefmt:str = 'pipe') -> None:
    """
    Renders the variables and their values as LaTeX equations in a Jupyter notebook.

    Args:
        precision (int): The precision for numerical values. Defaults to 2.
        offset (int): The number of previous cells to include for variable extraction. Defaults to 0.
        rows (int): Maximum number of equations per row in horizontal display. Defaults to 3.
        symbols (dict): Dictionary of symbols for LaTeX formatting.

    Returns:
        None
    """
    # Use the new cell parser function
    variables = parse_cell_variables(offset)


    formatted_vars = {}

    for name, value in variables.items():
        if type(value) == dict:
            display(Markdown(dict_to_markdown_table(value, precision=precision, tablefmt=tablefmt)))
            
        else:
            formatted_vars.update({format_name(name, symbols=symbols): format_value(value, precision=precision)})

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
            [f"{var_name} & = {value}" for var_name, value in row]
        )
        if len(row) < rows and rows != 1:
            row_str += " \\quad & " * (rows - len(row)) + " \n"

        markdown_str += row_str + " \\\\ \n"

    if markdown_str.endswith(" \\\\ \n"):
        markdown_str = markdown_str[:-4]
    markdown_str += "\\end{aligned}\n$$"

    display(Markdown(markdown_str))



