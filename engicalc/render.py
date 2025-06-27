from sympy import latex
from parsing import parse, cell_content
from sympify import do_sympify
from numeric import numeric_eval
from IPython.display import display, Markdown

def render(precision: float = 2, symbolic: bool = True, evaluate: bool = False, numeric: bool = True, rows: int = 1, style=None, raw=False):
    """
    Uses cell_content() to get the cell content, parses it, creates symbolic and numeric parts, and returns a LaTeX string.
    Displays each equation as: symbolic = num_val
    """
    content = cell_content()
    parsed = parse(content)
    sympified = do_sympify(parsed)
    for sym_obj in sympified:
        symbolic_str = latex(sym_obj) if symbolic else ""
        num_val = numeric_eval(sym_obj) if numeric else None
        num_str = f"{num_val:.{int(precision)}f}" if (num_val is not None and hasattr(num_val, '__float__')) else str(num_val) if num_val is not None else ""
        eq_str = symbolic_str
        if symbolic and numeric and num_str:
            eq_str += f" = {num_str}"
        display(Markdown(r"$$" + eq_str + r"$$"))
    # Optionally, return the last equation string
    return eq_str

