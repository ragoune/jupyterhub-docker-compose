# JupyterHub configuration
#
## If you update this file, do not forget to delete the `jupyterhub_data` volume before restarting the jupyterhub service:
##
##     docker volume rm jupyterhub_jupyterhub_data
##
## or, if you changed the COMPOSE_PROJECT_NAME to <name>:
##
##    docker volume rm <name>_jupyterhub_data
##

import os

## Generic
c.JupyterHub.admin_access = True
c.Spawner.default_url = '/lab'

## Docker spawner
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.JupyterHub.hub_ip = os.environ['HUB_IP']
c.JupyterHub.shutdown_on_logout = True
c.DockerSpawner.image = os.environ['DOCKER_JUPYTERLAB_CONTAINER']
c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']

## user data persistence
# see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan'
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }
c.DockerSpawner.remove = True

## capacities
c.DockerSpawner.cpu_limit = 2
c.DockerSpawner.mem_limit = '32G'
c.ResourceUseDisplay.track_cpu_percent = True
c.ResourceUseDisplay.mem_limit = True
c.ResourceUseDisplay.mem_warning_threshold = 0.1
c.ResourceUseDisplay.enable_prometheus_metrics = False
