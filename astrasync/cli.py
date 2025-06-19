import click
import json
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from . import AstraSync, __version__
from .exceptions import AstraSyncError

console = Console()

@click.group()
@click.version_option(version=__version__)
def cli():
    """AstraSync AI - Universal AI Agent Registration"""
    pass

@cli.command()
@click.argument('agent_file', type=click.Path(exists=True))
@click.option('--email', '-e', help='Developer email')
@click.option('--output', '-o', help='Output file for credentials')
def register(agent_file, email, output):
    """Register an AI agent from any format"""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Loading agent file...", total=None)
            
            client = AstraSync(email=email)
            
            progress.update(task, description="Registering with AstraSync...")
            result = client.register(agent_file)
            
            progress.update(task, description="Registration complete!")
        
        table = Table(title="✅ Registration Successful")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Agent ID", result['agentId'])
        table.add_row("Status", result['status'])
        table.add_row("Trust Score", result.get('trustScore', 'N/A'))
        
        console.print(table)
        
        if output:
            output_path = Path(output)
            with open(output_path, 'w') as f:
                json.dump(result, f, indent=2)
            console.print(f"\n💾 Credentials saved to {output_path}")
            
    except AstraSyncError as e:
        console.print(f"[red]❌ Error:[/red] {e}")
        sys.exit(1)

@cli.command()
def health():
    """Check AstraSync API health"""
    client = AstraSync()
    try:
        with console.status("Checking API health..."):
            response = client.api_client.health_check()
        console.print("[green]✅ API is healthy![/green]")
        console.print(f"Endpoint: {client.api_url}")
    except Exception as e:
        console.print(f"[red]❌ API health check failed:[/red] {e}")
        sys.exit(1)

if __name__ == '__main__':
    cli()
