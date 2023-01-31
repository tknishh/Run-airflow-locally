"""Phi Workflow Cli

This is the entrypoint for the `phi wf` commands
"""

from datetime import datetime
from typing import Optional, cast

import typer

from phiterm.utils.cli_console import (
    print_conf_not_available_msg,
    print_active_workspace_not_available,
    print_available_workspaces,
)
from phiterm.workflow.wf_enums import WorkflowEnv
from phiterm.utils.dttm import dttm_str_to_dttm
from phiterm.utils.log import logger, set_log_level_to_debug

wf_app = typer.Typer(
    name="wf",
    short_help="Run workflows",
    help="""\b
Use `phi wf <command>` to run workflows.
Run `phi wf <command> --help` for more info.
    """,
    no_args_is_help=True,
    add_completion=False,
    invoke_without_command=True,
    options_metavar="\b",
    subcommand_metavar="<command>",
)


@wf_app.command(short_help="Run workflow", options_metavar="\b", no_args_is_help=True)
def run(
    workflow: str = typer.Argument(
        ...,
        help="Workflow path: `dir/file` inside the workflow directory",
        metavar="[workflow]",
        show_default=False,
    ),
    env_filter: Optional[str] = typer.Option(
        "local",
        "-e",
        "--env",
        metavar="",
        help="The environment to run the workflow in",
    ),
    app_name: Optional[str] = typer.Option(
        None,
        "-a",
        "--app",
        metavar="",
        help="The App to run the workflow in.",
        show_default=False,
        hidden=True,
    ),
    run_date: Optional[str] = typer.Option(
        None,
        "-dt",
        "--date",
        help="Run datetime for the workflow. Example: '2023-01-01' or '2023-01-01T01:00'",
        show_default=False,
    ),
    dry_run: bool = typer.Option(
        False,
        "-dr",
        "--dry-run",
        help="Perform a dry run for each task. Does not run the task.",
    ),
    detach: bool = typer.Option(
        False,
        "--detach",
        help="[experimental] Run the command in the background.",
        hidden=True,
    ),
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    """\b
    Run a workflow in the target environment.

    \b
    Examples:
    $ phi wf run crypto/prices -> Runs the crypto/prices workflow in the local environment
    """
    from phiterm.conf.phi_conf import PhiConf, PhiWsData
    from phiterm.workflow.wf_operator import run_workflow
    from phiterm.utils.load_env import load_env

    if print_debug_log:
        set_log_level_to_debug()

    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if not phi_conf:
        print_conf_not_available_msg()
        return

    active_ws_data: Optional[PhiWsData] = phi_conf.get_active_ws_data()
    if active_ws_data is None:
        print_active_workspace_not_available()
        avl_ws = phi_conf.available_ws
        if avl_ws:
            print_available_workspaces(avl_ws)
        return

    # Load environment from .env
    load_env(dotenv_dir=active_ws_data.ws_root_path)

    target_env: Optional[WorkflowEnv] = None
    target_app: Optional[str] = app_name
    target_dttm: Optional[datetime] = (
        dttm_str_to_dttm(run_date) if run_date else datetime.now()
    )
    if target_dttm is None:
        logger.error("Invalid run_date")
        return

    default_env = (
        active_ws_data.ws_config.default_env if active_ws_data.ws_config else None
    )
    target_env_str = env_filter or default_env or "dev"
    try:
        target_env = cast(WorkflowEnv, WorkflowEnv.from_str(target_env_str))
    except Exception as e:
        logger.error(e)
        logger.error(
            f"{target_env_str} is not supported, please choose from: {WorkflowEnv.values_list()}"
        )
        return

    logger.debug("Running workflow")
    logger.debug(f"\tworkflow     : {workflow}")
    logger.debug(f"\ttarget_env   : {target_env}")
    logger.debug(f"\ttarget_dttm  : {target_dttm}")
    logger.debug(f"\tdry_run      : {dry_run}")
    logger.debug(f"\tdetach       : {detach}")
    logger.debug(f"\ttarget_app   : {target_app}")
    run_workflow(
        wf_description=workflow,
        ws_data=active_ws_data,
        target_env=target_env,
        target_dttm=target_dttm,
        dry_run=dry_run,
        detach=detach,
        target_app=target_app,
    )


# @wf_app.command(short_help="Build workflow")
# def build(workflow: str = typer.Argument(..., help="The workflow to build")):
#     print_info(f"Building workflow {workflow}")
#     print_info(f"To be implemented")
#


@wf_app.command(short_help="List workflows", options_metavar="\b", no_args_is_help=True)
def ls(
    workflow: str = typer.Argument(
        ...,
        help="Workflow path: `dir/file` inside the workflow directory",
        metavar="[workflow]",
        show_default=False,
    ),
    print_debug_log: bool = typer.Option(
        False,
        "-d",
        "--debug",
        help="Print debug logs.",
    ),
):
    from phiterm.conf.phi_conf import PhiConf, PhiWsData
    from phiterm.workflow.wf_operator import list_workflows
    from phiterm.utils.load_env import load_env

    if print_debug_log:
        set_log_level_to_debug()

    phi_conf: Optional[PhiConf] = PhiConf.get_saved_conf()
    if not phi_conf:
        print_conf_not_available_msg()
        return

    active_ws_data: Optional[PhiWsData] = phi_conf.get_active_ws_data(refresh=True)
    if active_ws_data is None:
        print_active_workspace_not_available()
        avl_ws = phi_conf.available_ws
        if avl_ws:
            print_available_workspaces(avl_ws)
        return

    # Load environment from .env
    load_env(dotenv_dir=active_ws_data.ws_root_path)

    list_workflows(
        wf_description=workflow,
        ws_data=active_ws_data,
    )
