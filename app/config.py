from starlette.config import Config

config = Config(".env")

DEBUG = config.get("DEBUG", bool, False)
