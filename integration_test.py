import logic      # Member 1's Math/Calendar Logic
import recommend  # Your (Member 2) Ranked Recommendation Logic

# 1. Simulate the User Input (Budget in ₹)
# Adjusted to ₹50,000 to match our new logic.py scales
USER_BUDGET = 50000.0 

# 2. Get Analysis from Member 1 (The "Observation" Phase)
analysis = logic.get_full_analysis(USER_BUDGET)
metrics = analysis['metrics']

# 3. Get Recommendations from Member 2 (The "Decision" Phase)
recommendation = recommend.get_recommendation(metrics['over_pct'])

# 4. Display the "Agentic" Result
print(f"\n" + "="*60)
print(f"--- 🤖 AGENTIC WATCHDOG REPORT ---")
print(f"="*60)
print(f"Current Forecast: ₹{metrics['forecast']:,}")
print(f"Overspend Detected: {metrics['over_pct']}%")
print(f"Summary: {recommendation['message']}")

# 5. Show the Systematic Plan & Green Impact
if recommendation['alert']:
    # Run the simulation to get GreenOps data
    sim_result = recommend.simulate_action(recommendation, metrics['forecast'], USER_BUDGET)
    
    print("\n--- SYSTEMATIC FIX PLAN ---")
    for step in recommendation['plan']:
        # Check if plan has eco_impact tag from our new recommend.py
        eco_tag = f" [{step.get('eco_impact', '')}]" if step.get('eco_impact') else ""
        print(f"RANK {step['rank']}: {step['action']} (Priority: {step['priority']}){eco_tag}")
        print(f"    Details: {step['detail']}")
    
    print("\n--- 🌱 GREENOPS IMPACT (ESTIMATED) ---")
    print(f"CO2 Avoided: {sim_result['co2_saved_kg']} kg")
    print(f"Planet Impact: Equivalent to planting {sim_result['trees_equiv']} trees today!")

    # 6. Show the AGENT REASONING (The "Logic" Phase)
    # Passing sim_result now to include the tree-logic in the reasoning
    rationale = recommend.get_agent_decision_logic(metrics, recommendation, sim_result)
    print(f"\n" + "-"*60)
    print(f"🤖 AGENT RATIONALE:")
    print(f"{rationale}")
    print("-"*60)
else:
    print("\n✅ System status optimal. Budget and Carbon Footprint are healthy.")

print(f"="*60 + "\n")
