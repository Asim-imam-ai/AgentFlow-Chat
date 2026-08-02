import sqlite3
import os
from langgraph.checkpoint.sqlite import SqliteSaver

# Global variables to manage database connection lifecycle
_conn = None
_checkpointer = None

def get_checkpointer() -> SqliteSaver:
    """
    Returns a persistent, global SQLite checkpointer instance.
    This avoids context manager connection closing bugs by keeping the connection
    open for the lifetime of the application.
    """
    global _conn, _checkpointer
    if _checkpointer is None:
        db_dir = "data"
        os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join(db_dir, "langgraph_checkpoints.sqlite")
        
        # Open the connection with check_same_thread=False for multi-threaded uvicorn apps
        _conn = sqlite3.connect(db_path, check_same_thread=False)
        
        # Instantiate SqliteSaver with the connection object directly
        _checkpointer = SqliteSaver(_conn)
        
        # Run table creation migrations (required on startup)
        _checkpointer.setup()
        
    return _checkpointer

def close_checkpointer_connection() -> None:
    """
    Cleanly close the database connection on application shutdown.
    """
    global _conn, _checkpointer
    if _conn is not None:
        try:
            _conn.close()
        except Exception:
            pass
        _conn = None
        _checkpointer = None
