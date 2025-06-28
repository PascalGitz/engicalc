class Markdown_block:
    def __init__(self, parse_results, show_name=True, show_expression=True, show_value=True, precision=4):
        """
        - parse_results: list of objects from parse()
        - show_name, show_expression, show_value: toggles for build_latex_equation
        - precision: for latexify_value
        """
        self.parse_results = parse_results
        self.show_name = show_name
        self.show_expression = show_expression
        self.show_value = show_value
        self.precision = precision
        # Collect latex_equation from each object
        self.latex_lines = [obj.latex_equation for obj in self.parse_results]
        # Store the aligned LaTeX block
        self.latex_aligned = self._build_aligned_block()

    def _build_aligned_block(self):
        # Use LaTeX aligned environment for multi-row rendering
        lines = self.latex_lines
        aligned = r"\begin{aligned}" + " \\ ".join(lines) + r"\end{aligned}"
        return aligned
