import csv
import os
import calendar
import random
import sys
from datetime import datetime

# ══════════════════════════════════════════════════════════════════
# CONFIGURATION & CONSTANTS
# ══════════════════════════════════════════════════════════════════
CSV_FILE = "dataset.csv"
MY_BUDGET = 50000.0  # Monthly Budget in ₹

# ══════════════════════════════════════════════════════════════════
# 1. UTILITIES & DATA PERSISTENCE (The Agent's Memory)
# ══════════════════════════════════════════════════════════════════

def reset_data():
    """Wipes the dataset for a fresh demo run. Essential for hackathon resets."""
    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)
        print("🧹 Clean Slate: dataset.csv has been deleted.")
    else:
        print("ℹ️ Nothing to reset.")

def fetch_realtime_cloud_data():
    """
    Simulates real-time cloud pulling. 
    Includes Abhinav's 20% anomaly detection logic.
    """
    last_day = 0
    if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
        try:
            with open(CSV_FILE, 'r') as f:
                rows = list(csv.DictReader(f))
                if rows and 'day' in rows[-1]:
                    last_day = int(rows[-1]['day'])
        except Exception:
            last_day = 0

    new_day_num = last_day + 1
    
    # 20% Probability of an Anomaly/Spike (The 'Problem' the Agent must solve)
    is_spike = random.random() < 0.2 

    if is_spike:
        # High spend to trigger the Gemini Reasoning
        amount = random.uniform(3500, 6000)
        service = "Lambda (Anomaly Spike)"
    else:
        # Normal operational spend
        amount = random.uniform(1100, 1400)
        service = random.choice(["EC2", "S3", "RDS"])

    return [{
        "day": new_day_num,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "amount": round(amount, 2),
        "service": service
    }]

def append_to_csv(data_list):
    """Saves the Agent's observations to permanent memory."""
    file_exists = os.path.isfile(CSV_FILE) and os.path.getsize(CSV_FILE) > 0
    keys = ["day", "date", "amount", "service"]
    
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        if not file_exists:
            writer.writeheader()
        writer.writerows(data_list)

# ══════════════════════════════════════════════════════════════════
# 2. AGENTIC MATH (The Observation Analysis)
# ══════════════════════════════════════════════════════════════════

def perform_analysis(budget):
    """
    Reads the CSV memory and calculates the 'Goal-Gap'.
    This feeds the Gemini Brain and the UI.
    """
    amounts = []
    if not os.path.exists(CSV_FILE): 
        return None

    with open(CSV_FILE, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                amounts.append(float(row['amount']))
            except (ValueError, KeyError):
                continue

    if not amounts: 
        return None

    days_recorded = len(amounts)
    total_spent = sum(amounts)
    avg_daily = total_spent / days_recorded
    
    now = datetime.now()
    # Dynamic calculation of days in the current month
    total_days_in_month = calendar.monthrange(now.year, now.month)[1]
    days_remaining = max(0, total_days_in_month - days_recorded)
    
    # The 'Forecast' logic: How much will we spend if we don't act?
    forecast = total_spent + (avg_daily * days_remaining)
    over_amt = round(forecast - budget, 2)
    over_pct = round((over_amt / budget) * 100, 2) if budget > 0 else 0
    
    # The 'Action Metric': How much must the Agent cut per day to hit the goal?
    required_cut = round(over_amt / days_remaining, 2) if over_amt > 0 and days_remaining > 0 else 0

    return {
        "total_spent": round(total_spent, 2),
        "forecast": round(forecast, 2),
        "over_amt": max(0, over_amt),
        "over_pct": max(0, over_pct),
        "required_daily_cut": required_cut,
        "days_remaining": days_remaining,
        "history_count": days_recorded,
        "last_day_spend": amounts[-1] if amounts else 0,
        "is_breach": over_amt > 0
    }

# ══════════════════════════════════════════════════════════════════
# 3. STANDALONE TEST EXECUTION
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Handle the 'reset' command for demo purposes
    if len(sys.argv) > 1 and sys.argv[1].lower() == "reset":
        reset_data()
        sys.exit()

    print(f"--- 🤖 AGENTIC CALCULATION ENGINE (Budget: ₹{MY_BUDGET}) ---")
    
    # 1. Fetch & Store (Observation)
    new_data = fetch_realtime_cloud_data()
    append_to_csv(new_data)
    
    # 2. Analyze (Reasoning Preparation)
    m = perform_analysis(MY_BUDGET)
    
    if m:
        print(f"💸 Today's Spend: ₹{m['last_day_spend']}")
        print(f"📊 Progress: Day {m['history_count']} logged in memory.")
        print(f"🔮 Month-End Projection: ₹{m['forecast']}")
        
        if m['is_breach']:
            print(f"🚨 ALERT: Predicted overrun of ₹{m['over_amt']} ({m['over_pct']}%)")
            print(f"🎯 AGENTIC GOAL: Target reduction of ₹{m['required_daily_cut']}/day.")
        else:
            print("🟢 STATUS: Spend is within healthy budget limits.")

    print("--- 🤖 RUN COMPLETE ---")
