import inspect
import sys
import ast
from sympy import sympify, latex, SympifyError, Symbol, Matrix
import numpy as np
from IPython.display import display, Markdown
import IPython
import re

from engicalc.substitutes import replacements_specials, replacements_units
from engicalc.units import ureg


global_expressions = []  # Store parsed variables globally




def render(precision: float = 2, symbolic: bool = True, evaluate: bool = False, numeric: bool = True, rows: int = 1, style=None, raw=False):
    """Parses variables from the current cell and renders Markdown output."""
    
    parsed_lines = parse_cell()  # Parse cell variables
    _build_markdown(parsed_lines, precision, symbolic, evaluate, numeric, rows, style, raw)

def render_func(precision: float = 2, symbolic: bool = True, evaluate: bool = False, numeric: bool = True, rows: int = 1, style=None, raw=False):
    """Parses variables from the function where it is called and renders Markdown output."""
    
    parsed_lines = parse_function()  # Parse function variables
    _build_markdown(parsed_lines, precision, symbolic, evaluate, numeric, rows, style, raw)


def _return_recalled_variables(variable_name):
    """Parses recalled variables from global_expressions."""
    for entry in global_expressions:
        if entry['variable_name'] == variable_name:
            return entry
    return None

def _format_parsing(variable_name, expression, result):
    """Formats parsed content into a structured dictionary."""
    return {
        'variable_name': variable_name,  # Name of the variable
        'expression': expression,  # Expression used to define the variable
        'result': result  # Evaluated result of the expression
    }

def _update_global_expressions(variable_name, expression, result):
    """Updates or adds parsed variables to global_expressions."""
    for entry in global_expressions:
        if entry['variable_name'] == variable_name:
            entry.update({'expression': expression, 'result': result})
            return
    global_expressions.append(_format_parsing(variable_name, expression, result))



def parse_cell():
    """Extracts variables, function calls, and recalled variables from the current cell using AST."""
    ipy = get_ipython()

    # Get the last executed cell from the input history
    last_cell_index = len(ipy.history_manager.input_hist_raw) - 1
    cell_code = ipy.history_manager.input_hist_raw[last_cell_index]

    tree = ast.parse(cell_code)  # Parse the cell code into an AST

    user_ns = ipy.user_ns
    cell_variables = []

    for node in ast.walk(tree):
        # Handle variable assignments
        if isinstance(node, ast.Assign):
            variable_name = node.targets[0].id  # Extract variable name
            expression = ast.unparse(node.value)  # Get the expression as a string

            # Evaluate the expression safely
            try:
                result = eval(expression, user_ns)
            except Exception:
                result = None  # If evaluation fails, store None

            parsed_data = _format_parsing(variable_name, expression, result)
            cell_variables.append(parsed_data)
            _update_global_expressions(variable_name, expression, result)

        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Name):  # Standalone variable reference
            variable_name = node.value.id  # Extract variable name

            recalled_variable = _return_recalled_variables(variable_name)
            if recalled_variable:
                variable, expression, result = recalled_variable["variable_name"], recalled_variable["expression"], recalled_variable["result"]
                parsed_data = _format_parsing(variable, expression, result)
                cell_variables.append(parsed_data)

    return cell_variables
     
