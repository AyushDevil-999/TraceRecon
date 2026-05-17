import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from modules.mock_data import get_phone_leak_data

console = Console()

def analyze_phone_number(number_str: str):
    console.print("\n[bold cyan][*] Initializing Phone Number OSINT Module...[/bold cyan]")
    
    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse(number_str, None)
        
        # Validate
        is_valid = phonenumbers.is_valid_number(parsed_number)
        is_possible = phonenumbers.is_possible_number(parsed_number)
        
        # Extract Metadata
        region = geocoder.description_for_number(parsed_number, "en")
        timezones = timezone.time_zones_for_number(parsed_number)
        telecom_provider = carrier.name_for_number(parsed_number, "en")
        
        # Format output
        validity_str = "[bold green]VALID[/bold green]" if is_valid else "[bold red]INVALID[/bold red]"
        if not is_valid and is_possible:
            validity_str = "[bold yellow]POSSIBLE BUT INVALID FORMAT[/bold yellow]"
            
        tz_str = ", ".join(timezones) if timezones else "Unknown"
        carrier_str = telecom_provider if telecom_provider else "Unknown / VoIP"

        # Build Basic Info Table
        basic_table = Table(title="Phone Number Metadata", box=box.ROUNDED, show_lines=True)
        basic_table.add_column("Parameter", style="bold cyan", justify="right")
        basic_table.add_column("Extracted Data", style="white")
        
        basic_table.add_row("Input Number", str(parsed_number.national_number))
        basic_table.add_row("International Format", phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL))
        basic_table.add_row("Validity Status", validity_str)
        basic_table.add_row("Country / Region", region or "Unknown")
        basic_table.add_row("Timezone(s)", tz_str)
        basic_table.add_row("Carrier / Provider", carrier_str)
        
        console.print(Panel(basic_table, title="[bold white]Telecom Reconnaissance[/bold white]", border_style="blue"))

        # Mock Data Enrichment (Security Report Structure)
        if is_valid:
            console.print("\n[bold yellow][*] Querying simulated historical breach/web-directory registries...[/bold yellow]")
            formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            leak_data = get_phone_leak_data(formatted_number)
            
            if leak_data:
                leak_table = Table(title="⚠️  SIMULATED PII ENRICHMENT (Breach/Web Directory Structure)", box=box.HEAVY, show_lines=True)
                leak_table.add_column("Field", style="bold red", justify="right")
                leak_table.add_column("Simulated Data", style="bold yellow")
                
                leak_table.add_row("Database Status", leak_data["status"])
                leak_table.add_row("Associated Name", leak_data["name"])
                leak_table.add_row("Father's Name", leak_data["father_name"])
                leak_table.add_row("Historical Address", leak_data["address"])
                leak_table.add_row("Location Status", leak_data["live_location_status"])
                
                console.print(Panel(leak_table, title="[bold red]CRITICAL: Simulated PII Found[/bold red]", border_style="red"))
                console.print("[bold dim red]Disclaimer: The above data is strictly mocked. Obtaining this data passively is generally not possible without illicit means.[/bold dim red]")
            else:
                console.print(f"[bold green][+] No simulated PII found in local educational databases for {formatted_number}.[/bold green]")

    except phonenumbers.NumberParseException as e:
        console.print(f"[bold red][!] Error parsing phone number: {e}[/bold red]")
    except Exception as e:
        console.print(f"[bold red][!] An unexpected error occurred: {e}[/bold red]")
