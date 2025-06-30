from langgraph.graph import StateGraph
from app.state_types import AgentState
from app.planner import generate_agent_plan
from app.checkpointer import get_checkpointer
from app.graph_definition import build_graph

def build_and_run_graph(prompt: str, history: list[str], thread_id: str) -> dict:
    # Step 1: Plan agents
    agent_plan, meta, results = generate_agent_plan(prompt, history)

    # Step 2: Build initial state
    state = {
        "prompt": prompt,
        "history": history,
        "agent_plan": agent_plan,
        "current_step": 0,
        "logs": [],
        "responses": [],
        "executed_agents": [],
        "meta": meta,
        "results": results
    }

    # Step 3: Setup graph
    builder = StateGraph(AgentState)
    build_graph(builder)
    graph = builder.compile()
    checkpointer = get_checkpointer()

    # Step 4: Run execution
    result = graph.invoke(state, config={"thread_id": thread_id, "checkpointer": checkpointer})
    return result
