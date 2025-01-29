
from jinja2 import Template

template = Template("""
from pydantic import BaseModel, Field
from pyn8n.n8n_decorator import n8n_node

{% for import in import_list %}
{{ import }}
{% endfor %}

# Input model
class {{ input_model.name }}Input(BaseModel):
    {% for field in input_model.fields %}
    {{ field.name }}: {{ field.type }} = Field(..., description="{{ field.description }}")
    {% endfor %}

# Output model
class {{ output_model.name }}(BaseModel):
    {% for field in output_model.fields %}
    {{ field.name }}: {{ field.type }} = Field(..., description="{{ field.description }}")
    {% endfor %}

# Node definition
@n8n_node(input_model={{ input_model.name }}Input, output_model={{ output_model.name }})
def {{ function_name }}(body: {{ input_model.name }}Input) -> {{ output_model.name }}:
    \"\"\"{{ function_description }}\"\"\"
    {{ implementation }}
    return {{ output_model.name }}({{ return_fields }})
""")

input_model = {
    "name": "ExampleNode",
    "fields": [
        {"name": "field1", "type": "int", "description": "An example field"}
    ]
}

output_model = {
    "name": "ExampleNodeOutput",
    "fields": [
        {"name": "result", "type": "int", "description": "The result of the computation"}
    ]
}

function_data = {
    "function_name": "example_node",
    "function_description": "An example node that performs a computation.",
    "implementation": "result = body.field1 * 2",
    "return_fields": "result=result"
}

class FieldTemplate(BaseModel):
    name: str
    type: str
    description: str

class InputModelTemplate(BaseModel):
    name: str
    fields: list[FieldTemplate]

class OutputModelTemplate(BaseModel):
    name: str
    fields: list[FieldTemplate]

class FunctionDataTemplate(BaseModel):
    function_name: str
    function_description: str
    implementation: str
    return_fields: str


if __name__ == "__main__":
    input_model = InputModelTemplate(
        name="ExampleNode",
        fields=[
            FieldTemplate(name="field1", type="int", description="An example field")
        ]
    )

    output_model = OutputModelTemplate(
        name="ExampleNodeOutput",
        fields=[
            FieldTemplate(name="result", type="int", description="The result of the computation")
        ]
    )

    function_data = FunctionDataTemplate(
        function_name="example_node",
        function_description="An example node that performs a computation.",
        implementation="result = body.field1 * 2",
        return_fields="result=result"
    )

    rendered_code = template.render(input_model=input_model, output_model=output_model, **function_data.model_dump())
    print(rendered_code)