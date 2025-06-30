from typing import TypedDict, List, Dict, Optional

class AgentState(TypedDict):
    prompt: str
    history: List[Dict[str, str]]
    agent_plan: List[Dict]  # list of agent instructions
    current_step: int
    logs: List[str]
    response: Optional[str]
    responses: List[str]
    executed_agents: List[str]
    meta: Dict[str, List[str]]  # independent agent -> dependent agents
    results: Dict[str, str]     # agent name -> output string
