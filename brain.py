import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") 

genai.configure(api_key=api_key)

def get_agent_reasoning(metrics, recommendation):
    """
    The 'Reasoning Engine': Converts raw budget numbers into 
    cause-oriented, strategic narratives using Gemini.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    plan = recommendation.get('plan', [])
    if not plan:
        return ("I have analyzed the current cloud infrastructure. All systems are "
                "operating within their allocated financial and thermal envelopes; "
                "no autonomous intervention is required at this time.")

    over_amt = metrics.get('over_amt', 0)
    action = plan[0].get('action', 'Optimization')
    
    # NEW MISSION-DRIVEN PROMPT
    prompt = f"""
    You are 'Watchdog', an autonomous FinOps AI Agent dedicated to sustainable financial stewardship.
    The current project is facing a projected budget breach of ₹{over_amt}. 
    Your selected intervention is: {action}.

    Task:
    Write a professional, cause-oriented paragraph explaining your rationale. 
    Focus on the 'Double Bottom Line': how this action eliminates fiscal waste while 
    simultaneously reducing the project's digital carbon footprint. 
    Use a tone that is authoritative yet environmentally conscious.
    Start with: 'As your project’s autonomous guardian, I have identified a fiscal anomaly...'
    """

    try:
        # Generating content with safety settings to ensure smooth delivery
        response = model.generate_content(
            prompt,
            safety_settings=[
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
        )
        return response.text.strip()

    except Exception as e:
        # DYNAMIC FALLBACK: Still uses real data even if the API fails
        return (f"As your project's autonomous guardian, I have identified a fiscal anomaly "
                f"of ₹{over_amt}. I am initiating {action} to optimize resource "
                f"efficiency, effectively reducing both operational overhead and our "
                f"environmental impact to restore sustainable project health.")
