import ast
from latex import latexify_name, latexify_expression

class Function:
    def __init__(self, function_str=None):
        self.name, self.parameters, self.body, self.ret = split(function_str)
        self.latex_name = latexify_name(self.name)
        self.latex_ret = latexify_expression(self.ret)


def split(function_str):
    """
    Splits a function string into name, parameters, body, and return value.
    - name: function name (without parameters)
    - parameters: list of parameter names
    - body: function body as a string (excluding return)
    - ret: return expression as a string
    """
    tree = ast.parse(function_str)
    func_node = next((node for node in tree.body if isinstance(node, ast.FunctionDef)), None)
    # Get the parameters
    param_names = [arg.arg for arg in func_node.args.args]
    # Get the function name
    name = func_node.name
    # Get the body as code (excluding return)
    body_stmts = [stmt for stmt in func_node.body if not isinstance(stmt, ast.Return)]
    body = '\n'.join([ast.unparse(stmt) for stmt in body_stmts])
    # Get the return statement
    ret_stmt = next((stmt for stmt in func_node.body if isinstance(stmt, ast.Return)), None)
    ret = ast.unparse(ret_stmt.value) if ret_stmt is not None else None
    return name, param_names, body, ret
