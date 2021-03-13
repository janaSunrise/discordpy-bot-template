import os

# ---- About bot section ----
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "=")

branding = ""
creator = ""
devs = []  # ID of the developers.

# -- Logger configuration --
log_file = "logs/bot.log"
log_level = "INFO"
log_format = (
    "<green>{time:YYYY-MM-DD hh:mm:ss}</green> | <level>{level: <8}</level> | "
    "<cyan>{name: <18}</cyan> | <level>{message}</level>"
)
log_file_size = "400 MB"
