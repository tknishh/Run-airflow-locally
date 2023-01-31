from typing import Dict

from phiterm.workspace.ws_enums import WorkspaceStarterTemplate

template_to_repo_map: Dict[WorkspaceStarterTemplate, str] = {
    WorkspaceStarterTemplate.aws: "https://github.com/phidatahq/aws-dp-template.git",
    WorkspaceStarterTemplate.aws_snowflake: "https://github.com/phidatahq/aws-snowflake-dp-template.git",
    WorkspaceStarterTemplate.aws_backend: "https://github.com/phidatahq/aws-backend-template.git",
}
