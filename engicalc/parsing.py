import inspect
import ast


global_expressions = []  # Store parsed variables globally


def return_recalled_variables(variable_name):
    """Parses recalled variables from global_expressions."""
    for entry in global_expressions:
        if entry['variable_name'] == variable_name:
            return entry
    return None

def format_parsing(variable_name, expression, result):
    """Formats parsed content into a structured dictionary."""
    return {
        'variable_name': variable_name,  # Name of the variable
        'expression': expression,  # Expression used to define the variable
        'result': result  # Evaluated result of the expression
    }

def update_global_expressions(variable_name, expression, result):
    """Updates or adds parsed variables to global_expressions."""
    for entry in global_expressions:
        if entry['variable_name'] == variable_name:
            entry.update({'expression': expression, 'result': result})
            return
    global_expressions.append(format_parsing(variable_name, expression, result))



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

            parsed_data = format_parsing(variable_name, expression, result)
            cell_variables.append(parsed_data)
            update_global_expressions(variable_name, expression, result)

        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Name):  # Standalone variable reference
            variable_name = node.value.id  # Extract variable name

            recalled_variable = return_recalled_variables(variable_name)
            if recalled_variable:
                variable, expression, result = recalled_variable["variable_name"], recalled_variable["expression"], recalled_variable["result"]
                parsed_data = format_parsing(variable, expression, result)
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
                parsed_data.append(format_parsing(arg_name, expression, user_ns.get(arg_name, None)))

            # Extract variable assignments inside the function body
            for stmt in node.body:
                if isinstance(stmt, ast.Assign):
                    variable_name = stmt.targets[0].id
                    expression = ast.unparse(stmt.value)

                    try:
                        result = eval(expression, user_ns)
                    except Exception:
                        result = None
                    parsed_data.append(format_parsing(variable_name, expression, result))

    return parsed_data


def parse_list(variable_list):
    """Retrieves variables from global namespace and formats them as equations."""
    ipy = get_ipython()

    # Get the last executed cell from the input history
    last_cell_index = len(ipy.history_manager.input_hist_raw) - 1
    cell_code = ipy.history_manager.input_hist_raw[last_cell_index]

    tree = ast.parse(cell_code)  # Parse the cell code into an AST

    list_variables = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):  # Handle variable references
            variable_name = node.id  # Extract variable name correctly
            
            recalled_variable = return_recalled_variables(variable_name)
            if recalled_variable:
                variable, expression, result = recalled_variable["variable_name"], recalled_variable["expression"], recalled_variable["result"]
                parsed_data = format_parsing(variable, expression, result)
                list_variables.append(parsed_data)

    return list_variables
