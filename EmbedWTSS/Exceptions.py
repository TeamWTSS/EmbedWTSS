class InvalidSyntax(Exception):
    def __init__(self):
        super().__init__("Invalid Syntax!")


class InvalidSyntaxCompiler(Exception):
    def __init__(self, line, text):
        super().__init__(f"Invalid Syntax, Line: {line}, Text: {text}")


class NeedAnArgument(Exception):
    def __init__(self):
        super().__init__("Code is need an argument!")
