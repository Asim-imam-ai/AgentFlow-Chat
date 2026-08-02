from app.graph.builder import build_agent_graph
import logging

logger = logging.getLogger("agentflow.graph.factory")

# Global singleton for compiled graph
_compiled_graph = None

def get_graph():
    """
    Get the compiled agent graph singleton.
    """
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_agent_graph()
    return _compiled_graph

def create_graph():
    """
    Create a new instance of the compiled agent graph.
    """
    return build_agent_graph()
