import ast
from IPython import get_ipython

def get_code(node, lines):
    start = getattr(node, 'lineno', 1) - 1
    end = getattr(node, 'end_lineno', start + 1)
    return '\n'.join(lines[start:end])

def parse(code: str,):
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
            results.append(("function", get_code(node, lines)))
        elif isinstance(node, ast.Assign):
            results.append(("assignment", get_code(node, lines)))
        elif isinstance(node, ast.If):
            results.append(("conditional", get_code(node, lines)))

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
