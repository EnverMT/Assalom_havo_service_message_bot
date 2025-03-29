import logging
from config import load_config

env_config = load_config(".env")


level = logging.ERROR

if env_config.env_mode.mode == "development":
    print("Development mode detected")
    level = logging.DEBUG

logging.basicConfig(level=level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.critical("Logger initialized in %s mode", logging.getLevelName(level))
