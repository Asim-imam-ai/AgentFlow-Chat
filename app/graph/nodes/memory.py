import logging

from app.graph.state import AgentState
from app.tools.memory import load_memory

logger = logging.getLogger("agentflow.graph.nodes.memory")


def memory_node(state: AgentState) -> dict:
    """
    Node that loads persistent user memory facts and saves them to the agent state.
    """
    logger.info("Executing memory node: loading facts from storage")
    memory = load_memory()

    if not memory:
        return {"memory_context": "No details or preferences are currently remembered."}

    facts = []
    for k, v in memory.items():
        facts.append(f"- {k}: {v}")

    memory_context = "\n".join(facts)
    return {"memory_context": memory_context}
