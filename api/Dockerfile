# base image
FROM python:3.10-slim-bookworm AS base

LABEL maintainer="kesixcross@gmail.com"

# install packages
FROM base as packages

RUN touch /etc/apt/sources.list
RUN echo "deb https://mirrors.tencent.com/debian/ bookworm main non-free non-free-firmware contrib" >> /etc/apt/sources.list \
    echo "deb-src https://mirrors.tencent.com/debian/ bookworm main non-free non-free-firmware contrib" >> /etc/apt/sources.list \
    echo "deb https://mirrors.tencent.com/debian-security/ bookworm-security main" >> /etc/apt/sources.list \
    echo "deb-src https://mirrors.tencent.com/debian-security/ bookworm-security main" >> /etc/apt/sources.list \
    echo "deb https://mirrors.tencent.com/debian/ bookworm-updates main non-free non-free-firmware contrib" >> /etc/apt/sources.list \
    echo "deb-src https://mirrors.tencent.com/debian/ bookworm-updates main non-free non-free-firmware contrib" >> /etc/apt/sources.list \
    echo "deb https://mirrors.tencent.com/debian/ bookworm-backports main non-free non-free-firmware contrib" >> /etc/apt/sources.list \
    echo "deb-src https://mirrors.tencent.com/debian/ bookworm-backports main non-free non-free-firmware contrib" >> /etc/apt/sources.list

RUN mkdir ~/.pip && \
    echo "[global]\nindex-url = http://mirrors.tencent.com/pypi/simple/\ntrusted-host = mirrors.tencent.com" > ~/.pip/pip.conf

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ libc-dev libffi-dev libgmp-dev libmpfr-dev libmpc-dev pkg-config libmysqlclient-dev

COPY requirements.txt /requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --prefix=/pkg -r requirements.txt

# production stage
FROM base AS production

ENV EDITION SELF_HOSTED
ENV DEPLOY_ENV PRODUCTION
ENV CONSOLE_API_URL http://127.0.0.1:5001
ENV CONSOLE_WEB_URL http://127.0.0.1:3000
ENV SERVICE_API_URL http://127.0.0.1:5001
ENV APP_WEB_URL http://127.0.0.1:3000

EXPOSE 5001

# set timezone
ENV TZ UTC

WORKDIR /app/api

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl wget vim nodejs ffmpeg libgmp-dev libmpfr-dev libmpc-dev \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

COPY --from=packages /pkg /usr/local
COPY . /app/api/

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ARG COMMIT_SHA
ENV COMMIT_SHA ${COMMIT_SHA}

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]