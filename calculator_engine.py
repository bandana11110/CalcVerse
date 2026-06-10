import math

allowed = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "factorial": math.factorial,
    "log": math.log10,
    "ln": math.log,
    "pow": pow,
    "pi": math.pi,
    "e": math.e,
    "abs": abs,
    "round": round
}

def calculate(expression):

    try:
        result = eval(
            expression,
            {"_builtins_": None},
            allowed
        )

        return result

    except Exception as err:
        return f"Error: {err}"