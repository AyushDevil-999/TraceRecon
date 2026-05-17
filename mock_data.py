"""
Simulated OSINT Databases for Educational Purposes.
Demonstrates how data structures look in actual breach-dump parsing 
or public directory aggregations without touching real PII.
"""

# Simulated Historical Breach Database
BREACH_DB = {
    "test@example.com": [
        {"breach_name": "MockSocial_2021", "category": "Social Media", "data_types": ["Email", "Hashed Password", "IP"]},
        {"breach_name": "FakeShop_2023", "category": "E-Commerce", "data_types": ["Email", "Plain Text Password", "Address"]}
    ],
    "admin@security.com": [
        {"breach_name": "DarkWeb_Forums_2019", "category": "Forum", "data_types": ["Email", "Clear Password"]}
    ]
}

# Simulated Public Web Directory / Historical Leak Data for Phones
PHONE_LEAK_DB = {
    "+14155552671": {
        "status": "Found in Simulated Historic Web Directory",
        "name": "John Doe",
        "father_name": "Richard Doe",
        "address": "123 Cybersecurity Ave, San Francisco, CA",
        "live_location_status": "Simulated: Historically active in San Francisco, CA. [LEGAL NOTE: Real-time GPS tracking requires a warrant/specialized telco access; cannot be done via passive OSINT.]"
    },
    "+919876543210": {
        "status": "Found in Simulated Data Breach",
        "name": "Jane Smith",
        "father_name": "Robert Smith",
        "address": "456 Recon Lane, Mumbai, India",
        "live_location_status": "Simulated: Last known registration location Mumbai, India. [LEGAL NOTE: Real-time GPS tracking requires a warrant/specialized telco access; cannot be done via passive OSINT.]"
    }
}

def get_email_breaches(email: str) -> list:
    return BREACH_DB.get(email.lower(), [])

def get_phone_leak_data(phone: str) -> dict:
    return PHONE_LEAK_DB.get(phone, None)
