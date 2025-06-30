import google.generativeai as genai
import os
import json
from typing import List, Dict, Tuple

# Initialize Gemini model
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Descriptions used in prompt planning
AGENT_DESCRIPTIONS = {
    "health": "Check over and under utilized servers.",
    "forecast": "Predict resource usage trends.",
    "recommendation": "Recommend actions based on current and future health.",
    "promql": "Generate Prometheus query based on system intent."
}

def generate_agent_plan(user_prompt: str, history: List[Dict]) -> Tuple[List[Dict], Dict[str, List[str]], Dict[str, str]]:
    """
    Use Gemini to generate a structured plan of agents to run based on prompt and conversation history.
    Returns the plan, meta mapping, and initial empty results dict.
    """
    history_text = "\n".join([f"{m['role']}: {m['content']}" for m in history])

    system_prompt = f"""
You are an agent planner.

Your task is to determine the next set of agents to execute based on the full conversation context — not just the latest user input.

Review any agent responses or summaries.

The available agents and their purposes are:
{json.dumps(AGENT_DESCRIPTIONS, indent=2)}

Return a Python dictionary with the following keys:

1. "plan" – a list of agent contracts. Each contract must include:
   - agent: the agent name (e.g., "health")
   - description: override the default (if needed) based on the user query
   - input_value: either a static string (e.g., "APP1") or a previous agent name (e.g., "health")
   - input_instruction: describe what the agent should process
   - output_instruction: describe the expected result
   - action_type: "independent" or "dependent"

2. "meta" – a dictionary mapping each independent agent to the dependent agents that require its output.
   Example:
   {{
     "health": ["forecast", "recommendation"]
   }}

3. "results" – a dictionary initialized with empty strings for each independent agent.
   Example:
   {{
     "health": ""
   }}

You may override default agent descriptions to match the user's request more closely. If no override is needed, use the default.

❗ If the user query is not related to monitoring or agent execution, return:
{{ "plan": [], "meta": {{}}, "results": {{}} }}

Respond ONLY with a valid Python dictionary. Do not include explanations or comments.

Example:
{{
  "plan": [
    {{
      "agent": "health",
      "description": "Check CPU/memory usage for APP1",
      "input_value": "APP1",
      "input_instruction": "Inspect server metrics",
      "output_instruction": "Return overloaded servers",
      "action_type": "independent"
    }},
    {{
      "agent": "forecast",
      "description": "Predict future usage based on current load",
      "input_value": "health",
      "input_instruction": "Use health output",
      "output_instruction": "Forecast risk over next 30 mins",
      "action_type": "dependent"
    }}
  ],
  "meta": {{
    "health": ["forecast"]
  }},
  "results": {{
    "health": ""
  }}
}}
"""

    prompt = f"{system_prompt}\n\nConversation so far:\n{history_text}\n\nUser query: \"{user_prompt}\"\n"
    response = model.generate_content(prompt)
    try:
        parsed = json.loads(response.text)
        return parsed["plan"], parsed.get("meta", {}), parsed.get("results", {})
    except Exception as e:
        raise ValueError(f"Failed to parse agent planning output: {e}\nRaw response: {response.text}")
