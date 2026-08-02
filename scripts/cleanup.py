import logging
import os
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agentflow.scripts.cleanup")


def cleanup():
    logger.info("Cleaning up temporary workspace files...")

    # 1. Delete SQLite database files inside data folder (except keep data/ folder structure)
    data_dir = "data"
    if os.path.exists(data_dir):
        for item in os.listdir(data_dir):
            item_path = os.path.join(data_dir, item)
            # Remove DBs and pickle files
            if os.path.isfile(item_path) and item.endswith((".db", ".sqlite", ".pkl")):
                try:
                    os.remove(item_path)
                    logger.info(f"Removed database file: {item_path}")
                except Exception as e:
                    logger.warning(f"Could not remove file {item_path}: {e}")

    # 2. Clear uploads folder
    upload_dir = "uploads"
    if os.path.exists(upload_dir):
        for item in os.listdir(upload_dir):
            item_path = os.path.join(upload_dir, item)
            if os.path.isfile(item_path):
                try:
                    os.remove(item_path)
                    logger.info(f"Removed upload file: {item_path}")
                except Exception as e:
                    logger.warning(f"Could not remove file {item_path}: {e}")

    # 3. Clean up root python caches
    for root, dirs, files in os.walk("."):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            try:
                shutil.rmtree(pycache_path)
                logger.info(f"Removed python cache: {pycache_path}")
            except Exception:
                pass


if __name__ == "__main__":
    cleanup()
