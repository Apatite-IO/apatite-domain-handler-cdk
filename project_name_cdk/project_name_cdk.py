from aws_cdk import (
    Stack
)
from constructs import Construct
from config.env_config import StackEnvConfig

class cdk_ProjectName(Stack):

    def __init__(self, scope: Construct, construct_id: str, config: StackEnvConfig, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        
        self.template_options.description = f"{config.project_name} - {config.environment} stack"