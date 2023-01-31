from typing import Optional

from phiterm.conf.constants import PHI_CREDS_PATH
from phiterm.utils.common import pickle_object_to_file, unpickle_object_from_file
from phiterm.utils.log import logger


class PhiCliCreds:
    def __init__(self, auth_token: str):
        self._auth_token = auth_token

    @property
    def auth_token(self) -> str:
        return self._auth_token


def save_auth_token(auth_token: str):
    # logger.debug(f"Storing {auth_token} to {str(PHI_CREDS_PATH)}")
    creds = PhiCliCreds(auth_token)
    pickle_object_to_file(creds, PHI_CREDS_PATH)


def read_auth_token() -> Optional[str]:
    # logger.debug(f"Reading token from {str(PHI_CREDS_PATH)}")
    creds: PhiCliCreds = unpickle_object_from_file(PHI_CREDS_PATH)
    return creds.auth_token
