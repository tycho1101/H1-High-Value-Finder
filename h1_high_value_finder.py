import requests
import pandas as pd
import time
import os
import math
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ================= Configuration =================
COOKIE = os.getenv("H1_COOKIE")
CSRF_TOKEN = os.getenv("H1_CSRF_TOKEN")

# Filtering Thresholds (Set to 0 to include all BBP)
MIN_AVG_BOUNTY = int(os.getenv("MIN_AVG_BOUNTY", 0))
MIN_RESOLVED_COUNT = int(os.getenv("MIN_RESOLVED_COUNT", 0))
# =================================================

def clean_val(v):
    """Sanitize headers to avoid encoding errors."""
    if not v: return ""
    return "".join(c for c in str(v) if 32 <= ord(c) <= 126).strip()

def fetch_h1_data():
    url = "https://hackerone.com/graphql"
    
    # Headers optimized to mimic discovery search behavior
    headers = {
        "Host": "hackerone.com",
        "Cookie": clean_val(COOKIE),
        "X-Csrf-Token": clean_val(CSRF_TOKEN),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json",
        "X-Product-Area": "opportunity_discovery",
        "Origin": "https://hackerone.com",
        "Referer": "https://hackerone.com/opportunities/all/search"
    }
    
    cursor = None
    all_results = []
    
    # GraphQL Query for full inventory retrieval
    query = """
    query getDetailedInventory($cursor: String) {
      teams(first: 100, after: $cursor) {
        pageInfo { hasNextPage, endCursor }
        nodes {
          handle
          name
          average_bounty_lower_amount
          average_bounty_upper_amount
          resolved_report_count
          offers_bounties
          state
          most_recent_sla_snapshot {
            average_time_to_first_program_response
          }
        }
      }
    }
    """

    print("🚀 Starting pagination to fetch HackerOne inventory...")

    while True:
        payload = {"query": query, "variables": {"cursor": cursor}}
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=20)
            if resp.status_code != 200:
                print(f"❌ Error: Received status code {resp.status_code}")
                break
            
            data = resp.json()
            teams_data = data.get('data', {}).get('teams', {})
            nodes = teams_data.get('nodes', [])
            
            if not nodes: break
            
            for node in nodes:
                # Logic: Filter only for Bounty Programs (BBP)
                if node.get('offers_bounties'):
                    lower = node.get('average_bounty_lower_amount') or 0
                    upper = node.get('average_bounty_upper_amount') or 0
                    avg_bounty = (float(lower) + float(upper)) / 2
                    resolved = node.get('resolved_report_count') or 0
                    
                    # Apply custom filtering
                    if avg_bounty >= MIN_AVG_BOUNTY and resolved >= MIN_RESOLVED_COUNT:
                        is_private = node.get('state') == 'soft_launched'
                        all_results.append({
                            "Handle": node['handle'],
                            "Name": node['name'],
                            "Type": "Private" if is_private else "Public",
                            "Avg_Bounty": round(avg_bounty, 2),
                            "Resolved_Total": resolved,
                            "First_Response_Hrs": node.get('most_recent_sla_snapshot', {}).get('average_time_to_first_program_response')
                        })

            if not teams_data.get('pageInfo', {}).get('hasNextPage'):
                break
                
            cursor = teams_data['pageInfo']['endCursor']
            print(f"✅ Fetched page ending with cursor: {cursor[:10]}... | Total BBP found: {len(all_results)}")
            time.sleep(1.5) # Anti-WAF delay
            
        except Exception as e:
            print(f"⚠️ Exception during runtime: {e}")
            break

    # --- Export Processing ---
    if all_results:
        df = pd.DataFrame(all_results)
        if not os.path.exists('results'): os.makedirs('results')
        
        # Save structured CSV
        ts = int(time.time())
        df[df['Type'] == 'Private'].to_csv(f"results/private_{ts}.csv", index=False)
        df[df['Type'] == 'Public'].to_csv(f"results/public_{ts}.csv", index=False)
        
        # Save plaintext handles for automation
        with open('results/private_handles.txt', 'w') as f:
            f.write("\n".join(df[df['Type'] == 'Private']['Handle'].tolist()))
        with open('results/public_handles.txt', 'w') as f:
            f.write("\n".join(df[df['Type'] == 'Public']['Handle'].tolist()))
            
        print(f"\n🎉 Task Finished! Data saved in 'results/' directory.")
    else:
        print("\n🔎 No active BBP programs found with current credentials.")

if __name__ == "__main__":
    fetch_h1_data()
