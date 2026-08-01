#!/usr/bin/env python3
"""Small local server for Windows, Linux and Termux."""
from __future__ import annotations
import argparse
import http.server
import os
import socketserver
import threading
import webbrowser
from pathlib import Path

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def main() -> None:
    parser = argparse.ArgumentParser(description="Serve HackTheBasics.gr locally.")
    parser.add_argument("--host", default="127.0.0.1", help="Listening address. Use 0.0.0.0 only for trusted LAN access.")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    os.chdir(Path(__file__).resolve().parent)
    handler = http.server.SimpleHTTPRequestHandler
    with ReusableTCPServer((args.host, args.port), handler) as server:
        url = f"http://127.0.0.1:{args.port}/"
        print(f"HackTheBasics.gr is available at {url}")
        print("Press Ctrl+C to stop.")
        if not args.no_browser:
            threading.Timer(0.7, lambda: webbrowser.open(url)).start()
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    main()
