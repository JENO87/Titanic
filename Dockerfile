ARG BASE_IMAGE="python:3.13-slim"

FROM ${BASE_IMAGE}

ARG GITLAB_TOKEN
RUN echo "GITLAB_TOKEN value: $GITLAB_TOKEN"

RUN apt-get update \
    && apt-get install -y ca-certificates openssl \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3-dev \
        gcc \
        git \
        make \
    && update-ca-certificates

WORKDIR /app

COPY . /app

ARG REQUIREMENTS_FILE=requirements.txt

RUN pip install --quiet --upgrade pip

ADD requirements.txt .

RUN python -m pip install -r ${REQUIREMENTS_FILE} --trusted-host github.com--trusted-host release-assets.githubusercontent.com
RUN python -m pip install --trusted-host pypi.org--trusted-host files.pythonhosted.org--user pip-system-certs

ENV PYTHONPATH="${PYTHONPATH}:/app/src"
ENV PYTHONDONTWRITEBYTECODE=1
