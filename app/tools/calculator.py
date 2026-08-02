import math
import re

from langchain_core.tools import tool

from app.tools.registry import tool_registry


@tool("calculator")
def calculator_tool(expression: str) -> str:
    """
    Useful to compute mathematical expressions.
    Input should be a mathematical expression, e.g., '2 + 2' or 'sqrt(16) * 5'.
    Only supports arithmetic operations and standard math functions (sin, cos, tan, log, sqrt, etc.).
    """
    # Clean expression and only allow safe characters
    clean_expr = re.sub(r"[^0-9+\-*/().\s,a-zA-Z]", "", expression)

    # Define a safe dictionary of math functions and constants
    safe_dict = {
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "sqrt": math.sqrt,
        "log": math.log,
        "exp": math.exp,
        "pi": math.pi,
        "e": math.e,
        "pow": math.pow,
        "abs": abs,
    }

    try:
        # Safe eval using limited globals and no locals
        result = eval(clean_expr, {"__builtins__": None}, safe_dict)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression '{expression}': {e!s}"


# Register tool
tool_registry.register(calculator_tool)
