import logging

logging.basicConfig(level="INFO", filename= "Log.log", filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)