FROM quay.io/jupyter/minimal-notebook:2024-04-29

USER root
RUN apt update && apt install -y htop vim iputils-ping
USER $NB_USER

# resources usage display
RUN pip install jupyter-resource-usage

#######################################
# R kernel
#######################################
RUN conda install -y r-recommended r-irkernel && \
    R -e 'IRkernel::installspec()'

#######################################
# Go kernel
#######################################
ENV GO_VERSION=1.22.0
ENV GONB_VERSION="v0.9.6"
ENV GOROOT=/usr/local/go
ENV GOPATH=/opt/go
ENV PATH=$PATH:$GOROOT/bin:$GOPATH/bin

# Create Go directory for user -- that will not move if the user home directory is moved.
USER root
RUN mkdir ${GOPATH} && chown ${NB_USER}:users ${GOPATH}

USER root
WORKDIR /usr/local
RUN wget --quiet --output-document=- "https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz" | tar -xz \
    && go version

# Install GoNB (https://github.com/janpfeifer/gonb) in the user account
USER $NB_USER
WORKDIR ${HOME}
RUN export GOPROXY=direct && \
    go install "github.com/janpfeifer/gonb@${GONB_VERSION}" && \
    go install golang.org/x/tools/cmd/goimports@latest && \
    go install golang.org/x/tools/gopls@latest && \
    gonb --install

#######################################
# Rust kernel
#######################################
USER root
RUN apt install -y build-essential

USER $NB_USER
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    export PATH=$PATH:$HOME/.cargo/bin && \
    cargo install --locked evcxr_jupyter && \
    evcxr_jupyter --install


#######################################
# Ruby kernel
#######################################
USER root
RUN apt install -y libtool libffi-dev ruby ruby-dev make libzmq-ffi-perl ruby-ffi-rzmq
RUN gem install iruby && \
    iruby register --force
USER $NB_USER

#######################################
# Bash kernel
#######################################
RUN pip install bash_kernel && \
    python -m bash_kernel.install

#######################################
# c/c++ kernel
#######################################
RUN pip install jupyter-cpp-kernel

#######################################
# c# kernel
#######################################
USER root
RUN apt install -y ca-certificates gnupg && \
    gpg --homedir /tmp --no-default-keyring --keyring /usr/share/keyrings/mono-official-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF && \
    echo "deb [signed-by=/usr/share/keyrings/mono-official-archive-keyring.gpg] https://download.mono-project.com/repo/ubuntu stable-focal main" | sudo tee /etc/apt/sources.list.d/mono-official-stable.list && \
    apt update && \
    apt install -y mono-complete mono-dbg mono-runtime-dbg && \
    mozroots --import --machine --sync
USER $NB_USER
RUN git clone --recursive https://github.com/zabirauf/icsharp.git && \
    cd icsharp && \
    # update NuGet
    mono Engine/.nuget/NuGet.exe update -self && \
    mono .nuget/NuGet.exe update -self && \
    bash ./build.sh brew
COPY icsharp_kernel.json icsharp/kernel-spec/kernel.json
RUN chmod 755 /home/jovyan/icsharp/Kernel/bin/Release/iCSharp.Kernel.exe
RUN cd icsharp && jupyter-kernelspec install kernel-spec --user

#######################################
# sudoer jovyan
#######################################
USER root
RUN sudo usermod -a -G sudo $NB_USER
# Provide password-less sudo to NB_USER
RUN \
    sed -i /etc/sudoers -re 's/^%sudo.*/%sudo ALL=(ALL:ALL) NOPASSWD: ALL/g' && \
    sed -i /etc/sudoers -re 's/^root.*/root ALL=(ALL:ALL) NOPASSWD: ALL/g' && \
    sed -i /etc/sudoers -re 's/^#includedir.*/## **Removed the include directive** ##"/g' && \
    echo "${NB_USER} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    chmod g+w /etc/passwd
USER $NB_USER
