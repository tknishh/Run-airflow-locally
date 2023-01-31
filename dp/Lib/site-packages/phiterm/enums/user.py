from phiterm.utils.enums import ExtendedEnum


class UserAuthProviderEnum(ExtendedEnum):
    email_pass = "email_pass"
    google = "google"
    github = "github"
    gitlab = "gitlab"
    linkedin = "linkedin"
    aws = "aws"
    api = "api"


class VersionControlProviderEnum(ExtendedEnum):
    GITHUB = "GITHUB"
    GITLAB = "GITLAB"
    BITBUCKET = "BITBUCKET"


class UserPermissions(ExtendedEnum):
    read_user = "read_user"
    edit_user = "edit_user"
    read_workspace = "read_workspace"
    edit_workspace = "edit_workspace"
    workspace_admin = "workspace_admin"
