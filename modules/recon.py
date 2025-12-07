import requests
import socket
from urllib.parse import urlparse

def sanitize_target(target):
    """
    Cleans input. Converts 'http://site.com/' -> 'site.com'
    """
    target = target.strip()
    if not target.startswith("http"):
        target = "http://" + target # urlparse needs scheme
    
    parsed = urlparse(target)
    return parsed.netloc # Returns just 'site.com'

def get_subdomains(domain):
    # Ensure we are querying a bare domain
    clean_domain = sanitize_target(domain)
    print(f"[+] Recon started for: {clean_domain}")
    
    url = f"https://crt.sh/?q=%.{clean_domain}&output=json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            subdomains = set()
            subdomains.add(clean_domain) # Always include the root
            for entry in data:
                name = entry['name_value']
                if "*" not in name and "@" not in name:
                    subdomains.add(name)
            return list(subdomains)
    except:
        return [clean_domain] # Fallback to just the main target
    return [clean_domain]

def resolve_ip(subdomain):
    try:
        return socket.gethostbyname(subdomain)
    except:
        return None