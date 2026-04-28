import os
from config.validators import validate_env_vars

class StackEnvConfig:
    def __init__(self, project_name, environment, aws_account):
        validate_env_vars(
            "PROJECT_NAME",
            "PROJECT_OWNER",
            "AWS_APATITE_SANDBOX_ACCOUNT_ID",
            "AWS_REGION",
        )
        self.project_owner = os.getenv("PROJECT_OWNER")
        self.aws_account = aws_account
        self.region = os.getenv("AWS_REGION")
        self.project_name = project_name
        self.stack_name = project_name
        self.environment = environment
        self.application_id_tag = os.getenv("PROJECT_NAME")

class stackConfig:
    def __init__(self, project_name):
        self.sandbox = StackEnvConfig(
            project_name = project_name,
            environment = "sandbox",
            aws_account = os.getenv("AWS_APATITE_SANDBOX_ACCOUNT_ID")
        )

stack_config = {
    os.getenv("PROJECT_NAME") : stackConfig(project_name = os.getenv("PROJECT_NAME"))
}