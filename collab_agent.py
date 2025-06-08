#export OPENAI_API_KEY=sk-xxxxx
pip install openai
python collaboration_agent_llm.py

import os
from openai import OpenAI
from typing import List, Dict

# === Simulated Agent Classes ===
class OverutilizedAgent:
    def run(self, app_id: str) -> List[Dict]:
        return [
            {"server": "srv1", "over_util_reason": "CPU"},
            {"server": "srv2", "over_util_reason": "memory"}
        ]


class UnderutilizedAgent:
    def run(self, app_id: str) -> List[Dict]:
        return [
            {"server": "srv4", "under_util_reason": "Idle"}
        ]


class CurrentHeadroomAgent:
    def run(self, app_id: str) -> Dict:
        return {"headroom_percent": 35}


class FutureHeadroomAgent:
    def run(self, app_id: str) -> Dict:
        return {"forecast": "Headroom may drop below 15% in 5 days"}


# === Collaboration Agent Using LLM for Summary ===
class CollaborationAgentWithLLM:
    def __init__(self, api_key: str):
        self.overutil_agent = OverutilizedAgent()
        self.underutil_agent = UnderutilizedAgent()
        self.current_headroom_agent = CurrentHeadroomAgent()
        self.future_headroom_agent = FutureHeadroomAgent()
        self.client = OpenAI(api_key=api_key)

    def run(self, app_id: str):
        overutil = self.overutil_agent.run(app_id)
        underutil = self.underutil_agent.run(app_id)
        current_headroom = self.current_headroom_agent.run(app_id)
        future_headroom = self.future_headroom_agent.run(app_id)

        # Build breakdown
        breakdown = f"Health Report for Application: {app_id}\n\n"
        breakdown += "1. Overutilized Servers:\n"
        if overutil:
            for item in overutil:
                breakdown += f"   - {item['server']} is overutilized due to {item['over_util_reason']}\n"
        else:
            breakdown += "   - None\n"

        breakdown += "\n2. Underutilized Servers:\n"
        if underutil:
            for item in underutil:
                breakdown += f"   - {item['server']} is underutilized due to {item['under_util_reason']}\n"
        else:
            breakdown += "   - None\n"

        breakdown += f"\n3. Current Headroom:\n"
        breakdown += f"   - Available headroom is {current_headroom['headroom_percent']}%\n"

        breakdown += f"\n4. Future Headroom Forecast:\n"
        breakdown += f"   - {future_headroom['forecast']}\n"

        # Prompt LLM to generate summary
        prompt = f"""
You are a system health assistant. Read the following infrastructure status breakdown and write a clear, business-friendly summary with recommendations:

{breakdown}

Summary:
"""
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        summary = response.choices[0].message.content.strip()

        return {
            "app_id": app_id,
            "summary": summary,
            "breakdown": breakdown.strip()
        }


# === Execution ===
if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        app_id = "APP1"
        collab_agent = CollaborationAgentWithLLM(api_key=api_key)
        result = collab_agent.run(app_id)

        print("\n🧠 LLM-Generated Summary:\n", result["summary"])
        print("\n📊 Breakdown:\n", result["breakdown"])
    else:
        print("❌ OPENAI_API_KEY not found in environment variables.")
