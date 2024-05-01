# JupyterHub on Docker Compose

This is a project example on how to create a system around JupyterLab + JupyterHub using Docker Compose.
Multiple kernels are pre-configured and available to the users (see _jupyterlab/Dockerfile_ to understand the installation process if more are required):
- Bash
- C#
- C/C++
- Go
- Python 3
- R
- Ruby
- Rust

Note that each kernel has its own process for installation.

## Installation

- Be sure to have docker & docker-compose on your host machine.
- Create a new network on docker, for JupyterHub to be able to communicate with JupyterLab:
`docker network create jupyter_network`
- Build the project
`docker-compose build`
- Run the project
`docker-compose up -d`
- Create user(s) from the JupyterHub container
```
docker-compose exec jupyterhub bash
> adduser {username}
```


## How to use
The web interface is available at http://127.0.0.1:8000.
The user will be prompted to authentify using the login/password from the JupyterHub system.

A new container is created when the user connects, and is destroyed automatically when the user close its server or logout.
We use the default Jupyter username 'jovyan'. It is configured as sudoer, but can be deactivated when building the image (see _jupyterlab/Dockerfile_).

## Persistence
We need to persist two applications:
- JupyterHub, it is automatically stored in the volume _jupyterhub_data_. It contains the users authentications.
- The datas of our users' instances. It is stored in automatically created volumes _jupyterhub-user-{username}_.
These volumes only contain the users homes. So that the rest of the environment (installed packages etc) is destroyed when the user logout.

## References
- JupyterLab docker documentation: https://jupyter-docker-stacks.readthedocs.io/en/latest/
- JupyterHub docker documentation: https://jupyterhub.readthedocs.io/en/stable/tutorial/quickstart-docker.html
- See https://github.com/defeo/jupyterhub-docker as the main inspiration to write this project
- Bash kernel: https://github.com/takluyver/bash_kernel
- C# kernel: https://github.com/zabirauf/icsharp
- C/C++ kernel: https://github.com/shiroinekotfs/jupyter-cpp-kernel
- Go kernel: https://github.com/janpfeifer/gonb
- R kernel: https://irkernel.github.io/
- Ruby kernel: https://github.com/SciRuby/iruby
- Rust kernel: https://github.com/evcxr/evcxr/tree/main/evcxr_jupyter
