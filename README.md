🚀 ASM Pro - Attack Surface Manager

ASM Pro is a comprehensive, GUI-based security tool designed to automate the reconnaissance phase of a penetration test. It bridges the gap between Passive OSINT (Google Dorking) and Active Network Scanning (Nmap), providing a unified dashboard for vulnerability assessment.

Designed for security researchers and students to visualize the "Attack Surface" of a target infrastructure in real-time.

📸 Dashboard Preview

<img width="960" height="540" alt="image" src="https://github.com/user-attachments/assets/351e9b60-081f-42a1-bd58-fa0816e2745e" />


✨ Key Features

1. 🕵️ Passive Reconnaissance (OSINT)

Automated Google Dorking: Scrapes search engines to find exposed sensitive files (SQL dumps, Log files, Env configurations) without touching the target server.

Subdomain Enumeration: Uses Certificate Transparency logs (CRT.sh) to map hidden subdomains.

2. ⚡ Active Scanning

Port Enumeration: Multi-threaded Nmap integration to identify open TCP ports.

Service Fingerprinting: Detects exact software versions (e.g., Apache 2.4.49 vs Apache 2.2).

Live Terminal: Integrated bottom-console providing real-time hacker-style feedback.

3. 🛡️ Vulnerability Intelligence

CVE Mapping: Automatically correlates detected service versions with the National Vulnerability Database (NVD) and CIRCL API.

Risk Scoring: Assigns CVSS severity scores (Critical, High, Medium, Low) to findings.

Visual Reporting: Displays findings in modern, color-coded "Risk Cards."

4. 💻 Modern UI/UX

Built with CustomTkinter for a professional Dark Mode aesthetic.

State Management: Stop/Start scanning capabilities without freezing the UI.

Thread-Safe: Background processing ensures the interface remains responsive during heavy scans.

🛠️ Installation

Prerequisites

Python 3.x

Nmap: Must be installed and added to your system PATH.

Download Nmap for Windows/Linux

Setup Guide

# 1. Clone the repository
git clone [https://github.com/YourUsername/ASM-Pro.git](https://github.com/YourUsername/ASM-Pro.git)
cd ASM-Pro

# 2. Create a virtual environment (Recommended)
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt


Dependencies (requirements.txt)

customtkinter
python-nmap
requests
googlesearch-python
packaging


🚀 Usage

Launch the Tool:

python gui_app.py


Enter Target: Type a domain name (e.g., demo.testfire.net) in the top search bar.

Initiate Scan: Click the START SCAN button.

Monitor: Watch the Live Terminal for progress and the Vulnerability Intelligence panel for results.

Note: To stop a scan midway, press the STOP SCAN button (Red).

🏗️ Project Architecture

The tool follows a modular architecture for maintainability:

ASM-Pro/
│
├── gui_app.py           # Main Entry Point & UI Logic
├── requirements.txt     # Dependency List
│
└── modules/             # Core Logic Packages
    ├── __init__.py
    ├── recon.py         # Subdomain & Sanitization Logic
    ├── scanner.py       # Nmap Wrapper & Port Analysis
    ├── intel.py         # CVE API & Vulnerability Database
    └── dorking.py       # Google Dorking & OSINT Logic


⚠️ Legal Disclaimer

EDUCATIONAL PURPOSES ONLY.

This tool is designed for security research and educational use within the context of a Cybersecurity degree program.

Do not scan targets you do not own or have explicit permission to test.

The authors are not responsible for any misuse or damage caused by this program.

Scanning unauthorized networks is illegal and a violation of the Computer Fraud and Abuse Act (CFAA).

Recommended Safe Targets for Testing:

demo.testfire.net (IBM)

testhtml5.vulnweb.com (Acunetix)