def parse_function():
    """Extracts variables, conditionals, loops, expressions, and recalled variables from the function that called `put_out()`."""
    
    # Get the current call stack
    stack = inspect.stack()
    
    # Find the frame where `put_out()` was called
    put_out_frame = stack[1]  # This is the frame of `put_out()`
    
    # Find the frame where `put_out()` was invoked
    for frame_info in stack[2:]:  # Start from the caller of `put_out()`
        if frame_info.function != "put_out":  # Skip `put_out` itself
            target_frame = frame_info.frame
            break
    else:
        raise RuntimeError("Could not determine the calling function.")

    # Get the source code of the calling function
    code = inspect.getsource(target_frame.f_code)
    tree = ast.parse(code)  # Parse the function source code into AST
    user_ns = target_frame.f_locals  # Get local variables from the calling function

    parsed_data = []

    for node in ast.walk(tree):
        # Handle function definitions
        if isinstance(node, ast.FunctionDef):
            # Extract function arguments
            for arg in node.args.args:
                arg_name = arg.arg
                expression = None  # Function arguments don't have an assigned expression initially
                parsed_data.append(_format_parsing(arg_name, expression, user_ns.get(arg_name, None)))

            # Extract variable assignments inside the function body
            for stmt in node.body:
                if isinstance(stmt, ast.Assign):
                    variable_name = stmt.targets[0].id
                    expression = ast.unparse(stmt.value)

                    try:
                        result = eval(expression, user_ns)
                    except Exception:
                        result = None
                    parsed_data.append(_format_parsing(variable_name, expression, result))

    return parsed_data

def _build_markdown(parsed_lines, precision: float = 2, symbolic: bool = True, evaluate: bool = False, numeric: bool = True, rows: int = 1, style=None, raw=False):
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
        display(Markdown(colored_markdown_str))
        if raw:
            print(markdown_str)
    else:
        display(Markdown(markdown_str))
        if raw:
            print(markdown_str)

    # Reset unit format
    ureg.formatter.default_format = "~P"

def _format_value(value, precision: float):
    """Formats the value based on its type."""
    # change the unit format to latex
    ureg.formatter.default_format = "~L"

    if isinstance(value, (int, float)):
        return round(value, precision)
    
    elif isinstance(value, np.ndarray):
        # Handle numpy arrays as matrices
        rounded_value = np.round(value, precision)
        matrix = Matrix(rounded_value.tolist())
        return latex(matrix)
    
    elif isinstance(value, list):
        # Handle lists as vectors
        formatted_list = [_format_value(item, precision) for item in value]
        return formatted_list
    
    elif hasattr(value, "magnitude"):

        # replace the degree sign
        units = str(value.units)
        units = units.replace('deg','°')

        # Handle Pint quantities
        magnitude = np.round(value.magnitude, precision)
        if isinstance(magnitude, np.ndarray):
            # Handle numpy arrays of Pint quantities as matrices
            return f"{latex(Matrix(magnitude.tolist()))} \\ {latex(Symbol(units))}"
        else:
            # Handle scalar Pint quantities
            return f"{magnitude} \\ {latex(Symbol(units))}"
    else:
        return value

def _format_symbolic(expr: str, evaluate: bool) -> str:
    """Formats the symbolic expression using sympy by applying a structured substitution process."""
    try:
        expr = _apply_substitutions(expr)
        symbolic_expr = sympify(expr, evaluate=evaluate)
        return latex(symbolic_expr, mul_symbol='dot', order='none')
    except (SympifyError, TypeError, ValueError):
        return expr

def _apply_substitutions(expr: str) -> str:
    """Applies all necessary substitutions in a structured order."""
    possible_prefixes = _get_possible_prefixes()  # Retrieve module prefixes

    expr = _substitute_numpy_functions(expr)  # Convert NumPy functions dynamically
    expr = _substitute_pint_methods(expr, possible_prefixes)
    expr = _substitute_units(expr, possible_prefixes)
    expr = _substitute_special_characters(expr)

    return expr

def _get_possible_prefixes() -> set:
    """Retrieve dynamically imported module prefixes, including NumPy's alias."""
    user_ns = IPython.get_ipython().user_ns  # Get global namespace
    possible_prefixes = {name for name, obj in user_ns.items() if inspect.ismodule(obj)}

    # Identify the alias used for NumPy
    for name, obj in user_ns.items():
        if obj is np:
            possible_prefixes.add(name)  # Add NumPy alias dynamically
    return possible_prefixes

