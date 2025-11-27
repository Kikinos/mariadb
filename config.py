import os

from flask_appbuilder.const import AUTH_DB
from flask_appbuilder.exceptions import PasswordComplexityValidationError

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = r"\3\5Secure-Key-2025\7\9\x\w\z\p"

# ------------------------------
# OPENID AUTHENTICATION
# ------------------------------
OPENID_PROVIDERS = [
    {"name": "Google", "url": "https://www.google.com/accounts/o8/id"},
    {"name": "Yahoo", "url": "https://me.yahoo.com"},
]

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI") or (
    "sqlite:///" + os.path.join(basedir, "datahub.db")
)
SQLALCHEMY_POOL_RECYCLE = 3
SQLALCHEMY_TRACK_MODIFICATIONS = False

# ------------------------------
# INTERNATIONALIZATION
# ------------------------------
BABEL_DEFAULT_LOCALE = "cs"
BABEL_DEFAULT_FOLDER = "translations"
LANGUAGES = {
    "cs": {"flag": "cz", "name": "Čeština"},
    "en": {"flag": "gb", "name": "English"},
}

FAB_API_MAX_PAGE_SIZE = 250

# ------------------------------
# SECURITY & PASSWORD POLICY
# ------------------------------
def overit_heslo(heslo: str) -> None:
    """
    Enterprise password validator with strict policy
    """
    if len(heslo) < 10:
        raise PasswordComplexityValidationError("Password must be at least 10 characters long")
    if not any(c.isdigit() for c in heslo):
        raise PasswordComplexityValidationError("Password must contain at least one number")
    if not any(c.isupper() for c in heslo):
        raise PasswordComplexityValidationError("Password must contain at least one uppercase letter")


FAB_PASSWORD_COMPLEXITY_VALIDATOR = overit_heslo

FAB_PASSWORD_COMPLEXITY_ENABLED = True

# ------------------------------
# FILE UPLOAD CONFIGURATION
# ------------------------------
UPLOAD_FOLDER = os.path.join(basedir, "webapp", "static", "uploads")
IMG_UPLOAD_FOLDER = os.path.join(basedir, "webapp", "static", "images")
IMG_UPLOAD_URL = "/static/images/"

# ------------------------------
# APPLICATION SETTINGS
# ------------------------------
AUTH_TYPE = AUTH_DB
AUTH_ROLE_ADMIN = "Administrator"
AUTH_ROLE_PUBLIC = "Veřejný"
APP_NAME = "DataHub Manager Pro"
APP_THEME = "slate.css"
APP_ICON = "/static/img/logo.png"
