import os

DEBUG = True

# Use the DATABASE_URL environment variable (ie. Docker MariaDB connection) or a blank sqlite for tests
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///")
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True

# Use the JWT_SECRET_KEY if defined, otherwise set a default secret
JWT_SECRET_KEY = os.environ.get(
    "JWT_SECRET_KEY", "585c94ee-a1b7-11ea-bb37-0242ac130002"
)
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "585c94ee-a1b7-11ea-bb37-0242ac130002")
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = [
    "access",
    "refresh",
]
