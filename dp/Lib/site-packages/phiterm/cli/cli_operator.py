from typing import Optional

from typer import launch as typer_launch

from phiterm.api.exceptions import CliAuthException
from phiterm.api.user import (
    sign_in_user,
    authenticate_and_get_user,
)
from phiterm.conf.constants import PHI_CONF_DIR, PHI_SIGNIN_URL_WITHOUT_PARAMS
from phiterm.conf.phi_conf import PhiConf
from phiterm.schemas.user import UserSchema, EmailPasswordSignInSchema
from phiterm.utils.cli_auth_server import (
    get_port_for_auth_server,
    get_auth_token_from_web_flow,
)
from phiterm.utils.cli_console import (
    print_error,
    print_heading,
    print_info,
)
from phiterm.utils.filesystem import delete_from_fs
from phiterm.utils.log import logger


def delete_phidata_conf() -> None:
    logger.debug("Removing existing Phidata configuration")
    delete_from_fs(PHI_CONF_DIR)


def authenticate_user() -> bool:
    """Authenticate the user using credentials from phidata.com
    Steps:
    1. Authenticate the user by opening the phidata sign-in url
        and the web-app will post an auth token to a mini http server
        running on the auth_server_port.
    2. Using the auth_token, authenticate the CLI with backend and
        save the auth_token to PHI_AUTH_TOKEN_PATH.
        This step is handled by authenticate_and_get_user()
    5. After the user is authenticated create a PhiConf if needed.
    """

    print_heading("Logging in at phidata.com ...")

    auth_server_port = get_port_for_auth_server()
    redirect_uri = "http%3A%2F%2Flocalhost%3A{}%2F".format(auth_server_port)
    auth_url = "{}?source=cli&action=signin&redirecturi={}".format(
        PHI_SIGNIN_URL_WITHOUT_PARAMS, redirect_uri
    )
    print_info("\nYour browser will be opened to visit:\n{}".format(auth_url))
    typer_launch(auth_url)
    print_info("\nWaiting for a response from browser...\n")

    tmp_auth_token = get_auth_token_from_web_flow(auth_server_port)
    if tmp_auth_token is None:
        print_error(f"Could not authenticate, please run `phi auth` again")
        return False

    try:
        user: Optional[UserSchema] = authenticate_and_get_user(tmp_auth_token)
    except CliAuthException as e:
        logger.exception(e)
        print_error(f"Could not authenticate, please run `phi auth` again")
        return False

    if user is None:
        print_error(f"Could not get user data, please run `phi auth` again")
        return False

    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if phi_conf is None:
        phi_conf = PhiConf(user)

    phi_conf.user = user
    print_info("Welcome {}, you are now logged in\n".format(user.email))

    return phi_conf.sync_workspaces_from_api()


def initialize_phidata(reset: bool = False, login: bool = False) -> bool:
    """This function is called by `phi init` and initializes phidata on the users machine.
    Steps:
    1. Check if PHI_CONF_DIR exists, if not, create it. If reset == True, recreate PHI_CONF_DIR.
    2. Check if PhiConf exists, if it does, try and authenticate the user
        If the user is authenticated, phi is configured and authenticated. Return True.
    3. If PhiConf does not exist, create a new PhiConf. Return True.
    """

    print_heading("Welcome to phidata!\n")
    if reset:
        delete_phidata_conf()

    logger.debug("Initializing phidata")

    # Check if ~/.phi exists, if it is not a dir - delete it and create the dir
    if PHI_CONF_DIR.exists():
        logger.debug(f"{PHI_CONF_DIR} exists")
        if not PHI_CONF_DIR.is_dir():
            try:
                delete_from_fs(PHI_CONF_DIR)
            except Exception as e:
                logger.exception(e)
                print_info(
                    f"Something went wrong, please delete {PHI_CONF_DIR} and run `phi init` again"
                )
                return False
            PHI_CONF_DIR.mkdir(parents=True)
    else:
        PHI_CONF_DIR.mkdir(parents=True)
        logger.debug(f"created {PHI_CONF_DIR}")

    # Confirm PHI_CONF_DIR exists otherwise we should return
    if PHI_CONF_DIR.exists():
        logger.debug(f"Your phidata config is stored at: {PHI_CONF_DIR}")
    else:
        print_info(f"Something went wrong, please run `phi init` again")
        return False

    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if phi_conf is None:
        # Create a new PhiConf
        phi_conf = PhiConf()

    # Authenticate user
    if login:
        auth_success = authenticate_user()

    if phi_conf is not None:
        print_info("Phidata is initialized. Next steps:\n")
        print_info(" 1. Run `phi ws init` to create a new workspace")
        print_info(" 2. Run `phi ws setup` to setup an existing workspace")
        print_info(" 3. Run `phi ws up -dr` to dry-run workspace deploy")
        print_info(" 4. Run `phi ws up` to deploy the workspace")
    return True


def sign_in_using_cli() -> bool:
    from getpass import getpass

    print_heading("Log in")
    email_raw = input("email: ")
    pass_raw = getpass()

    if email_raw is None or pass_raw is None:
        print_error("Incorrect email or password")

    try:
        user: Optional[UserSchema] = sign_in_user(
            EmailPasswordSignInSchema(email=email_raw, password=pass_raw)
        )
    except CliAuthException as e:
        logger.exception(e)
        return False

    if user is None:
        print_error("Could not get user data, please log in again")
        return False

    print_info("Welcome {}, you are now authenticated\n".format(user.email))

    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if phi_conf is None:
        phi_conf = PhiConf()

    phi_conf.user = user
    return phi_conf.sync_workspaces_from_api()
