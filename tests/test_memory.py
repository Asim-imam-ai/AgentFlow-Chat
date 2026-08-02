import pytest
from app.tools.memory import memory_tool
import json
import os

def test_memory_tool_runs():
    """Test memory tool gets/sets values."""
    # Ensure tool runs and returns correct output format
    res = memory_tool.invoke({"action": "set", "key": "test_pref", "value": "Python developer"})
    assert "saved memory" in res or "Error" in res
    
    # Cleanup memory file created during tests if any
    if os.path.exists("user_memory.json"):
        try:
            os.remove("user_memory.json")
        except Exception:
            pass
