# omi-command-env

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