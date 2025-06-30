import ast
from IPython import get_ipython
from assignment import Assignment
from conditional import Conditional 
from function import Function
from name import Name



class Cell:
    def __init__(self, show_name=True, show_expression=True, show_value=True, precision=2, rows=1):
        self.cell_content = cell_content()
        self.blocks = parse(self.cell_content, show_name, show_expression, show_value, precision)
        self.latex_aligned = self.build_aligned(rows)

    def __repr__(self):
        # Return the raw LaTeX string, with single backslashes and no $$
        return self.latex_aligned

    def _repr_markdown_(self):
        return self.latex_aligned

    def build_aligned(self, rows=3):
        """
        Build a LaTeX aligned block from the cell's blocks (self.blocks).
        The number of equations per row is determined by the 'rows' parameter.
        Each row is spaced with \quad and aligned at the start of each equation.
        If there are more equations than rows, continue on the next line.
        """
        equations = [block.latex_equation for block in self.blocks]
        markdown_str = "$$\\begin{aligned}" + "&"
        for i in range(0, len(equations), rows):
            row = equations[i : i + rows]
            # Add \quad between equations, align at start
            row_str = " \\quad ".join([f" {eq}" for eq in row])
            markdown_str += row_str
            if i + rows < len(equations):
                markdown_str += " \\\\ & "
        markdown_str += "\\end{aligned}$$"
        return markdown_str


def parse(code: str, show_name, show_expression, show_value, precision) -> list:
    """
    Parses the input code using ast and returns a list of tuples (syntax_type, content).
    syntax_type: 'name', 'assignment', 'function', 'conditional', or 'expression'
    content: the source code of the detected object or name
    """
    results = []
    try:
        tree = ast.parse(code)
    except Exception as e:
        return [("error", str(e))]

    lines = code.splitlines()
    for node in tree.body:
        # Skip if the node is a call or instantiation of Cell (even in assignment)
        if isinstance(node, ast.Assign):
            value = node.value
            if isinstance(value, ast.Call):
                func = value.func
                if (hasattr(func, 'id') and func.id == 'Cell') or (hasattr(func, 'attr') and func.attr == 'Cell'):
                    continue
            results.append(Assignment(get_code(node, lines), show_name=show_name, show_expression=show_expression, show_value=show_value, precision=precision))
        if isinstance(node, ast.FunctionDef):
            results.append(Function(get_code(node, lines), show_name=show_name, show_expression=show_expression, show_value=show_value, precision=precision))
        elif isinstance(node, ast.If):
            results.append(Conditional(get_code(node, lines), show_name=show_name, show_expression=show_expression, show_value=show_value, precision=precision))
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Name):
            # Single variable name as a statement (e.g., 'var')
            results.append(Name(node.value.id))
        # Ignore all other node types
    return results


def cell_content() -> str:
    """
    Returns the content of the current Jupyter notebook cell as a string.
    """
    try:
        ip = get_ipython()
        if ip is None:
            raise RuntimeError("Not running inside an IPython environment.")
        # Use ip.history_manager to get the last input (current cell)
        cell = ip.history_manager.input_hist_raw[-1]
        return cell
    except Exception as e:
        raise RuntimeError(f"Could not retrieve cell content: {e}")


def get_code(node, lines):
    start = getattr(node, 'lineno', 1) - 1
    end = getattr(node, 'end_lineno', start + 1)
    return '\n'.join(lines[start:end])