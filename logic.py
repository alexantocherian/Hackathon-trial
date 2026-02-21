import csv
import os
import calendar
import random
import sys
from datetime import datetime, timedelta

# ══════════════════════════════════════════════════════════════════
# CONFIGURATION & CONSTANTS
# ══════════════════════════════════════════════════════════════════
CSV_FILE = "dataset.csv"
MY_BUDGET = 50000.0  

# ══════════════════════════════════════════════════════════════════
# 1. UTILITIES & DATA PERSISTENCE
# ══════════════════════════════════════════════════════════════════

def reset_data():
    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)
        print("🧹 Clean Slate: dataset.csv has been deleted.")

def fetch_realtime_cloud_data():
    """
    Simulates real-time cloud pulling with incremental dates.
    """
    last_day = 0
    if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
        try:
            with open(CSV_FILE, 'r') as f:
                rows = list(csv.DictReader(f))
                if rows:
                    last_day = int(rows[-1]['day'])
        except Exception:
            last_day = 0

    new_day_num = last_day + 1
    
    # --- DATE CALCULATION LOGIC ---
    # Starts from the 1st of the current month and adds 'last_day' days
    start_of_month = datetime.now().replace(day=1)
    current_date = start_of_month + timedelta(days=last_day)
    date_str = current_date.strftime("%Y-%m-%d")
    # ------------------------------

    is_spike = random.random() < 0.2 
    if is_spike:
        amount = random.uniform(3500, 6000)
        service = "Lambda (Anomaly Spike)"
    else:
        amount = random.uniform(1100, 1400)
        service = random.choice(["EC2", "S3", "RDS"])

    return [{
        "day": new_day_num,
        "date": date_str,
        "amount": round(amount, 2),
        "service": service
    }]

def append_to_csv(data_list):
    file_exists = os.path.isfile(CSV_FILE) and os.path.getsize(CSV_FILE) > 0
    keys = ["day", "date", "amount", "service"]
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        if not file_exists:
            writer.writeheader()
        writer.writerows(data_list)

# ══════════════════════════════════════════════════════════════════
# 2. AGENTIC MATH
# ══════════════════════════════════════════════════════════════════

def perform_analysis(budget):
    amounts = []
    if not os.path.exists(CSV_FILE): return None

    with open(CSV_FILE, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            amounts.append(float(row['amount']))

    if not amounts: return None

    # We use set(dates) to count unique days if there are multiple entries per day
    days_recorded = len(amounts) 
    total_spent = sum(amounts)
    avg_daily = total_spent / days_recorded
    
    now = datetime.now()
    total_days_in_month = calendar.monthrange(now.year, now.month)[1]
    days_remaining = max(0, total_days_in_month - days_recorded)
    
    forecast = total_spent + (avg_daily * days_remaining)
    over_amt = round(forecast - budget, 2)
    over_pct = round((over_amt / budget) * 100, 2) if budget > 0 else 0
    required_cut = round(over_amt / days_remaining, 2) if over_amt > 0 and days_remaining > 0 else 0

    return {
        "total_spent": round(total_spent, 2),
        "forecast": round(forecast, 2),
        "over_amt": max(0, over_amt),
        "over_pct": max(0, over_pct),
        "required_daily_cut": required_cut,
        "days_remaining": days_remaining,
        "history_count": days_recorded,
        "last_day_spend": amounts[-1],
        "is_breach": over_amt > 0
    }

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == "reset":
        reset_data()
    else:
        # For testing: run this multiple times to see dates increment!
        new_data = fetch_realtime_cloud_data()
        append_to_csv(new_data)
        m = perform_analysis(MY_BUDGET)
        print(f"Logged Date: {new_data[0]['date']} | Forecast: ₹{m['forecast']}")
