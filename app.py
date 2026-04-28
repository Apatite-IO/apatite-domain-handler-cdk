#!/usr/bin/env python3
import os
from pathlib import Path
from dotenv import load_dotenv

# Shared env (global across projects file)
SHARED_ENV_FILE = Path.home() / ".config" / ".env"
load_dotenv(dotenv_path = SHARED_ENV_FILE, override = False)

# Project specific env file
PROJECT_ROOT = Path(__file__).resolve().parent
PROJECT_ENV_FILE = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path = PROJECT_ENV_FILE, override = True)

import aws_cdk as cdk
from config.setup_stack import setup_stack
from project_name_cdk.project_name_cdk import cdk_ProjectName

env = os.getenv("ENVIRONMENT")

app = cdk.App()
setup_stack(env, app, "PROJECT_NAME", cdk_ProjectName)

app.synth()
