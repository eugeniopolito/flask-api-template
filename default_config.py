import os

DEBUG = True

# Docker MariaDB
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///")
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "12345")
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "12345")
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = [
    "access",
    "refresh",
]
