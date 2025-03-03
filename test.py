# from scapy.all import *

# def syn_scan(host, port):
#     # Create a SYN packet
#     syn_pkt = IP(dst=host) / TCP(dport=port, flags="S")
#     response = sr1(syn_pkt, timeout=10, verbose=0)
    
#     if response:
#         tcp_flags = response.getlayer(TCP).flags
#         if tcp_flags == 0x12:  # SYN/ACK
#             print(f"Port {port} is open.")
#             # Send RST to gracefully close the connection
#             sr(IP(dst=host) / TCP(dport=port, flags="R"), timeout=1, verbose=0)
#         elif tcp_flags == 0x14:  # RST/ACK
#             print(f"Port {port} is closed.")
#     else:
#         print(f"Port {port} is filtered (no response).")

# syn_scan("owasp.org", 70)

import socket

def scan_port(ip, port, timeout=1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result

def determine_port_status(ip, port):
    result = scan_port(ip, port)
    if result == 0:
        return "Open"
    elif result in [10060, 10035]:  # Connection timed out or WSAEWOULDBLOCK
        return "Filtered/Closed (No Response)"
    elif result == 10061:  # Connection refused
        return "Closed"
    else:
        return f"Unknown (Error code: {result})"

# Example usage
target_ip = "owasp.org"
status = determine_port_status(target_ip, 22)

print(status)