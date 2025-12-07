import nmap

def scan_host(ip):
    nm = nmap.PortScanner()
    try:
        # -sV: Version Detect
        # --open: Only show open ports
        # -T4: Fast timing
        # --top-ports 100: Check most common ports (HTTP, SSH, SQL, etc)
        nm.scan(ip, arguments='-sV --open -T4 --top-ports 100')
        
        results = []
        if ip in nm.all_hosts():
            if 'tcp' in nm[ip]:
                for port in nm[ip]['tcp']:
                    data = nm[ip]['tcp'][port]
                    results.append({
                        'port': port,
                        'service': data['product'] or data['name'], # Fallback to name if product empty
                        'version': data['version']
                    })
        return results
    except Exception as e:
        print(f"[-] Nmap Error: {e}")
        return []