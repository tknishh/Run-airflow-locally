from typing import Optional, List

from phiterm.conf.phi_conf import PhiWsData
from phiterm.utils.cli_console import (
    print_info,
    print_heading,
    print_info,
)
from phiterm.utils.log import logger


def run_command(
    command: str,
    ws_data: PhiWsData,
    target_env: str,
    target_app: Optional[str] = None,
) -> None:
    """Run a command in databox."""
    from phidata.docker.config import DockerConfig
    from phidata.k8s.config import K8sConfig
    from phidata.infra.config import InfraConfig
    from phiterm.workspace.ws_operator import filter_and_prep_configs

    if ws_data is None or ws_data.ws_config is None:
        logger.error("WorkspaceConfig invalid")
        return
    ws_config = ws_data.ws_config

    # Set the local environment variables before processing configs
    ws_config.set_local_env()

    # Get the config to run the command in
    filtered_configs: List[InfraConfig] = filter_and_prep_configs(
        ws_config=ws_config,
        target_env=target_env,
    )

    # Final run status
    run_status_list: List[bool] = []
    for config in filtered_configs:
        if isinstance(config, DockerConfig):
            from phiterm.docker.docker_operator import run_command_docker

            _run_status = run_command_docker(
                command=command,
                docker_config=config,
                target_app=target_app,
            )
            run_status_list.append(_run_status)
        if isinstance(config, K8sConfig):
            from phiterm.k8s.k8s_operator import run_command_k8s

            _run_status = run_command_k8s(
                command=command.split(),
                k8s_config=config,
                target_app=target_app,
            )
            run_status_list.append(_run_status)

    if all(run_status_list):
        print_heading("Command run success")
    else:
        logger.error(f"Command run failure: {run_status_list}")
