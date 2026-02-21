# integration_test.py - Master Orchestrator (Agentic Edition)
# ROLE: Bridge between Memory (logic.py), Strategy (recommend.py), and Reasoning (brain.py).

import warnings
import os
import logic      # Member 1's CSV & Math Engine
import recommend  # Member 2's Ranked Recommendations
import brain      # Member 3's Gemini Reasoning Engine

# ══════════════════════════════════════════════════════════════════
# 0. DEMO PREP
# ══════════════════════════════════════════════════════════════════
warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════════
# 1. SETUP PARAMETERS
# ══════════════════════════════════════════════════════════════════
USER_BUDGET = 50000.0 

def run_workflow():
    # ══════════════════════════════════════════════════════════════════
    # 2. THE OBSERVATION PHASE (Data Memory)
    # ══════════════════════════════════════════════════════════════════
    # Generate multiple logs per run for a richer dataset
    import random
    for _ in range(random.randint(2, 4)):
        new_data = logic.fetch_realtime_cloud_data()
        logic.append_to_csv(new_data)
    
    m = logic.perform_analysis(USER_BUDGET)
    
    if not m:
        print("❌ Error: Memory retrieval failed.")
        return

    print(f"\n" + "═"*60)
    print(f"🛡️ WATCHDOG AGENT: SYSTEMATIC AUDIT")
    print(f"═"*60)
    print(f"RECORDS LOGGED   : {m['history_count']} service entries.")
    print(f"MONTHLY FORECAST : ₹{m['forecast']:,}")
    print(f"PROJECTED GAP    : ₹{m['over_amt']:,}")

    # ══════════════════════════════════════════════════════════════════
    # 3. THE DECISION PHASE (Strategy Engine)
    # ══════════════════════════════════════════════════════════════════
    recommendation = recommend.get_recommendation(m['over_pct'])
    
    print(f"\n[DECISION STRATEGY]")
    print(f"SEVERITY: {recommendation.get('severity', 'SAFE')}")
    print(f"MESSAGE : {recommendation['message']}")

    # ══════════════════════════════════════════════════════════════════
    # 4. THE REASONING PHASE (Gemini AI)
    # ══════════════════════════════════════════════════════════════════
    # Passing raw metrics and recommendation to the AI for a rationale
    print(f"\n[AGENT Recommendation Rationale]")
    ai_thought = brain.get_agent_reasoning(m, recommendation)
    print(f"💬 Watchdog: \"{ai_thought}\"")

    # ══════════════════════════════════════════════════════════════════
    # 5. EXECUTION & IMPACT PHASE
    # ══════════════════════════════════════════════════════════════════
    if recommendation['alert']:
        sim = recommend.simulate_action(recommendation, m['forecast'], USER_BUDGET)
        
        print("\n[RANKED OPTIMIZATION PLAN]")
        for step in recommendation['plan']:
            eco_tag = f" [{step.get('eco_impact', '')}]" if step.get('eco_impact') else ""
            print(f"• {step['action']} (Priority: {step['priority']}){eco_tag}")
        
        print("\n[🌱 GREENOPS SUSTAINABILITY REPORT]")
        print(f"CO2 Avoided: {sim['co2_saved_kg']} kg | Impact: {sim['trees_equiv']} trees.")
        
        print(f"\n[FINANCIAL RECOVERY]")
        print(f"✅ Executing: {sim['action_taken']}")
        print(f"📉 New Forecast: ₹{sim['new_forecast']:,}")
        
        if sim['now_within_budget']:
            print(f"\n🎯 RESULT: Budget target restored.")
    else:
        print(f"\n✅ STATUS: Operating within healthy efficiency parameters.")

    print(f"\n" + "═"*60)
    print(f"AUDIT COMPLETE")
    print(f"═"*60 + "\n")

if __name__ == "__main__":
    run_workflow()
