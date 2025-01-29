from jinja2 import FileSystemLoader
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Union


from pydantic import BaseModel, Field
from typing import Optional

from jinja2 import Environment

from dslmodel import DSLModel, init_instant

env = Environment(loader=FileSystemLoader("templates"), trim_blocks=True, lstrip_blocks=True)


class Argument(BaseModel):
    """Represents an argument in a command with Annotated style."""
    name: str = Field(..., description="The name of the argument.")
    type: str = Field(..., description="The type of the argument (e.g., str, int).")
    help: Optional[str] = Field(None, description="The help text for the argument.")
    rich_help_panel: Optional[str] = Field(None, description="The help panel category for the argument.")
    default: Optional[str] = Field(None, description="The default value for the argument.")


class Option(BaseModel):
    name: str
    type: str
    prompt: Optional[Union[bool, str]] = None
    help: Optional[str] = None
    rich_help_panel: Optional[str] = None
    show_default: Optional[bool] = None
    default: Optional[str] = None


class Signature(DSLModel):
    function_name: str
    arguments: List[Argument]
    options: List[Option]
    docstring: str


class Docstring(BaseModel):
    """Represents the docstring for a command."""
    summary: str = Field(..., description="A short summary of the command.")
    arguments: List[Argument] = Field(..., description="Arguments documented in the docstring.")
    options: List[Option] = Field(..., description="Options documented in the docstring.")
    returns: str = Field(..., description="Description of the return value.")


class Command(BaseModel):
    """Represents a CLI command."""
    name: str = Field(..., description="The name of the command.")
    help_text: str = Field(..., description="Help text for the command.")
    docstring: Docstring = Field(..., description="The docstring for the command.")
    signature: Signature = Field(..., description="The signature of the command.")


class App(BaseModel):
    """Represents the entire Typer application."""
    app_help: str = Field(..., description="Help text for the Typer application.")
    commands: List[Command] = Field(..., description="List of commands in the application.")


def render_option(option: Option) -> str:
    """Renders the option template with the provided data."""
    template = env.get_template("option.j2")
    return template.render(ctx=option)


def render_signature(signature: Signature) -> str:
    """Renders the signature template using the provided data."""
    template = env.get_template("signature.j2")
    return template.render(ctx=signature.mod)


def render(template_name: str, model: BaseModel) -> str:
    """Renders the template using the provided model."""
    template = env.get_template(template_name)
    print(model.model_dump())
    return template.render(**model.model_dump())


if __name__ == "__main__":
    # Render the template

    init_instant()

    sig = Signature.from_prompt("Create a function called 'review_code' with 2 arguments and 2 options. The function should perform a code review on the specified repository and branch.")
    print(sig.to_yaml())

    rendered_signature = render("signature.j2", sig)
    print(rendered_signature)
