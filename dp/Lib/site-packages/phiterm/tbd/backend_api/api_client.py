from dataclasses import dataclass
from typing import Optional


@dataclass
class BackendApi:

    # /auth paths
    cli_auth: str = "auth/cliauth"
    sign_in: str = "auth/signin"
    sign_up: str = "auth/signup"
    authenticate: str = "auth/authenticate"
    ping: str = "auth/ping"

    # /user paths
    user_read: str = "user/read"
    user_update: str = "user/update"
    user_cli_auth: str = "user/cliauth"

    # /workspace paths
    workspace_update: str = "workspace/update"
    workspace_read_primary: str = "workspace/read/primary"
    workspaces_read_available: str = "workspace/read/available"
    workspace_upsert_from_cli: str = "workspace/upsertfromcli"


def get_authenticated_client():
    """Returns an instance of httpx.Client which with preconfigured auth and base url"""

    from httpx import Client

    from phiterm.conf.constants import (
        APP_NAME,
        APP_VERSION,
        BACKEND_API_URL,
        PHI_AUTH_TOKEN_COOKIE,
    )
    from phiterm.conf.auth import read_auth_token

    try:
        session_cookie: Optional[str] = read_auth_token()
    except Exception:
        # print_error("Could not authenticating user. Please run `phi auth` to fix")
        return None

    if session_cookie is None:
        return None
    return Client(
        base_url=BACKEND_API_URL,
        headers={"user-agent": f"{APP_NAME}/{APP_VERSION}"},
        cookies={PHI_AUTH_TOKEN_COOKIE: session_cookie},
        timeout=60,
    )
