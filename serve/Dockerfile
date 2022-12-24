ARG BASE_IMAGE="python:3.7"
FROM ${BASE_IMAGE}

ENV PYTHONUNBUFFERED TRUE

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    ca-certificates \
    g++ \
    python3-dev \
    python3-distutils \
    python3-venv \
    openjdk-11-jre-headless \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/* \
    && cd /tmp \
    && curl -O https://bootstrap.pypa.io/get-pip.py \
    && python3 get-pip.py \
    && rm get-pip.py

RUN python3 -m venv /home/venv

ENV PATH="/home/venv/bin:$PATH"

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN update-alternatives --install /usr/local/bin/pip pip /usr/local/bin/pip3 1

RUN pip install -U pip setuptools

RUN pip install --no-cache-dir torch==1.8.0 torchvision==0.9.1 torchserve==0.2.0

RUN useradd -m model-server

COPY dockerd-entrypoint.sh /usr/local/bin/dockerd-entrypoint.sh
COPY config.properties /home/model-server/config.properties

RUN chmod +x /usr/local/bin/dockerd-entrypoint.sh \
    && mkdir -p /home/model-server/tmp \
    && chown -R model-server /home/model-server \
    && chown -R model-server /home/venv

EXPOSE 8080 8081 8082

USER model-server
WORKDIR /home/model-server

COPY deeplabv3 ./deeplabv3
RUN pip install torch-model-archiver torch-workflow-archiver
RUN torch-model-archiver --model-name deeplabv3_resnet_101 --version 1.0 --model-file deeplabv3/model.py --serialized-file deeplabv3/deeplabv3_resnet101_coco-586e9e4e.pth --handler deeplabv3/handler.py --extra-files deeplabv3/deeplabv3.py,deeplabv3/intermediate_layer_getter.py,deeplabv3/fcn.py
RUN mkdir model-store && mv deeplabv3_resnet_101.mar /home/model-server/model-store/
RUN chown -R model-server /home/model-server/model-store \
    && cd /home/model-server/model-store

ENV TEMP=/home/model-server/tmp
ENTRYPOINT ["/usr/local/bin/dockerd-entrypoint.sh"]
CMD ["serve"]