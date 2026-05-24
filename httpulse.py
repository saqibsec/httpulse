#!/usr/bin/env python3
# ─────────────────────────────────────────────────────────────
# Tool     : httpulse
# Author   : Saqib Siddique (@saqibsec)
# GitHub   : https://github.com/saqibsec/httpulse
# Version  : 1.0
# License  : MIT
# Desc     : Fast concurrent HTTP status checker for Kali Linux
# ─────────────────────────────────────────────────────────────

import argparse
import sys
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

VERSION = "1.0"
AUTHOR  = "Saqib Siddique (@saqibsec)"
GITHUB  = "https://github.com/saqibsec/httpulse"

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORAMA = True
except ImportError:
    COLORAMA = False


# ─── Color helpers ─────────────────────────────────────────────────────────────

def green(text):
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}" if COLORAMA else text

def yellow(text):
    return f"{Fore.YELLOW}{text}{Style.RESET_ALL}" if COLORAMA else text

def red(text):
    return f"{Fore.RED}{text}{Style.RESET_ALL}" if COLORAMA else text

def cyan(text):
    return f"{Fore.CYAN}{text}{Style.RESET_ALL}" if COLORAMA else text

def bold(text):
    return f"{Style.BRIGHT}{text}{Style.RESET_ALL}" if COLORAMA else text


# ─── URL Checker ───────────────────────────────────────────────────────────────

def check_url(url, timeout):
    """Check a single URL and return (url, status_code, reason, category)."""
    url = url.strip()
    if not url or url.startswith("#"):
        return None

    # Auto-prefix scheme if missing
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        response = requests.get(
            url,
            timeout=timeout,
            allow_redirects=True,
            headers={"User-Agent": "httpulse/" + VERSION + " (Kali Linux)"}
        )
        code = response.status_code
        reason = response.reason

        if 200 <= code < 300:
            category = "OK"
        elif 300 <= code < 400:
            category = "REDIRECT"
        elif 400 <= code < 500:
            category = "CLIENT_ERROR"
        else:
            category = "SERVER_ERROR"

        return (url, code, reason, category)

    except requests.exceptions.ConnectionError:
        return (url, 0, "Connection Error", "FAILED")
    except requests.exceptions.Timeout:
        return (url, 0, "Timeout", "FAILED")
    except requests.exceptions.TooManyRedirects:
        return (url, 0, "Too Many Redirects", "FAILED")
    except requests.exceptions.RequestException as e:
        return (url, 0, str(e)[:60], "FAILED")


# ─── Output formatter ──────────────────────────────────────────────────────────

def format_terminal(url, code, reason, category):
    """Return a color-coded terminal line."""
    tag = f"[{code if code else 'ERR'}]"
    line = f"{tag:<8} {url}  ->  {reason}"

    if category == "OK":
        return green(line)
    elif category == "REDIRECT":
        return yellow(line)
    else:
        return red(line)


def format_plain(url, code, reason, category):
    """Return a plain text line for file output."""
    tag = f"[{code if code else 'ERR'}]"
    return f"{tag:<8} {url}  ->  {reason}"


# ─── Banner ────────────────────────────────────────────────────────────────────

def print_banner():
    banner = r"""
  _     _   _                    _
 | |__ | |_| |_ _ __  _   _| |___  ___
 | '_ \| __| __| '_ \| | | | / __|/ _ \
 | | | | |_| |_| |_) | |_| | \__ \  __/
 |_| |_|\__|\__| .__/ \__,_|_|___/\___|
               |_|
    """
    print(cyan(banner))
    print(cyan("  HTTP Status Checker  |  Kali Linux Tool  |  v" + VERSION))
    print(cyan("  Author : " + AUTHOR))
    print(cyan("  GitHub : " + GITHUB + "\n"))


# ─── Argument Parser ───────────────────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(
        prog="httpulse",
        description=bold("httpulse — Fast concurrent HTTP status checker for Kali Linux"),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  httpulse -u https://example.com
  httpulse -f urls.txt
  httpulse -f urls.txt -o results.txt -t 20 --timeout 8
  httpulse -f urls.txt -u https://extra.com -o out.txt

STATUS CODES:
  2xx  ->  OK             (green)
  3xx  ->  Redirect       (yellow)
  4xx  ->  Client Error   (red)
  5xx  ->  Server Error   (red)
  ERR  ->  Failed/Timeout (red)

