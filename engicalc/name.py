from latexit import latexify_name, latexify_expression

class Name:
    def __init__(self, name_str):
        self.name= name_str
        self.latex_name = latexify_name(self.name)
        self.latex_equation = self.latex_name

