import os
import aws_cdk as cdk
from config.env_config import stack_config

def setup_stack(env, app, stack_name_env_var, stack_class):
    stack_name = os.getenv(stack_name_env_var)
    if not stack_name:
        raise ValueError(f"Environment variable {stack_name_env_var} is not set.")

    stack = stack_config.get(stack_name)
    if not stack:
        raise ValueError(f"Stack name {stack_name} not found in stack_config.")

    if not hasattr(stack, env):
        raise ValueError(f"Environment {env} not found in the config file for stack {stack_name}.")

    stack_configuration = getattr(stack, env)
    stack_class = stack_class(app, 
                              stack_configuration.stack_name, 
                              stack_configuration,
                              env=cdk.Environment(account=stack_configuration.aws_account, region=stack_configuration.region))
    return stack_class