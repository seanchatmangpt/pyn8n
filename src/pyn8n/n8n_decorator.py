from typing import Callable, Type, Optional
from functools import wraps
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

# Initialize FastAPI Router
router = APIRouter()

# Registry to store all n8n nodes
n8n_nodes_registry = {}


def n8n_node(
    node_name: Optional[str] = None,
    input_model: Type[BaseModel] = BaseModel,
    output_model: Type[BaseModel] = BaseModel,
):
    """
    Decorator to register a Python function as an n8n node.

    Args:
        node_name (Optional[str]): The name of the node in n8n. Defaults to the function name.
        input_model (Type[BaseModel]): Pydantic model for input validation.
        output_model (Type[BaseModel]): Pydantic model for output validation.
    """
    def decorator(func: Callable[..., BaseModel]):
        # Use the function name if node_name is not provided
        action_name = node_name or func.__name__

        # Add to registry
        n8n_nodes_registry[action_name] = {
            "function": func,
            "input_model": input_model,
            "output_model": output_model,
        }

        print(f"Registered n8n node: {action_name}")

        # Define a FastAPI endpoint for the node
        @router.post(f"/{action_name}", response_model=output_model)
        @wraps(func)
        async def endpoint(body: input_model):
            try:
                # Execute the registered function
                result = func(body)
                return output_model(**result.dict())  # Ensure output matches the model
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

        return func  # Return the original function unmodified

    return decorator
