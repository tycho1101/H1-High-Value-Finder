# H1-Bounty-Inventory-Downloader

A lightweight, automated script for Bug Bounty Hunters to download their entire HackerOne program inventory. It specifically focuses on **BBP (Bounty Programs)** and automatically separates Public and Private invites.

## 🌟 Key Features
- **Bypass Pagination**: Automatically crawls through 600+ programs using GraphQL cursors.
- **Private Program Detection**: Identifies and separates your private invites from public programs.
- **Automation Ready**: Exports clean `.txt` handle lists ready to be piped into tools like `subfinder`, `httpx`, or `nuclei`.
- **WAF Friendly**: Mimics browser headers and includes CSRF token validation to prevent session blocking.

## 🚀 Quick Start

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/h1-inventory-downloader.git](https://github.com/your-username/h1-inventory-downloader.git)
   cd h1-inventory-downloader
