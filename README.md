# H1-High-Value-Finder

A simple, aggressive script to extract **High-Paying** and **Fast-Responding** program handles from your HackerOne account.

## What it does
It crawls your entire H1 inventory (Public/Private) and filters targets based on:
1. **The Money**: Only programs with high average bounties.
2. **The Speed**: Only programs with fast initial response times.
3. **The Status**: Separates Private invites from Public BBP.

## Usage
1. **Config**: Paste your session `Cookie` and `X-Csrf-Token` into the `.env` file.
2. **Filter**: Set your minimum bounty and response time thresholds.
3. **Run**: 
   ```bash
   python h1_downloader.py
4. **Result**: You get a clean list of high-value handles in `results/`.


## ⚖️ Legal & Disclaimer

**This tool is for educational and ethical security research purposes only.**

By using this software, you agree to the following terms:

1. **Compliance:** You are solely responsible for complying with [HackerOne's Terms of Service](https://www.hackerone.com/terms) and any applicable local or international laws.
2. **Authorized Access Only:** You must only use this script with your own authenticated session credentials. Use of this tool to access data without authorization is strictly prohibited.
3. **No Warranty:** This software is provided "as is" without warranty of any kind. The author is not responsible for any consequences resulting from the use of this tool, including but not limited to:
   - Account suspension or termination by HackerOne.
   - IP rate-limiting or blacklisting.
   - Data loss or leakage caused by improper handling of session credentials.
4. **Credential Security:** **NEVER** hardcode your `Cookie` or `X-Csrf-Token` directly into the source code when committing to public repositories. Always use environment variables or a protected `.env` file.

**Use this tool responsibly. Focus on the hunt, respect the platform.**
