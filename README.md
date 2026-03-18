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
