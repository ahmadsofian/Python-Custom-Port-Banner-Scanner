import socket
import concurrent.futures
import json
import argparse

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 3306: "MySQL", 3389: "RDP"
}

#Custom Payloads Dictionary
# We format these as raw bytes (the 'b' before the string)
CUSTOM_PAYLOADS = {
    80: b"GET / HTTP/1.1\r\nHost: target\r\n\r\n",
    443: b"GET / HTTP/1.1\r\nHost: target\r\n\r\n",
    21: b"HELP\r\n",         # FTP command to list commands
    25: b"EHLO test\r\n",    # SMTP greeting
    110: b"USER test\r\n"    # POP3 greeting
}

scan_results = {}

def scan_port(target, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    
    try:
        s.connect((target, port))
        
        # Smart Payload Selection
        payload = CUSTOM_PAYLOADS.get(port, b"\r\n\r\n")
        
        # Send our smart payload
        s.send(payload)
        
        banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
        service_name = COMMON_PORTS.get(port, "Unknown")
        
        scan_results[port] = {
            "state": "open",
            "service": service_name,
            "banner": banner[:80] if banner else "No banner"
        }
        print(f"[+] Port {port} ({service_name}) is OPEN")
            
    except:
        pass
    finally:
        s.close()

def main():
    parser = argparse.ArgumentParser(description="Custom Python Port & Banner Scanner")
    parser.add_argument("-t", "--target", help="Target IP or Domain (e.g., scanme.nmap.org)", required=True)
    parser.add_argument("-p", "--ports", help="Port range to scan (e.g., 20-100)", default="1-1024")
    
    args = parser.parse_args()
    target_host = args.target
    
    try:
        start_port, end_port = args.ports.split('-')
        ports_to_scan = range(int(start_port), int(end_port) + 1)
    except ValueError:
        print("[-] Invalid port format. Please use start-end (e.g., 20-100)")
        return

    print(f"Starting multi-threaded scan on {target_host} (Ports {start_port}-{end_port})...\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for port in ports_to_scan:
            executor.submit(scan_port, target_host, port)

    print("\nScan completed! Saving results...")
    
    output_filename = f"{target_host}_scan.json"
    with open(output_filename, "w") as outfile:
        json.dump(scan_results, outfile, indent=4)

    print(f"Results successfully saved to '{output_filename}'!")

if __name__ == "__main__":
    main()