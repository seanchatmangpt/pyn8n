from pydantic import BaseModel, Field
from pyn8n.n8n_decorator import n8n_node


# Input model
class FactorialInput(BaseModel):
    number: int = Field(..., ge=0, description="A non-negative integer")


# Output model
class FactorialOutput(BaseModel):
    result: int = Field(..., description="The factorial of the input number")


# Node definition with explicit node_name
@n8n_node(node_name="compute_factorial", input_model=FactorialInput, output_model=FactorialOutput)
def factorial_node(body: FactorialInput) -> FactorialOutput:
    """Compute the factorial of a number."""
    def factorial(n: int) -> int:
        return 1 if n == 0 else n * factorial(n - 1)

    result = factorial(body.number)
    print(f"{factorial_node.__name__}: Factorial of {body.number} is {result}")
    return FactorialOutput(result=result)


# Node definition without explicit node_name (defaults to the function name)
@n8n_node(input_model=FactorialInput, output_model=FactorialOutput)
def factorial(body: FactorialInput) -> FactorialOutput:
    """Compute the factorial of a number."""
    def factorial(n: int) -> int:
        return 1 if n == 0 else n * factorial(n - 1)

    result = factorial(body.number)
    print(f"{factorial.__name__}: Factorial of {body.number} is {result}")
    return FactorialOutput(result=result)

