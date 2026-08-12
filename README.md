# Python Custom Port & Banner Scanner 🕵️‍♂️

A lightweight, multi-threaded TCP port scanner and banner grabber written entirely in Python. 

This tool was built as a foundational cybersecurity project to explore low-level network interactions, the TCP 3-Way Handshake, and socket programming. It goes beyond basic port scanning by dynamically identifying running services and deploying protocol-specific payloads to extract software banners.

## 🧠 How It Works

Instead of relying on external tools like Nmap, this script interacts directly with the operating system's networking stack using Python's built-in `socket` library:
1. **TCP Handshake:** Attempts a full TCP connection (`SYN` -> `SYN-ACK` -> `ACK`) to determine if a port is in an **Open** state.
2. **Smart Banner Grabbing:** Different services speak different languages. Once a connection is established, the scanner checks the port number and sends a custom byte payload (e.g., sending `EHLO test\r\n` to Port 25 for SMTP, or `GET / HTTP/1.1\r\n\r\n` to Port 80 for HTTP).
3. **Response Parsing:** Captures the server's response (the banner), stripping away excess data to reveal the underlying software version or server status.

## ✨ Key Features

* **Multi-Threaded Performance:** Utilizes `concurrent.futures` to scan multiple ports concurrently, significantly reducing scan times while remaining stable.
* **Smart Protocol Payloads:** Deploys custom byte payloads based on the target port to coax accurate banners out of different services without causing the connection to drop.
* **Service Name Mapping:** Automatically translates raw port numbers into human-readable service names (SSH, HTTP, FTP, etc.) using a built-in dictionary.
* **JSON Output:** Automatically formats and saves scan results into a clean, parsed `.json` file for easy integration with reporting tools or other scripts.
* **Zero External Dependencies:** Built using strictly Python Standard Library modules. No `pip install` required!

## 🛠️ Prerequisites & Installation

Since this tool uses only standard Python libraries, there is no need to install external packages like `requests` or `scapy`. All you need is Python 3.x installed on your machine.
