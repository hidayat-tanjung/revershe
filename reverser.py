import socket
import ssl
import os
import subprocess
import threading
import sqlite3
import logging
import time

# CONFIGURATION
HOST = '0.0.0.0'  # For listener
PORT = 4444
CERTFILE = 'cert.pem'  # Self-signed cert
KEYFILE = 'key.pem'
AUTH_TOKEN = 'my_secret_token'
LOG_DB = 'shell_logs.db'

# DATABASE LOGGER SETUP
def init_db():
    conn = sqlite3.connect(LOG_DB)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ip TEXT,
            command TEXT,
            output TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_to_db(ip, command, output):
    conn = sqlite3.connect(LOG_DB)
    cur = conn.cursor()
    cur.execute('INSERT INTO logs (timestamp, ip, command, output) VALUES (?, ?, ?, ?)',
                (time.strftime('%Y-%m-%d %H:%M:%S'), ip, command, output[:1000]))
    conn.commit()
    conn.close()

# TLS WRAPPED LISTENER
class SecureShellServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        init_db()

    def handle_client(self, connstream, addr):
        try:
            # Authentication Step
            token = connstream.recv(1024).decode()
            if token != AUTH_TOKEN:
                connstream.send(b'Invalid token')
                connstream.close()
                return
            connstream.send(b'Authenticated')

            while True:
                command = connstream.recv(2048).decode().strip()
                if not command:
                    break
                if command.lower() == 'exit':
                    break
                output = self.execute_command(command)
                connstream.send(output.encode())
                log_to_db(addr[0], command, output)
        except Exception as e:
            logging.error(f"Session error: {e}")
        finally:
            connstream.close()

    def execute_command(self, cmd):
        if cmd.startswith('cd '):
            try:
                os.chdir(cmd[3:].strip())
                return f"Changed directory to {os.getcwd()}"
            except Exception as e:
                return str(e)
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout + result.stderr
        except Exception as e:
            return str(e)

    def start(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)

        bindsocket = socket.socket()
        bindsocket.bind((self.host, self.port))
        bindsocket.listen(5)
        print(f"[+] Listening with TLS on {self.host}:{self.port}")

        while True:
            newsocket, addr = bindsocket.accept()
            connstream = context.wrap_socket(newsocket, server_side=True)
            threading.Thread(target=self.handle_client, args=(connstream, addr)).start()

# CLIENT SIDE
class SecureShellClient:
    def __init__(self, server_ip, port, token):
        self.server_ip = server_ip
        self.port = port
        self.token = token

    def start(self):
        context = ssl._create_unverified_context()
        sock = socket.create_connection((self.server_ip, self.port))
        ssock = context.wrap_socket(sock, server_hostname=self.server_ip)
        
        ssock.send(self.token.encode())
        response = ssock.recv(1024).decode()
        if response != 'Authenticated':
            print("[!] Auth failed")
            return

        print("[+] Connected and authenticated")

        try:
            while True:
                cmd = input("shell> ")
                if not cmd:
                    continue
                ssock.send(cmd.encode())
                if cmd.lower() == 'exit':
                    break
                output = ssock.recv(8192).decode()
                print(output)
        finally:
            ssock.close()

# USAGE EXAMPLE
# Server: SecureShellServer(HOST, PORT).start()
# Client: SecureShellClient('127.0.0.1', PORT, AUTH_TOKEN).start()
