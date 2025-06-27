class Conditional:
    def __init__(self, name=None, expression=None, value=None):
        self.name = name
        self.expression = expression
        self.value = value
        self.latex_name = None
        self.latex_expression = None
        self.latex_value = None