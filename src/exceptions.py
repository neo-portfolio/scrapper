class InvalidEnvError(Exception):
    def __init__(self, expression: str = None):
        self.expression = expression
        self.message = "invalid"
