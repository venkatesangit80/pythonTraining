# 🧠 Normal Chat Mode with LangChain + MCP + Guardrails

This module enables an intelligent, secure, LLM-driven chat endpoint using LangChain, MCP-style agent execution, and Python-based prompt guardrails.

---

## 📂 File: `normal_chat.py`

This FastAPI route handles:

1. ✅ Prompt validation (guardrails)
2. ✅ Agent selection (intent extraction)
3. ✅ Restricted toolset execution (MCP)
4. ✅ LangChain execution
5. ✅ Structured response to UI

---

## ✨ Endpoint Summary

**POST** `/normal-chat`

**Input JSON:**
```json
{
  "message": "Get me the health of APP1"
}
```

**Output JSON:**
```json
{
  "answer": "Your application has 24 servers...",
  "agents_used": ["server_health", "capacity_forecast"]
}
```

---

## 🧱 Dependencies

### `prompt_guards.py`
```python
def validate_prompt(prompt: str) -> str:
    if len(prompt) > 512:
        raise ValueError("Prompt too long")
    if any(bad in prompt.lower() for bad in ["drop database", "delete all"]):
        raise ValueError("Unsafe prompt")
    return prompt
```

---

### `agent_selector.py`
```python
def extract_agents(prompt: str) -> list:
    keywords = {
        "health": "server_health",
        "overutilized": "overutilized_check",
        "forecast": "capacity_forecast"
    }
    return [val for key, val in keywords.items() if key in prompt.lower()]
```

---

### `agent_registry.py`
```python
from app.mcp_agents.server_health import ServerHealthTool
from app.mcp_agents.capacity_forecast import ForecastTool

ALLOWED_AGENTS = {
    "server_health": ServerHealthTool(),
    "capacity_forecast": ForecastTool()
}
```

---

### `llm_executor.py`
```python
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI

def run_with_agents(prompt: str, tools: list) -> str:
    llm = ChatOpenAI(model_name="gpt-4", temperature=0.0)
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent_type="openai-functions",
        verbose=True
    )
    return agent.run(prompt)
```

---

## ✅ Example Usage

```bash
curl -X POST http://localhost:8000/normal-chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Check forecast and current health"}'
```

---

## 📌 Best Practices

- Wrap LangChain calls with try/except for observability.
- Add logging inside `extract_agents()` to monitor agent match accuracy.
- Dynamically load available tools from a registry if needed.

---

## 🔐 Security Considerations

- Prompt guardrails reject dangerous or vague inputs.
- Only registered agents are allowed for execution.
- Responses are filtered and structured for safe UI display.

---

## 👨‍💻 Maintainer

Built by Venkatesan Subramanian — AI + Infra Automation Enthusiast.
