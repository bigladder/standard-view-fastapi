import os

SECRET_KEY = os.environ.get("SECRET_KEY", "6c03627fdc3f3928b5fb04c384ae5c75")
CACHE_SIZE = int(os.environ.get("CACHE_SIZE", str(1000)))
HTTPS_ONLY = bool(os.environ.get("HTTPS_ONLY", str(False)))
SESSION_AGE = int(os.environ.get("SESSION_AGE", str(60 * 60 * 24)))  # 1 day
