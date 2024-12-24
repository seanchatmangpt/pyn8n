"""pyn8n CLI."""

import typer
from rich import print

from pyn8n.client import N8nClient
from pyn8n.cmds import devops

app = typer.Typer()

app.add_typer(devops.app, name="devops")

@app.command()
def fire(name: str = "Chell") -> None:
    """Fire portal gun."""
    print(f"[bold red]Alert![/bold red] {name} fired [green]portal gun[/green] :boom:")

    client = N8nClient()


@app.command()
def version() -> None:
    """Print version."""
    print("pyn8n v0.1.0")
