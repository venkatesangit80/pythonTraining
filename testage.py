# core/mcp_chatbot_agent.py
# Unified LangChain agent combining multiple tools with memory

import os
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, initialize_agent
from langchain.memory import ConversationBufferMemory

# === Load tools from local agent modules ===
from agents.agentic_flow import agentic_flow_summary
from agents.rca_chat import get_incident_context, summarize_rca
from agents.kb_search_agent import kb_agent
from agents.contextual_recommendation import recommendation_agent

# === Wrapper functions to conform to Tool signature ===

def rca_tool_func(incident_id: str) -> str:
    incident, telemetry_df, _ = get_incident_context(incident_id)
    if incident is None:
        return "❌ RCAAgent: Incident not found."
    return summarize_rca(incident, telemetry_df)

def recommendation_tool_func(tag: str) -> str:
    return recommendation_agent(tag)

def telemetry_tool_func(_: str) -> str:
    return agentic_flow_summary()

def kb_tool_func(query: str) -> str:
    return kb_agent(query)

# === Define LangChain Tools ===
tools = [
    Tool(
        name="RCAAgent",
        func=rca_tool_func,
        description="Summarizes the root cause of a given incident. Input should be an incident ID (e.g., 'inc032')."
    ),
    Tool(
        name="TelemetryAgent",
        func=telemetry_tool_func,
        description="Detects recent anomalies in telemetry data. Input can be any placeholder text."
    ),
    Tool(
        name="KBAgent",
        func=kb_tool_func,
        description="Finds relevant knowledge base articles. Input should be a natural language query."
    ),
    Tool(
        name="RecommendationAgent",
        func=recommendation_tool_func,
        description="Provides contextual recommendations based on similarity tags (e.g., 'HighCPU', 'MemoryLeak')."
    ),
]

# === Initialize LangChain Agent ===

def get_mcp_chat_agent():
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent="chat-zero-shot-react-description",
        memory=memory,
        verbose=True,
        handle_parsing_errors=True
    )

    return agent
