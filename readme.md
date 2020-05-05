# GPU-jupyterhub
This jupyterhub implementation allows for Nvidia GPU access using the nvidia-docker-2 container runtime.

## Requirements
- A cuda driver must be installed on the host system, you can check this by running `nvidia-smi` in the terminal.
- Docker 19.03 or higher.
- Docker compose 1.25.5 or higher.
I've personally found the [DigitalOcean Tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-ubuntu-18-04) to be the most reliable. Make sure to change the version number to `1.25.5`!
- The nvidia-container-runtime needs to be installed:
```bash
sudo apt-get install nvidia-container-runtime
```
- Nvidia docker2 needs to be installed see their [Github](https://github.com/NVIDIA/nvidia-docker) for instructions.
- 


## Installation
To make this work make sure to change your `/etc/docker/daemon.json` to the following:
```json
{
    "runtimes": {
        "nvidia": {
            "path": "/usr/bin/nvidia-container-runtime",
            "runtimeArgs": []
        }
    }
}

```
