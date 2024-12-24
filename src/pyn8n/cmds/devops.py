import typer
import subprocess

app = typer.Typer(help="CLI tool to manage Monica CRM and n8n using Docker Compose.")

DOCKER_COMPOSE_FILE = "docker-compose.yml"

@app.command()
def init(app_key: str = typer.Option(..., help="Base64 encoded APP_KEY for Monica CRM")):
    """Initialize the application by setting up and starting all services."""
    typer.echo("Initializing the application...")
    try:
        # Generate APP_KEY if not provided
        if not app_key:
            typer.echo("Generating APP_KEY...")
            result = subprocess.run(["openssl", "rand", "-base64", "32"], capture_output=True, text=True)
            app_key = f"base64:{result.stdout.strip()}"
            typer.echo(f"Generated APP_KEY: {app_key}")

        # Start services
        typer.echo("Starting services...")
        subprocess.run(["docker-compose", "-f", DOCKER_COMPOSE_FILE, "up", "-d"], check=True)

        # Set up Monica CRM
        typer.echo("Setting up Monica CRM...")
        subprocess.run(["docker-compose", "-f", DOCKER_COMPOSE_FILE, "exec", "monica-app", "php", "artisan", "setup:production"], check=True)

        typer.echo("Application initialized successfully.")
    except subprocess.CalledProcessError as e:
        typer.echo(f"An error occurred during initialization: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def start():
    """Start all services."""
    typer.echo("Starting services...")
    subprocess.run(["docker-compose", "-f", DOCKER_COMPOSE_FILE, "up", "-d"], check=True)
    typer.echo("Services started.")

@app.command()
def stop():
    """Stop all services."""
    typer.echo("Stopping services...")
    subprocess.run(["docker-compose", "-f", DOCKER_COMPOSE_FILE, "down"], check=True)
    typer.echo("Services stopped.")

@app.command()
def monica_setup(app_key: str = typer.Option(..., help="Base64 encoded APP_KEY for Monica CRM")):
    """Set up Monica CRM."""
    typer.echo("Setting up Monica CRM...")
    subprocess.run(["docker-compose", "-f", DOCKER_COMPOSE_FILE, "exec", "monica-app", "php", "artisan", "setup:production"], check=True)
    typer.echo("Monica CRM setup complete.")

@app.command()
def logs(service: str = typer.Argument(..., help="Service name (e.g., monica-app, n8n)")):
    """View logs for a specific service."""
    typer.echo(f"Fetching logs for {service}...")
    subprocess.run(["docker-compose", "-f", DOCKER_COMPOSE_FILE, "logs", "-f", service], check=True)

@app.command()
def restart(service: str = typer.Argument(..., help="Service name (e.g., monica-app, n8n)")):
    """Restart a specific service."""
    typer.echo(f"Restarting {service}...")
    subprocess.run(["docker-compose", "-f", DOCKER_COMPOSE_FILE, "restart", service], check=True)
    typer.echo(f"Service {service} restarted.")

@app.command()
def status():
    """Show the status of all services."""
    typer.echo("Checking service status...")
    subprocess.run(["docker-compose", "-f", DOCKER_COMPOSE_FILE, "ps"], check=True)

@app.command()
def generate_app_key():
    """Generate a secure Base64 APP_KEY for Monica CRM."""
    typer.echo("Generating APP_KEY...")
    result = subprocess.run(["openssl", "rand", "-base64", "32"], capture_output=True, text=True)
    app_key = result.stdout.strip()
    typer.echo(f"Generated APP_KEY: base64:{app_key}")

if __name__ == "__main__":
    app()
