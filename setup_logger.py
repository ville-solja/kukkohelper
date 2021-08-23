import logging
logger = logging.getLogger("discord")
level = logging.getLevelName("INFO")
logger.setLevel(level)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(console_handler)