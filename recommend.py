# recommend.py - Managed by Member 2
# VERSION: Agentic GreenOps Systematic Watchdog (Rupees Edition)
import os

# ══════════════════════════════════════════════════════════════════
# 1. API CONFIGURATION (Expert Requirement)
# ══════════════════════════════════════════════════════════════════
FINOPS_API_KEY = os.getenv("FINOPS_WATCHDOG_KEY", "hc_demo_2026_agent_auth")

# ══════════════════════════════════════════════════════════════════
# 2. SUSTAINABILITY CALCULATOR (GreenOps Logic)
# ══════════════════════════════════════════════════════════════════

def calculate_environmental_impact(rupees_saved):
    """
    Translates financial savings into planet-saving metrics.
    Assumptions for Indian Data Centers:
    - Average cost per kWh in India: ₹8.00
    - Carbon Intensity of Indian Grid: ~0.8kg CO2 per kWh
    - 1 Tree absorbs ~0.06kg CO2 per day (21kg per year)
    """
    # Estimate energy saved in kWh
    kwh_saved = rupees_saved / 8.0
    kg_co2_saved = round(kwh_saved * 0.8, 2)
    
    # Tree equivalent: How many trees would it take to absorb this in a day?
    trees_equivalent = round(kg_co2_saved / 0.06, 1)
    
    return {
        "co2_saved_kg": kg_co2_saved,
        "trees_planted_equiv": trees_equivalent
    }

# ══════════════════════════════════════════════════════════════════
# 3. RECOMMENDATION ENGINE
# ══════════════════════════════════════════════════════════════════

def get_recommendation(overspend_percent):
    """
    Analyzes overspend and returns a ranked, systematic plan.
    Now includes GreenOps impact tags for each action.
    """
    if overspend_percent <= 0:
        return {
            "alert": False,
            "severity": "SAFE",
            "message": "Spending is within budget. No action needed.",
            "plan": [],
            "total_potential_savings_pct": 0
        }

    plan = []

    # RANK 1: CRITICAL ACTION
    if overspend_percent >= 25:
        plan.append({
            "rank": 1,
            "priority": "HIGH",
            "action": "Terminate Idle Systems",
            "detail": "Immediately shut down unused GPU instances. Significant energy waste detected.",
            "savings_pct": 35,
            "eco_impact": "High Carbon Reduction"
        })
    
    # RANK 2: OPTIMIZATION ACTION
    if overspend_percent >= 10:
        plan.append({
            "rank": 2,
            "priority": "MEDIUM",
            "action": "Instance Right-Sizing",
            "detail": "Scale down oversized instances (e.g., m5.large to t3.medium). Reduces heat generation.",
            "savings_pct": 20,
            "eco_impact": "Energy Efficiency"
        })

    # RANK 3: MINOR CLEANUP
    plan.append({
        "rank": 3,
        "priority": "LOW",
        "action": "Resource Scheduling",
        "detail": "Automate shutdown of Dev/Test environments during non-business hours.",
        "savings_pct": 8,
        "eco_impact": "Vampire Power Elimination"
    })

    if overspend_percent >= 25:
        summary_msg = f"CRITICAL: {overspend_percent}% Overspend. Immediate shutdown required for budget & planet."
    elif overspend_percent >= 10:
        summary_msg = f"WARNING: {overspend_percent}% Overspend. Optimization needed."
    else:
        summary_msg = f"NOTICE: {overspend_percent}% Overspend. Minor cleanup suggested."

    return {
        "alert": True,
        "severity": "CRITICAL" if overspend_percent >= 25 else "WARNING",
        "message": summary_msg,
        "overspend_level": overspend_percent,
        "plan": plan,
        "total_potential_savings_pct": sum(item['savings_pct'] for item in plan)
    }

# ══════════════════════════════════════════════════════════════════
# 4. ACTION SIMULATOR
# ══════════════════════════════════════════════════════════════════

def simulate_action(recommendation, forecast, budget):
    """
    Simulates the result of applying the HIGHEST RANKED action.
    Calculates both ₹ savings and Carbon Footprint reduction.
    """
    if not recommendation["alert"] or not recommendation["plan"]:
        return {
            "action_taken": "None",
            "amount_saved": 0,
            "new_forecast": forecast,
            "now_within_budget": forecast <= budget,
            "message": "No action needed."
        }

    top_action = recommendation["plan"][0]
    savings_multiplier = top_action["savings_pct"] / 100
    saved_amount = round(forecast * savings_multiplier, 2)
    new_forecast = round(forecast - saved_amount, 2)

    # GreenOps Calculation
    green_impact = calculate_environmental_impact(saved_amount)

    return {
        "action_taken": top_action["action"],
        "priority": top_action["priority"],
        "amount_saved": saved_amount,
        "new_forecast": new_forecast,
        "co2_saved_kg": green_impact["co2_saved_kg"],
        "trees_equiv": green_impact["trees_planted_equiv"],
        "now_within_budget": new_forecast <= budget,
        "message": f"Agent applied {top_action['action']}. Saved ₹{saved_amount} and {green_impact['co2_saved_kg']}kg CO2."
    }

# ══════════════════════════════════════════════════════════════════
# 5. AGENT REASONING TOOL
# ══════════════════════════════════════════════════════════════════

def get_agent_decision_logic(metrics, recommendation, sim_result):
    """
    Explains the 'Why' behind the plan.
    Connects financial goals (₹) to environmental stewardship (Trees).
    """
    if not recommendation["alert"]:
        return "Budget goals are currently met. Carbon footprint is within optimized limits."
    
    daily_cut_needed = metrics.get('required_daily_cut', 0)
    top_action = recommendation['plan'][0]['action']
    
    return (
        f"Goal Alignment: To offset the projection, a daily reduction of ₹{daily_cut_needed} is required. "
        f"The Agent has prioritized '{top_action}' to save ₹{sim_result['amount_saved']}. "
        f"🌱 Environmental Impact: This action avoids {sim_result['co2_saved_kg']}kg of CO2 emissions, "
        f"equivalent to planting {sim_result['trees_equiv']} trees today."
    )
