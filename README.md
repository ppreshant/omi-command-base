# omi-command-base

This repository provides a **Conda/Micromamba environment** for managing workflows using **Nextflow** and **Singularity** (via **Apptainer**).

## Installation

To create the environment, follow these steps:

### 1. Install Micromamba

If you don't have `micromamba` installed, you can download it by following the instructions on the official [micromamba documentation](https://mamba.readthedocs.io/en/latest/installation.html).

For `micromamba`, you can use the following commands to download and install it:

```bash
curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba
sudo mv bin/micromamba /usr/local/bin/micromamba
```

### 2. Create the Environment

Once `micromamba` (or Conda) is installed, you can create the environment from the `environment.yml` file:

#### Using Micromamba

If you're using **Micromamba**, run the following command to create the environment:

```bash
micromamba env create -f environment.yml
```

## Command Server

The `omi-command-base` package includes a FastAPI-based command execution server that provides a secure and isolated environment for running shell commands. The server exposes a REST API for command execution and monitoring.

### Components

- `command_server.py`: FastAPI server implementation for executing commands

### Usage

1. Update the conda environment to include FastAPI dependencies:
```bash
conda env update -f environment.yml
```

2. Start the command server:
```bash
python command_server.py
```

The server will run on `http://localhost:8000` by default.

### API Endpoints

- `POST /api/v1/commands`: Submit a new command for execution
  ```json
  {
    "command": "string",
    "working_directory": "string (optional)"
  }
  ```
- `GET /api/v1/commands/{command_id}/status`: Check command execution status
  ```json
  {
    "command_id": "string",
    "status": "pending|running|completed|failed",
    "exit_code": "integer (if completed)",
    "start_time": "datetime",
    "end_time": "datetime (if completed)"
  }
  ```
- `GET /api/v1/commands/{command_id}/output`: Get command output
  ```json
  {
    "command_id": "string",
    "stdout": "string",
    "stderr": "string"
  }
  ```