def _get_numpy_alias() -> str:
    """Detect the alias used for NumPy dynamically, filtering out direct 'numpy' imports."""
    user_ns = IPython.get_ipython().user_ns  # Get global namespace

    for name, obj in user_ns.items():
        try:
            # Ensure it's a module AND originates from NumPy
            if isinstance(obj, type(np)) and obj.__name__ == "numpy" and name != "numpy":
                return name  # Return the alias, NOT 'numpy'
        except AttributeError:
            continue  # Ignore non-modules
    
    return "numpy"  # NumPy alias not found


def _substitute_numpy_functions(expr: str) -> str:
    """Replace NumPy functions with their SymPy equivalents, using the detected alias."""
    
    numpy_alias = _get_numpy_alias()  # Detect NumPy alias dynamically

    if numpy_alias:
        numpy_to_sympy = {
            f'{numpy_alias}.sin': 'sin',
            f'{numpy_alias}.asin': 'asin',
            f'{numpy_alias}.cos': 'cos',
            f'{numpy_alias}.acos': 'acos',
            f'{numpy_alias}.tan': 'tan',
            f'{numpy_alias}.atan': 'atan',
            f'{numpy_alias}.exp': 'exp',
            f'{numpy_alias}.log': 'log',
            f'{numpy_alias}.sqrt': 'sqrt',
            f'{numpy_alias}.abs': 'Abs',
            f'{numpy_alias}.array': 'Matrix',
            f'{numpy_alias}.dot': '*',  # Convert matrix multiplication
        }

        for np_func, sympy_func in numpy_to_sympy.items():
            expr = expr.replace(np_func, sympy_func)  # Replace dynamically
        
    return expr


def _substitute_pint_methods(expr: str, possible_prefixes: set) -> str:
    """Handles `.m` and `.magnitude`, keeping `.m` if it has a valid prefix."""
    
    # Step 1: Remove `.magnitude`
    expr = re.sub(r'\.magnitude\b', '', expr)
    
    # Step 2: Explicitly check prefixes instead of using a regex pattern
    tokens = expr.split()  # Split expression into tokens for processing
    cleaned_tokens = []
    
    for token in tokens:
        # If the token has `.m`, check if the prefix is in possible_prefixes
        if ".m" in token:
            prefix = token.split(".")[0]  # Extract prefix before `.m`
            if prefix not in possible_prefixes:  
                token = token.replace(".m", "")  # Remove `.m` only if prefix isn't valid
        
        cleaned_tokens.append(token)
    
    expr = " ".join(cleaned_tokens)  # Reconstruct expression
    
    # Step 3: Remove `.to(...)` unit conversions
    expr = re.sub(r'\.to\(\s*[^)]*\)', '', expr)
    
    return expr

def _substitute_units(expr: str, possible_prefixes: set) -> str:
    """Replace unit names with corresponding SymPy symbols, handling dynamic prefixes."""
    sorted_keys = sorted(replacements_units.keys(), key=len, reverse=True)
    for key in sorted_keys:
        pattern = rf'\b(?:{"|".join(possible_prefixes)})?\.{key}\b|\b{key}\b'
        expr = re.sub(pattern, replacements_units[key], expr)
    return expr

def _substitute_special_characters(expr: str) -> str:
    """Wrap special variable names in SymPy Symbol() and replace special characters."""

    def replace_variables(match):
        var_name = match.group(0)
        for entry in global_expressions:
            if var_name == entry['variable_name']:
                return f'Symbol("{var_name}")'
        return var_name

    expr = re.sub(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', replace_variables, expr)
    
    for key, value in replacements_specials.items():
        expr = expr.replace(key, value)
    
    return expr

def build_equation(assignment: dict, precision: float, symbolic: bool, numeric: bool, evaluate: bool):
    try:
        var = _format_symbolic(assignment['variable_name'], evaluate=evaluate)
        expression = _format_symbolic(assignment['expression'], evaluate=evaluate)
        result = _format_value(assignment['result'], precision=precision)

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
        var = _format_symbolic(assignment['variable_name'], evaluate=evaluate)
        result = _format_value(assignment['result'], precision=precision)
        equation = f'{var}& = {result}'

    return equation