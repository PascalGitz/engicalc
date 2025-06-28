import ast
from IPython import get_ipython
from assignment import Assignment
from conditional import Conditional 
from function import Function
from name import Name



class Cell:
    def __init__(self, show_name=True, show_expression=True, show_value=True, precision=4):
        self.cell_content = cell_content()
        self.blocks = parse(self.cell_content, show_name, show_expression, show_value, precision)
        self.precision = precision  
    

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
        if isinstance(node, ast.FunctionDef):
            results.append(Function(get_code(node, lines), show_name=show_name, show_expression=show_expression, show_value=show_value, precision=precision))
        elif isinstance(node, ast.Assign):
            results.append(Assignment(get_code(node, lines), show_name=show_name, show_expression=show_expression, show_value=show_value, precision=precision))
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