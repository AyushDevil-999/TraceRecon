import re
import click
from rich.console import Console
from rich.panel import Panel

from modules.phone_recon import analyze_phone_number
from modules.user_email_recon import analyze_username, analyze_email

console = Console()

def is_phone_number(input_str: str) -> bool:
    cleaned = input_str.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    return re.match(r'^\+?\d{7,15}$', cleaned) is not None

def is_email(input_str: str) -> bool:
    return re.match(r'^[^@]+@[^@]+\.[^@]+$', input_str) is not None

@click.command()
@click.argument("target")
def main(target):
    """🛡️ TraceRecon: Educational OSINT Reconnaissance Tool"""
    
    banner = """
    [bold blue]
    ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗
    ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║
    ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║
    ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║
    ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝
    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝
    [/bold blue]
    [bold dim red]DISCLAIMER: Strictly for educational & authorized security auditing only.[/bold dim red]
    """
    console.print(Panel(banner, border_style="cyan", expand=False))
    
    target = target.strip()
    
    try:
        if is_phone_number(target):
            analyze_phone_number(target)
        elif is_email(target):
            analyze_email(target)
        else:
            import asyncio
            asyncio.run(analyze_username(target))
    except KeyboardInterrupt:
        console.print("\n[bold red][!] Process interrupted by user.[/bold red]")
    except Exception as e:
        console.print(f"\n[bold red][!] Fatal Error: {e}[/bold red]")

if __name__ == "__main__":
    main()
