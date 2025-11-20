import ast
from .latexit import latexify_name, latexify_expression


class Function():
    def __init__(self, function_str, show_name, show_expression, show_value, precision):
        self.show_name = show_name
        self.show_expression = show_expression
        self.show_value = show_value
        self.precision = precision
        # Parse the function string into name, parameters, body, and return value
        self.body = split(function_str)
        from .parsing import parse
        self.latex_body = [obj.latex_equation for obj in parse(self.body, show_name, show_expression, show_value, precision)]
        self.latex_equation = self.build_latex_equation()

    def build_latex_equation(self):
        # Build the function signature with value
        body_part = self.latex_body
        return body_part



def split(function_str):
    """
    Splits a function string into name, parameters, body, and return value.
    - name: function name (without parameters)
    - parameters: string of parameters, each on a new line (e.g. 'x\na=2\nc')
    - body: function body as a string (excluding return)
    - ret: return expression as a string
    """
    tree = ast.parse(function_str)
    func_node = next((node for node in tree.body if isinstance(node, ast.FunctionDef)), None)
    if func_node is None:
        raise ValueError("No function definition found in the provided string.")
    # Get the body as code (excluding return)
    body_stmts = [stmt for stmt in func_node.body if not isinstance(stmt, ast.Return)]
    body = '\n'.join([ast.unparse(stmt) for stmt in body_stmts])
    
    return body
