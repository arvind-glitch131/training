import datetime

def get_current_time(*args, **kwargs):
    """Returns the current date and time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculator(expression):
    """Evaluates a mathematical expression string."""
    try:
        # Note: In a production app, use a safer math parser like 'numexpr' 
        # but for an assignment, eval is the standard way to show logic.
        return eval(expression)
    except Exception as e:
        return f"Error: {str(e)}"

# The Registry: This is what the Agent will look at
TOOL_REGISTRY = {
    "get_current_time": get_current_time,
    "calculator": calculator
}