# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub.
# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.
import os
import docker

c = get_config()

##################################
# NOTEBOOK CONFIGURATION
##################################

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"

# Spawn containers from this image
c.DockerSpawner.image = os.environ["DOCKER_NOTEBOOK_IMAGE"]

# Connect containers to this Docker network
network_name = os.environ["DOCKER_NETWORK_NAME"]
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name

# Explicitly set notebook directory because we"ll be mounting a volume to it.
# Most `jupyter/docker-stacks` *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR") or "/home/jovyan/work"
c.DockerSpawner.notebook_dir = notebook_dir

# Mount the real user"s Docker volume on the host to the notebook user"s
# notebook directory in the container
c.DockerSpawner.volumes = {
    "jupyterhub-user-{username}": notebook_dir,
    # Personal network folder config (e.g. per user)
    os.environ.get("HOST_PERSONAL_NETWORK_FOLDER")+"{username}":  os.environ.get("DOCKER_PERSONAL_NETWORK_FOLDER"),
    # Shared network folder config (e.g. for all users)
    os.environ.get("HOST_SHARED_NETWORK_FOLDER"): os.environ.get("DOCKER_SHARED_NETWORK_FOLDER")
}

# Set the spawned container config
c.DockerSpawner.extra_host_config = {
    "device_requests": [
        docker.types.DeviceRequest(
            count=-1,
            capabilities=[["gpu"]],
        ),
    ],
}

# Notebook guarantees and limits
# c.Spawner.mem_guarantee = "16G"
# c.Spawner.mem_limit = "30G"
# c.Spawner.cpu_guarantee = 4.0
# c.Spawner.cpu_limit = 8.0

# Remove containers once they are stopped
c.DockerSpawner.remove = True

# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = "jupyterhub"
c.JupyterHub.hub_port = 8080
# c.JupyterHub.ip = "0.0.0.0"
# #c.JupyterHub.proxy_api_ip = "0.0.0.0"
# c.ConfigurableHTTPProxy.api_url = f"http://0.0.0.0:8081"
# c.DockerSpawner.hub_ip_connect = "jupyterhub"

##################################
# HUB DATA STORAGE CONFIGURATION
##################################

# Persist hub data on volume mounted inside container
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "postgresql+psycopg2://{host}:5432/{db}".format(
    host=os.environ["POSTGRES_HOST"],
    db=os.environ["POSTGRES_DB"],
)

##################################
# AUTHENTICATION CONFIGURATION
##################################

# Allow all signed-up users to login
c.Authenticator.allow_all = True

# Authenticate users with Native Authenticator
c.JupyterHub.authenticator_class = "nativeauthenticator.NativeAuthenticator"

# Allow anyone to sign-up without approval
c.NativeAuthenticator.open_signup = True

# Allowed admins
admin = os.environ.get("JUPYTERHUB_ADMIN")
if admin:
    c.Authenticator.admin_users = [admin]

##################################
# SSL/TLS CONFIGURATION
##################################

# c.JupyterHub.port = 443
# c.JupyterHub.ssl_key = os.environ["SSL_KEY"]
# c.JupyterHub.ssl_cert = os.environ["SSL_CERT"]