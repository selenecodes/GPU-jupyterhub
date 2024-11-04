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


## Installation
### Preparation
To make `runtime: nvidia` work we need to change our `/etc/docker/daemon.json` to the following:
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

### Building our notebook containers
We can now build our notebook containers with:
```bash
#cd notebooks/{notebook-folder}
#docker build -t {notebook-folder-name} .

# Example
cd notebooks/base-notebook
docker build -t "base-notebook" .

cd ..
cd notebooks/minimal-notebook
docker build -t "minimal-notebook"

# And so on
```

### Building the hub
**Note:** Make sure to change the `userlist` file to include your Github username.

```bash
# Make sure to do this in the root of the repo*
docker-compose up --build
```

### Common Issues
- Volume `jupyterhub-db-data` or `jupyterhub-data` not found.
```bash
docker volume create --name="jupyterhub-data"
```
- Network `jupyterhub-network` not found.
```bash
docker network create "jupyterhub-network"
```
- No such file or directory: '/data/jupyerhub_cookie_secret'
Run the following command whilst replacing $DATA_VOLUME_CONTAINER with the actual path.
```bash
openssl rand -hex 32 > {$DATA_VOLUME_CONTAINER}/jupyterhub_cookie_secret
```