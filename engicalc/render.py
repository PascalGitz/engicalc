from sympy import latex
from parsing import parse, cell_content
from sympify import do_sympify
from numeric import numeric_eval
from IPython.display import display, Markdown

def render(precision: float = 2, symbolic: bool = True, evaluate: bool = False, numeric: bool = True, rows: int = 1, raw=False):
    """Parses variables from the current cell and renders Markdown output."""
    
    content = cell_content()
    parsed_lines = parse(content)
    markdown_str = build_markdown(parsed_lines, precision, symbolic, evaluate, numeric, rows)
    if not raw:
        display(Markdown(markdown_str))
    else:
        return markdown_str
    

def build_markdown(parsed_lines, precision: float = 2, symbolic: bool = True, evaluate: bool = False, numeric: bool = True, rows: int = 1):
    """Constructs and displays the final Markdown output from parsed variables."""

    print(parsed_lines)
    
    equations = [build_equation(eq, precision, symbolic, numeric, evaluate) for eq in parsed_lines]
    print(equations)
    equations = list(dict.fromkeys(equations))
    print(equations)
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
    
    return(markdown_str)
        

def build_equation(line, precision: float, symbolic: bool, numeric: bool, evaluate: bool):
    """
    Builds a LaTeX equation string from a parsed line using do_sympify for symbolic and numeric_eval for numeric part.
    """
    # Symbolic part
    sympified = do_sympify([line])[0]
    var = latex(sympified.lhs) if hasattr(sympified, 'lhs') else ''
    expr = latex(sympified.rhs) if hasattr(sympified, 'rhs') else latex(sympified)
    # Numeric part
    result = numeric_eval(sympified)
    result_str = f"{result:.{int(precision)}f}" if (result is not None and hasattr(result, '__float__')) else str(result)
    if var == expr:
        equation = f'{var} = {result_str}'
    else:
        if symbolic and numeric:
            equation = f'{var} = {expr} = {result_str}'
        elif symbolic:
            equation = f'{var} = {expr}'
        elif numeric:
            equation = f'{var} = {result_str}'
        else:
            equation = var
    return equation