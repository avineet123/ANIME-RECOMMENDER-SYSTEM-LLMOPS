## Parent image
FROM python:3.10-slim

## Essential environment variables

# PYTHONDONTWRITEBYTECODE=1 prevents Python from writing .pyc (bytecode cache) files to disk.
# PYTHONUNBUFFERED=1 ensures that Python output is shown in real-time (helpful for logs).

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

## Work directory inside the docker container
WORKDIR /app

## Installing system dependencies

# apt-get update: updates the package list from the Debian repositories.
# apt-get install -y: installs system packages.
# build-essential: a package with compiler tools (required for compiling some Python packages).
# curl: command-line tool for HTTP requests.
# rm -rf /var/lib/apt/lists/*: deletes cached package lists to reduce image size.

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

## Copying ur all contents from local to app

# Copies everything from your local project directory to the /app directory inside the container.

COPY . .

## Run setup.py

#-e .: installs the current project in editable mode (good for development with setup.py or pyproject.toml present).

RUN pip install --no-cache-dir -e .

# Used PORTS
EXPOSE 8501

# Run the app 

# Sets the default command to run when the container starts.
# Runs a Streamlit app located at app/app.py.
# --server.port=8501: Streamlit will listen on port 8501.
#--server.address=0.0.0.0: makes the app accessible from outside the container.
# --server.headless=true: prevents Streamlit from trying to open a web browser (important inside containers).

CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0","--server.headless=true"]
