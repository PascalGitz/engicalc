import ast
from latexit import latexify_name, latexify_expression


class Function():
    def __init__(self, function_str, show_name, show_expression, show_value, precision):
        self.name, self.parameters, self.body, self.ret = split(function_str)
        self.latex_name = latexify_name(self.name)
        from parsing import parse
        self.latex_parameters = [obj.latex_equation for obj in parse(self.parameters, show_name, show_expression, show_value, precision)]
        self.latex_body = [obj.latex_equation for obj in parse(self.body, show_name, show_expression, show_value, precision)]
        self.latex_ret = latexify_expression(self.ret)
        self.latex_equation = self.build_latex_equation()

    def build_latex_equation(self):
        # Build the function signature with value
        name_part = self.latex_name + '(' + ', '.join(self.latex_parameters) + ')'
        value_part = self.latex_ret if (show_value and self.latex_ret is not None) else ''
        first_line = f"{name_part} = {value_part}" if value_part else name_part
        # Indent each body line with a single \quad
        if show_expression and self.latex_body:
            body_lines = [r'\\\quad ' + line for line in self.latex_body]
            body_part = ''.join(body_lines)
            return f"{first_line}{body_part}"
        else:
            return first_line


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
    # Get the parameters as a string, each on a new line
    args = func_node.args.args
    defaults = func_node.args.defaults
    num_args = len(args)
    num_defaults = len(defaults)
    param_strs = []
    for i, arg in enumerate(args):
        if i >= num_args - num_defaults:
            default_index = i - (num_args - num_defaults)
            default_val = ast.unparse(defaults[default_index])
            param_strs.append(f"{arg.arg}={default_val}")
        else:
            param_strs.append(arg.arg)
    param_names = "\n".join(param_strs)
    # Get the function name
    name = func_node.name
    # Get the body as code (excluding return)
    body_stmts = [stmt for stmt in func_node.body if not isinstance(stmt, ast.Return)]
    body = '\n'.join([ast.unparse(stmt) for stmt in body_stmts])
    # Get the return statement
    ret_stmt = next((stmt for stmt in func_node.body if isinstance(stmt, ast.Return)), None)
    ret = ast.unparse(ret_stmt.value) if ret_stmt is not None and getattr(ret_stmt, 'value', None) is not None else None
    return name, param_names, body, ret
