# 🫀 httpulse

> **Check the pulse of your HTTP links — fast, concurrent, and color-coded.**

`httpulse` is a command-line tool built for **Kali Linux** that checks HTTP status codes of URLs — from a file or a direct link — using concurrent threads for maximum speed. Designed for penetration testers, bug bounty hunters, and developers who need quick, clean link status reports.

---

## 📸 Preview

```
  _     _   _                    _
 | |__ | |_| |_ _ __  _   _| |___  ___
 | '_ \| __| __| '_ \| | | | / __|/ _ \
 | | | | |_| |_| |_) | |_| | \__ \  __/
 |_| |_|\__|\__| .__/ \__,_|_|___/\___|
               |_|

  HTTP Status Checker  |  Kali Linux Tool  |  v1.0
  Author : Saqib Siddique (@saqibsiddique)
  GitHub : https://github.com/saqibsiddique/httpulse

[*] Loaded 5 URL(s) from 'urls.txt'
[*] Checking 5 unique URL(s) with 10 thread(s), timeout=5.0s

STATUS   URL                                               REASON
--------------------------------------------------------------------------------
[200]    https://example.com          ->  OK
[200]    https://google.com           ->  OK
[301]    https://github.com/404page   ->  Moved Permanently
[404]    https://example.com/missing  ->  Not Found
[ERR]    https://dead-link.xyz        ->  Connection Error

--------------------------------------------------------------------------------
SUMMARY
  OK (2xx):            2
  Redirects (3xx):     1
  Client Errors (4xx): 1
  Failed/Timeout:      1
  Total checked:       5

[*] Results saved to: results.txt
```

---

## ✨ Features

- ✅ Check URLs from a **text file** or a **direct CLI argument** (or both)
- ⚡ **Concurrent threads** — check hundreds of links simultaneously
- 🎨 **Color-coded terminal output** — green / yellow / red at a glance
- 💾 **Auto-saves results** to a file, sorted by status category
- 🔁 **Auto-prefixes** `https://` if scheme is missing in URL
- 🧹 **Deduplicates** URLs automatically — no double-checking
- 🛡️ Custom **User-Agent** header identifying the tool
- 🕐 Configurable **timeout** per request
- `--version` flag shows tool version and author

---

## 🖥️ Requirements

- Python 3.6+
- Kali Linux (or any Linux/macOS with Python 3)
- pip3

---

## ⚙️ Installation

### Option 1 — Auto Install (Recommended)

```bash
git clone https://github.com/saqibsiddique/httpulse.git
cd httpulse
chmod +x install.sh
./install.sh
```

After install, run from anywhere:

```bash
httpulse -h
```

---

### Option 2 — Manual Install

```bash
# 1. Clone the repo
git clone https://github.com/saqibsiddique/httpulse.git
cd httpulse

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Copy to PATH and make executable
sudo cp httpulse.py /usr/local/bin/httpulse
sudo chmod +x /usr/local/bin/httpulse
```

---

### Option 3 — Run Directly (No Install)

```bash
git clone https://github.com/saqibsiddique/httpulse.git
cd httpulse
pip3 install -r requirements.txt
python3 httpulse.py -h
```

---

## 🚀 Usage

```
httpulse [-h] [-f FILE] [-u URL] [-o FILE] [-t NUM] [--timeout SEC] [--version]
```

### Flags

| Flag | Long Form | Description | Default |
|------|-----------|-------------|---------|
| `-f` | `--file` | Path to `.txt` file with URLs (one per line) | — |
| `-u` | `--url` | Single URL to check directly | — |
| `-o` | `--output` | Output file to save results | `results.txt` |
| `-t` | `--threads` | Number of concurrent threads | `10` |
| `--timeout` | `--timeout` | Request timeout in seconds | `5` |
| `-h` | `--help` | Show help message and exit | — |
| `--version` | `--version` | Show version and author info | — |

---

## 📖 Examples

```bash
# Check a single URL
httpulse -u https://example.com

# Check all URLs from a file
httpulse -f urls.txt

# Check file + a direct URL together
httpulse -f urls.txt -u https://extra-site.com

# Save results to a custom file
httpulse -f urls.txt -o my_results.txt

# Use 20 threads and 8 second timeout
httpulse -f urls.txt -t 20 --timeout 8

# Full options combined
httpulse -f urls.txt -u https://example.com -o out.txt -t 20 --timeout 8
```

---

## 📄 URL File Format (`urls.txt`)

One URL per line. Lines starting with `#` are treated as comments and skipped.

```
# My target URLs
https://example.com
https://google.com
http://testsite.local
example.org           # scheme auto-added as https://
# https://skipped-comment.com
```

---

## 📊 Status Code Reference

| Code Range | Category | Terminal Color |
|------------|----------|----------------|
| `2xx` | OK — Request successful | 🟢 Green |
| `3xx` | Redirect — Resource moved | 🟡 Yellow |
| `4xx` | Client Error — Not found, forbidden, etc. | 🔴 Red |
| `5xx` | Server Error — Internal server error, etc. | 🔴 Red |
| `ERR` | Failed — Connection error or timeout | 🔴 Red |

---

## 📁 Output File

Results are automatically saved to `results.txt` (or your custom `-o` file). The file is sorted by status category — OK first, then redirects, then errors — and includes a summary at the bottom.

```
# httpulse results - 2025-01-15 14:32:10
# Author : Saqib Siddique (@saqibsiddique)
# GitHub : https://github.com/saqibsiddique/httpulse
# Total: 5 | Threads: 10 | Timeout: 5.0s
--------------------------------------------------------------------------------
[200]    https://example.com           ->  OK
[200]    https://google.com            ->  OK
[301]    https://github.com/404page    ->  Moved Permanently
[404]    https://example.com/missing   ->  Not Found
[ERR]    https://dead-link.xyz         ->  Connection Error

# SUMMARY
# OK: 2
# REDIRECT: 1
# CLIENT_ERROR: 1
# SERVER_ERROR: 0
# FAILED: 1
```

---

## 🗂️ Project Structure

```
httpulse/
├── httpulse.py        # Main tool script
├── requirements.txt   # Python dependencies
├── install.sh         # Auto-installer script
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

---

## 🔧 Uninstall

```bash
sudo rm /usr/local/bin/httpulse
```

---

## 👤 Author

**Saqib Siddique**
- GitHub: [@saqibsiddique](https://github.com/saqibsiddique)

---

## 📜 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute.

---

## ⚠️ Disclaimer

This tool is intended for **legal and authorized use only** — such as testing your own systems, bug bounty programs with proper scope, or educational purposes. The author is not responsible for any misuse of this tool.

---

⭐ If you found this useful, consider giving it a star on GitHub!
