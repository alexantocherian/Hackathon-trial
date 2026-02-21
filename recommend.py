# recommend.py - Managed by Member 2
# VERSION: Agentic GreenOps Watchdog (CSV-Logic Aligned)
import os

# ══════════════════════════════════════════════════════════════════
# 1. SUSTAINABILITY CALCULATOR (GreenOps Logic)
# ══════════════════════════════════════════════════════════════════

def calculate_green_impact(rupees_saved):
    """
    Scientific conversion: Money -> Energy -> Carbon -> Trees.
    """
    # 1. Indian Grid intensity: ₹10 approx 1kWh, 1kWh approx 0.7kg CO2
    kg_co2_saved = round((rupees_saved / 10) * 0.7, 2)
    
    # 2. Scientific Offset: One mature tree absorbs ~21kg of CO2 PER YEAR.
    trees_equivalent = round(kg_co2_saved / 21, 2) 
    
    return {
        "co2_saved_kg": kg_co2_saved, 
        "trees_planted_equiv": trees_equivalent
    }

# ══════════════════════════════════════════════════════════════════
# 2. RECOMMENDATION ENGINE
# ══════════════════════════════════════════════════════════════════

def get_recommendation(overspend_percent):
    """
    Analyzes the 'over_pct' from Abhinav's logic.py.
    """
    if overspend_percent <= 0:
        return {
            "alert": False,
            "severity": "SAFE",
            "message": "Spending is within budget. No action needed.",
            "plan": []
        }

    plan = []

    # RANK 1: CRITICAL ACTION
    if overspend_percent >= 25:
        plan.append({
            "rank": 1,
            "priority": "HIGH",
            "action": "Terminate Idle Systems",
            "detail": "Immediate shutdown of unused Lambda/GPU anomalies.",
            "savings_pct": 35,
            "eco_impact": "High Carbon Reduction"
        })
    
    # RANK 2: OPTIMIZATION ACTION
    if overspend_percent >= 10:
        plan.append({
            "rank": 2,
            "priority": "MEDIUM",
            "action": "Instance Right-Sizing",
            "detail": "Scale down oversized EC2/RDS instances.",
            "savings_pct": 20,
            "eco_impact": "Energy Efficiency"
        })

    # RANK 3: MINOR CLEANUP
    plan.append({
        "rank": 3,
        "priority": "LOW",
        "action": "Resource Scheduling",
        "detail": "Off-hours shutdown for Dev/Test environments.",
        "savings_pct": 8,
        "eco_impact": "Vampire Power Elimination"
    })

    # Severity logic
    if overspend_percent >= 25:
        summary_msg = f"CRITICAL: {overspend_percent}% Overspend. High anomaly detected."
    elif overspend_percent >= 10:
        summary_msg = f"WARNING: {overspend_percent}% Overspend. Trend is exceeding limits."
    else:
        summary_msg = f"NOTICE: {overspend_percent}% Overspend. Minor optimization recommended."

    return {
        "alert": True,
        "severity": "CRITICAL" if overspend_percent >= 25 else "WARNING",
        "message": summary_msg,
        "plan": plan
    }

# ══════════════════════════════════════════════════════════════════
# 3. ACTION SIMULATOR
# ══════════════════════════════════════════════════════════════════

def simulate_action(recommendation, forecast, budget):
    """
    Simulates the result of applying the HIGHEST RANKED action.
    """
    if not recommendation["alert"] or not recommendation["plan"]:
        return {
            "action_taken": "None",
            "amount_saved": 0,
            "new_forecast": forecast,
            "now_within_budget": forecast <= budget,
            "co2_saved_kg": 0,
            "trees_equiv": 0
        }

    # Pick the best fix based on the ranking
    top_action = recommendation["plan"][0]
    savings_multiplier = top_action["savings_pct"] / 100
    saved_amount = round(forecast * savings_multiplier, 2)
    new_forecast = round(forecast - saved_amount, 2)

    # FIXED: Calling the correct impact function
    green_impact = calculate_green_impact(saved_amount)

    return {
        "action_taken": top_action["action"],
        "amount_saved": saved_amount,
        "new_forecast": new_forecast,
        "co2_saved_kg": green_impact["co2_saved_kg"],
        "trees_equiv": green_impact["trees_planted_equiv"],
        "now_within_budget": new_forecast <= budget
    }

# ══════════════════════════════════════════════════════════════════
# 4. AGENT REASONING TOOL
# ══════════════════════════════════════════════════════════════════

def get_agent_decision_logic(metrics, recommendation, sim_result):
    """
    Explains the reasoning. Feeds the Agent Rationale section of the UI.
    """
    if not recommendation["alert"]:
        return "Budget goals are met. I am maintaining the current resource efficiency."
    
    daily_cut_needed = metrics.get('required_daily_cut', 0)
    top_action = recommendation['plan'][0]['action']
    
    return (
        f"Goal Alignment: To offset the projection, a daily reduction of ₹{daily_cut_needed} is required. "
        f"The Agent has prioritized '{top_action}' to save ₹{sim_result['amount_saved']}. "
        f"🌱 Impact: This action avoids {sim_result['co2_saved_kg']}kg of CO2 emissions, "
        f"equivalent to the work of {sim_result['trees_equiv']} trees."
    )
