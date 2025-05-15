from IPython.display import display, Markdown
from engicalc.units import ureg

from engicalc.substitution import *
from engicalc.parsing import *





def render(precision: float = 2, symbolic: bool = True, evaluate: bool = False, numeric: bool = True, rows: int = 1, style=None, raw=False):
    """Parses variables from the current cell and renders Markdown output."""
    
    parsed_lines = parse_cell()  # Parse cell variables
    raw_string = build_markdown(parsed_lines, precision, symbolic, evaluate, numeric, rows, style)
    if raw== False:
        display(Markdown(raw_string))
    if raw== True:
        return raw_string
    
def render_func(precision: float = 2, symbolic: bool = True, evaluate: bool = False, numeric: bool = True, rows: int = 1, style=None, raw=False):
    """Parses variables from the function where it is called and renders Markdown output."""
    
    parsed_lines = parse_function()  # Parse function variables
    raw_string = build_markdown(parsed_lines, precision, symbolic, evaluate, numeric, rows, style)
    if raw== False:
        display(Markdown(raw_string))
    if raw== True:
        return raw_string
    
def render_list(list, precision: float = 2, symbolic: bool = True, evaluate: bool = False, numeric: bool = True, rows: int = 1, style=None, raw=True):
    """Parses variables from the function where it is called and renders Markdown output."""
    
    parsed_lines = parse_list(list)  # Parse function variables
    raw_list = []
    for line in parsed_lines:
        raw_string = build_markdown([line], precision, symbolic, evaluate, numeric, rows, style)
        if raw== False:
            display(Markdown(raw_string))
        if raw== True:
            raw_list.append(raw_string)
    return raw_list


def build_markdown(parsed_lines, precision: float = 2, symbolic: bool = True, evaluate: bool = False, numeric: bool = True, rows: int = 1, style=None):
    """Constructs and displays the final Markdown output from parsed variables."""
    
    # Build equations from parsed variables
    equations = [build_equation(assignment=eq, symbolic=symbolic, numeric=numeric, precision=precision, evaluate=evaluate) for eq in parsed_lines]

    # Remove duplicates
    equations = list(dict.fromkeys(equations))
    rows = min(rows, len(equations))

    # Construct Markdown output
    markdown_str = "$$\\begin{aligned}"
    for i in range(0, len(equations), rows):
        row = equations[i : i + rows]
        row_str = " \\quad & ".join([f"{eq}" for eq in row])
        if len(row) < rows and rows != 1:
            row_str += " \\quad & " * (rows - len(row)) 

        markdown_str += row_str
        if i + rows < len(equations):
            markdown_str += " \\\\ "

    markdown_str += "\\end{aligned}$$"

    # Apply custom styling if provided
    if style:
        colored_markdown_str = f"::: {{custom-style=\"{style}\"}}\n{markdown_str}\n:::"
        # Reset unit format
        ureg.formatter.default_format = "~P"
        return(colored_markdown_str)
    else:
        # Reset unit format
        ureg.formatter.default_format = "~P"
        return(markdown_str)
        

def build_equation(assignment: dict, precision: float, symbolic: bool, numeric: bool, evaluate: bool):
    try:
        var = format_symbolic(assignment['variable_name'], evaluate=evaluate)
        expression = format_symbolic(assignment['expression'], evaluate=evaluate)
        result = format_value(assignment['result'], precision=precision)

        if var == expression:
            equation = f'{var}& = {result}'
        else:
            # Check if the expression can be converted to a float
            try:
                float(expression)
                # If it can be converted, use only the numeric form
                equation = f'{var}& = {result}'
            except ValueError:
                # If it cannot be converted, handle symbolic, numeric, or both forms
                if symbolic == False:
                    equation = f'{var}& = {result}'
                if numeric == False:
                    equation = f'{var}& = {expression}'
                if numeric == True and symbolic == True:
                    equation = f'{var}& = {expression} = {result}'
    except:
        var = format_symbolic(assignment['variable_name'], evaluate=evaluate)
        result = format_value(assignment['result'], precision=precision)
        equation = f'{var}& = {result}'
    return equation