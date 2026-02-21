"""
Member 1 — Calculation Engineer (Abhinav)
HACKATHON ROLE: Logic, Math, and Agentic Goal-Gap Analysis
CURRENCY: Indian Rupees (₹)
"""

import calendar
import random
from datetime import datetime, timedelta

# ══════════════════════════════════════════════════════════════════
# 1. REAL-TIME DATA SOURCE (DYNAMIC MOCK API)
# ══════════════════════════════════════════════════════════════════

def fetch_realtime_cloud_data():
    """
    Simulates a Real-Time API response from a Cloud Provider.
    Now uses Rupees (₹) and dynamic spikes for demo variability.
    """
    base_date = datetime.now() - timedelta(days=10)
    data = []
    
    # Randomizing the spike to ensure every demo run is unique
    # Normal spend: ₹1,100 - ₹1,400 | Spike: ₹3,500 - ₹5,500
    spike_intensity = random.uniform(3500, 5500) 
    
    for i in range(1, 11):
        # Days 1-7: Stable | Days 8-10: Anomaly detected
        if i < 8:
            amount = random.uniform(1100, 1400)
            service = random.choice(["EC2", "S3", "RDS"])
        else:
            amount = spike_intensity + random.uniform(-300, 300)
            service = "Lambda"
            
        data.append({
            "day": i,
            "date": (base_date + timedelta(days=i)).strftime("%Y-%m-%d"),
            "amount": round(amount, 2),
            "service": service
        })
    return data

# ══════════════════════════════════════════════════════════════════
# 2. CORE MATH & CALENDAR-AWARE FORECASTING
# ══════════════════════════════════════════════════════════════════

def get_month_stats():
    """Detects total days in current month to ensure 28/30/31 day accuracy."""
    now = datetime.now()
    total_days = calendar.monthrange(now.year, now.month)[1]
    return now.day, total_days

def calculate_daily_metrics(daily_amounts):
    """Deep analysis of spend so far."""
    total_so_far = sum(daily_amounts)
    avg_daily = total_so_far / len(daily_amounts) if daily_amounts else 0
    return round(total_so_far, 2), round(avg_daily, 2)

def predict_monthly_spend(daily_amounts):
    """
    AGENTIC PREDICTION: Linear extrapolation to the end of the month.
    Formula: Total Spent + (Average Daily Burn * Days Remaining)
    """
    _, total_days = get_month_stats()
    total_so_far, avg_daily = calculate_daily_metrics(daily_amounts)
    days_remaining = total_days - len(daily_amounts)
    
    forecast = total_so_far + (avg_daily * max(0, days_remaining))
    return round(forecast, 2), days_remaining

# ══════════════════════════════════════════════════════════════════
# 3. AGENTIC GOAL-GAP ANALYSIS
# ══════════════════════════════════════════════════════════════════

def calculate_agentic_gap(forecast, budget, days_remaining):
    """
    Calculates exactly what the AI needs to DO to fix the budget breach.
    This provides the 'Goal' for Member 2's Recommendation Engine.
    """
    over_amt = round(forecast - budget, 2)
    
    # Required Daily Reduction: How much to cut starting TODAY to hit ₹0 gap.
    if over_amt > 0 and days_remaining > 0:
        required_cut = round(over_amt / days_remaining, 2)
    else:
        required_cut = 0.0
        
    return over_amt, required_cut

# ══════════════════════════════════════════════════════════════════
# 4. MASTER INTEGRATION FUNCTION
# ══════════════════════════════════════════════════════════════════

def get_full_analysis(budget):
    """
    Main entry point for Member 4 (Integrator).
    Returns a complete package of data, metrics, and reasoning.
    """
    raw_data = fetch_realtime_cloud_data()
    amounts = [d['amount'] for d in raw_data]
    
    total_spent, avg_daily = calculate_daily_metrics(amounts)
    forecast, days_rem = predict_monthly_spend(amounts)
    over_amt, required_cut = calculate_agentic_gap(forecast, budget, days_rem)
    
    # Growth percentage for Member 2's severity logic
    over_pct = round((over_amt / budget) * 100, 2) if budget > 0 else 0

    return {
        "raw_data": raw_data,
        "metrics": {
            "total_spent": total_spent,
            "avg_daily": avg_daily,
            "forecast": forecast,
            "over_amt": over_amt,
            "over_pct": over_pct,
            "required_daily_cut": required_cut,
            "days_remaining": days_rem
        }
    }

# ══════════════════════════════════════════════════════════════════
# 5. TEST RUNNER (LOCAL CONSOLE DEMO)
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Test Budget set to ₹50,000 for realistic cloud testing
    MY_BUDGET = 50000.0 
    
    print(f"--- 🤖 AGENTIC ANALYSIS START (Budget: ₹{MY_BUDGET}) ---")
    
    result = get_full_analysis(MY_BUDGET)
    m = result['metrics']
    
    print(f"Status: Fetching real-time cloud streams... Done.")
    print(f"Total Spent (Days 1-10): ₹{m['total_spent']}")
    print(f"Projected Month-End (Day {m['days_remaining'] + 10}): ₹{m['forecast']}")
    
    if m['over_amt'] > 0:
        print(f"\n🚨 ALERT: Breach Predicted!")
        print(f"Projected Overrun: ₹{m['over_amt']} ({m['over_pct']}%)")
        print(f"Agentic Goal: Must reduce spend by ₹{m['required_daily_cut']} per day.")
    else:
        print("\n✅ Status: Spend projection is healthy and within limits.")
