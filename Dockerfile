# https://github.com/austinbrian/jupydocker

FROM ubuntu:latest
RUN apt-get update &&\
    apt-get -y update &&\
    apt-get install -y  build-essential python3.8 python3-pip python3-dev

COPY . .
WORKDIR /src

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt 

# Add Tini. Tini operates as a process subreaper for jupyter. This prevents kernel crashes.
ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]

# CMD ["jupyter", "notebook", "/src/main.ipynb",\
#      "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=''"]
 