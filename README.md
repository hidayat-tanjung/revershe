# Python Reverse Shell Tool
![carbon](https://github.com/user-attachments/assets/2ef5b2ae-005e-453e-a2f7-ab046fa65ec7)
Tool reverse shell sederhana berbasis Python untuk penetration testing yang sah.

## Fitur Utama

- 🚀 **Dual Mode**: Mode listener dan client
- 🔒 **Komunikasi Terenkripsi** (versi advanced)
- 📱 **Multi-Platform**: Bekerja di Windows, Linux, dan macOS
- 💻 **Shell Interaktif**
- 📡 **Port Customizable**

## Persyaratan

- Python 3.6+
- Modul `cryptography` (untuk versi enkripsi)
 ```console
 pip install cryptography
```

# Cara Penggunaan

1. Mode Listener (Target)
 ```console
 python3 reverse_shell.py -l -p 4444
```

2. Mode Client (Attacker)
 ```console
python3 reverse_shell.py -c <IP_TARGET> -p 4444 -i
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

[![GitHub](https://img.shields.io/badge/GitHub-View_Project-blue?logo=github)](https://github.com/hidayat-tanjung/CryptoAnalyzer)


