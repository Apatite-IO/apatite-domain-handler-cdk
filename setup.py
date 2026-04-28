'''
@Author: ingluvious

@Description:
    1. Create a Python Virtual Environment
    2. Install a basic set of requirements
    3. If requirements.txt exists, install that set of requirements
    4. Create the .env file
'''
import os
import subprocess
from pathlib import Path

venv_dir = Path(".venv")
venv_python = venv_dir / ("Scripts/python.exe" if Path("/").drive else "bin/python")

# Create the Virtual Env for where the proj packages will live
def createVirtualEnv():
    if not venv_dir.exists():
        print("Creating virtual environment...")
        subprocess.run(["uv", "venv", str(venv_dir), "--python", str(os.getenv("PYTHON_VERSION", "3.12"))], check=True)
    else:
        print("Virtual environment already exists.")

# Install the default packages
def installRequirements():
    print("Installing requirements...")

    default_packages = ["requests", "python-dotenv", "watchdog"]
    subprocess.run(["uv", "pip", "install", "--python", str(venv_python), "--upgrade", *default_packages], check=True)
    if Path("requirements.txt").exists():
        subprocess.run(["uv", "pip", "install", "--python", str(venv_python), "--upgrade", "-r", "requirements.txt"], check=True)

# Create the .env file
def createEnvFile():
    print("Checking .env file")
    env_file = Path(".env")
    if not env_file.exists():
        print("Creating .env file...")
        env_file.write_text("## Add your environment variables below ##\n")
    else:
        print(".env file already exists!")

# Load the global environments file from "~/.config/.env"
def loadGlobalEnv():
    global_env = Path.home() / ".config/.env"
    if global_env.exists():
        print("Loading global environment variables...")
        for line in global_env.read_text().splitlines():
            if line.strip() and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())

if __name__ == "__main__":
    loadGlobalEnv()
    createVirtualEnv()
    installRequirements()
    createEnvFile()

    print("\n✅ Setup complete!")
    
    is_windows = Path("/").drive != ""
    activate = str(venv_dir / ("Scripts/activate.bat" if is_windows else "bin/activate"))
    print(f"➡️  To activate your virtual environment:\n{''.join(['' if is_windows else 'source '])}{activate}")