from pathlib import Path

APP_NAME = "phiterm"
APP_VERSION = "0.1.0"

DEFAULT_WS_NAME = "data-platform"

PHI_CONF_DIR: Path = Path.home().resolve().joinpath(".phi")
PHI_CONF_PATH: Path = PHI_CONF_DIR.joinpath("conf")
PHI_AUTH_TOKEN_PATH: Path = PHI_CONF_DIR.joinpath("token")
PHI_CREDS_PATH: Path = PHI_CONF_DIR.joinpath("creds")

# Rest API Constants
PHI_API_MODE = "prd"
PHI_AUTH_TOKEN_COOKIE: str = "__phi_session"
PHI_AUTH_TOKEN_HEADER: str = "X-PHIDATA-AUTH-TOKEN"
PHI_SIGNIN_URL_WITHOUT_PARAMS: str = (
    "http://localhost:3000/signin"
    if PHI_API_MODE == "dev"
    else "https://phidata.com/signin"
)
BACKEND_API_URL: str = (
    "http://localhost:8000" if PHI_API_MODE == "dev" else "https://api.phidata.com"
)

# Logger Names
PHI_LOGGER_NAME = "phi"
PHIDATA_LOGGER_NAME = "phidata"
