import asyncio
import aiohttp
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from modules.mock_data import get_email_breaches

console = Console()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

SITES = {
    "GitHub": "https://github.com/{}",
    "Twitter/X": "https://twitter.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Instagram": "https://www.instagram.com/{}/"
}

async def check_username(session: aiohttp.ClientSession, site_name: str, url: str, username: str):
    try:
        async with session.get(url, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=5), allow_redirects=False) as response:
            if response.status == 404:
                return site_name, "[bold green]Not Found[/bold green]", " Likely Available"
            elif response.status == 200:
                return site_name, "[bold yellow]Exists / Catch-All[/bold yellow]", " Profile likely exists or login wall."
            else:
                return site_name, f"[dim]HTTP {response.status}[/dim]", " Rate limited or blocked."
    except asyncio.TimeoutError:
        return site_name, "[bold red]Timeout[/bold red]", " Network timeout."
    except Exception as e:
        return site_name, "[bold red]Error[/bold red]", str(e)

async def analyze_username(username: str):
    console.print("\n[bold cyan][*] Initializing Async Username OSINT Module...[/bold cyan]")
    
    table = Table(title="Username Availability Heuristics", box=box.ROUNDED, show_lines=True)
    table.add_column("Platform", style="bold cyan", justify="center")
    table.add_column("Status", style="white", justify="center")
    table.add_column("Details", style="dim", justify="left")

    async with aiohttp.ClientSession() as session:
        tasks = []
        for site_name, url in SITES.items():
            tasks.append(check_username(session, site_name, url.format(username), username))
        
        results = await asyncio.gather(*tasks)
        
        for site, status, details in results:
            table.add_row(site, status, details)
            
    console.print(Panel(table, title="[bold white]Digital Footprint Analysis[/bold white]", border_style="blue"))

def analyze_email(email: str):
    console.print("[bold cyan][*] Initializing Email Breach OSINT Module...[/bold cyan]")
    
    breaches = get_email_breaches(email)
    
    if breaches:
        breach_table = Table(title="⚠️  Simulated Breach Occurrences", box=box.HEAVY, show_lines=True)
        breach_table.add_column("Breach Name", style="bold red")
        breach_table.add_column("Category", style="bold yellow")
        breach_table.add_column("Data Compromised", style="white")  # Fixed column structure
        
        for b in breaches:
            breach_table.add_row(b["breach_name"], b["category"], ", ".join(b["data_types"]))
            
        console.print(Panel(breach_table, title="[bold red]BREACH ALERT[/bold red]", border_style="red"))
    else:
        console.print(f"[bold green][+] No simulated breaches found for {email}.[/bold green]\n")