AUTHOR:
  Saqib Siddique — https://github.com/saqibsec/httpulse
        """
    )

    parser.add_argument(
        "-f", "--file",
        metavar="FILE",
        help="Path to a .txt file containing URLs (one per line)"
    )
    parser.add_argument(
        "-u", "--url",
        metavar="URL",
        help="A single URL to check directly"
    )
    parser.add_argument(
        "-o", "--output",
        metavar="FILE",
        default="results.txt",
        help="Output file to save results (default: results.txt)"
    )
    parser.add_argument(
        "-t", "--threads",
        metavar="NUM",
        type=int,
        default=10,
        help="Number of concurrent threads (default: 10)"
    )
    parser.add_argument(
        "--timeout",
        metavar="SEC",
        type=float,
        default=5.0,
        help="Request timeout in seconds (default: 5)"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="httpulse v" + VERSION + " by " + AUTHOR
    )

    return parser


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = build_parser()
    args = parser.parse_args()

    # Show help if no args given
    if len(sys.argv) == 1:
        print_banner()
        parser.print_help()
        sys.exit(0)

    print_banner()

    # ── Collect URLs ──
    urls = []

    if args.file:
        if not os.path.isfile(args.file):
            print(red("[ERROR] File not found: " + args.file))
            sys.exit(1)
        with open(args.file, "r") as f:
            file_urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        print(cyan("[*] Loaded " + str(len(file_urls)) + " URL(s) from '" + args.file + "'"))
        urls.extend(file_urls)

    if args.url:
        print(cyan("[*] Added direct URL: " + args.url))
        urls.append(args.url)

    if not urls:
        print(red("[ERROR] No URLs provided. Use -f <file> and/or -u <url>"))
        parser.print_help()
        sys.exit(1)

    # Deduplicate while preserving order
    seen = set()
    unique_urls = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            unique_urls.append(u)

    total = len(unique_urls)
    print(cyan("[*] Checking " + str(total) + " unique URL(s) with " + str(args.threads) + " thread(s), timeout=" + str(args.timeout) + "s\n"))
    print(bold("STATUS   URL" + " " * 47 + "REASON"))
    print("-" * 80)

    # ── Run checks ──
    results = []
    stats = {"OK": 0, "REDIRECT": 0, "CLIENT_ERROR": 0, "SERVER_ERROR": 0, "FAILED": 0}

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(check_url, url, args.timeout): url for url in unique_urls}
        for future in as_completed(futures):
            result = future.result()
            if result is None:
                continue
            url, code, reason, category = result
            results.append(result)
            stats[category] += 1
            print(format_terminal(url, code, reason, category))

    # ── Summary ──
    print("\n" + "-" * 80)
    print(bold("SUMMARY"))
    ok_count     = stats["OK"]
    redir_count  = stats["REDIRECT"]
    client_count = stats["CLIENT_ERROR"]
    server_count = stats["SERVER_ERROR"]
    failed_count = stats["FAILED"]
    print("  " + green("OK (2xx):            " + str(ok_count)))
    print("  " + yellow("Redirects (3xx):     " + str(redir_count)))
    print("  " + red("Client Errors (4xx): " + str(client_count)))
    print("  " + red("Server Errors (5xx): " + str(server_count)))
    print("  " + red("Failed/Timeout:      " + str(failed_count)))
    print("  Total checked:       " + str(total))

    # ── Save to file ──
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(args.output, "w") as f:
        f.write("# httpulse results - " + timestamp + "\n")
        f.write("# Author : " + AUTHOR + "\n")
        f.write("# GitHub : " + GITHUB + "\n")
        f.write("# Total: " + str(total) + " | Threads: " + str(args.threads) + " | Timeout: " + str(args.timeout) + "s\n")
        f.write("-" * 80 + "\n")
        order = ["OK", "REDIRECT", "CLIENT_ERROR", "SERVER_ERROR", "FAILED"]
        results_sorted = sorted(results, key=lambda r: order.index(r[3]))
        for url, code, reason, category in results_sorted:
            f.write(format_plain(url, code, reason, category) + "\n")
        f.write("\n# SUMMARY\n")
        for key in order:
            f.write("# " + key + ": " + str(stats[key]) + "\n")

    print("\n" + cyan("[*] Results saved to: " + args.output))


if __name__ == "__main__":
    main()
