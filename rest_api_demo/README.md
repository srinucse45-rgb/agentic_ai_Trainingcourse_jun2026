# Install UV

powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Initialize UV project

uv init

# Install fastapi

uv add fastapi
uv add uvicorn

# TODO: Learn about various uv commands to update, remove packages

# Now, it is time to activate .venv

# In mac and linux

source .venv/bin/activate

# Activate venv In Windows Machine

.venv\Scripts\activate.bat

# To run this project

uv run uvicorn app.main:app --reload
