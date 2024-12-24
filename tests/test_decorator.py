import pytest
from pydantic import BaseModel
from pyn8n.n8n_decorator import n8n_node, n8n_nodes_registry


class TestInput(BaseModel):
    value: int


class TestOutput(BaseModel):
    squared: int


@n8n_node(node_name="square_node", input_model=TestInput, output_model=TestOutput)
def square_explicit(body: TestInput) -> TestOutput:
    return TestOutput(squared=body.value ** 2)


@n8n_node(input_model=TestInput, output_model=TestOutput)
def square_default(body: TestInput) -> TestOutput:
    return TestOutput(squared=body.value ** 2)


def test_n8n_node_registration():
    # Explicit node name
    assert "square_node" in n8n_nodes_registry
    node = n8n_nodes_registry["square_node"]
    assert node["function"] == square_explicit
    assert node["input_model"] == TestInput
    assert node["output_model"] == TestOutput

    # Default node name
    assert "square_default" in n8n_nodes_registry
    node = n8n_nodes_registry["square_default"]
    assert node["function"] == square_default
    assert node["input_model"] == TestInput
    assert node["output_model"] == TestOutput
