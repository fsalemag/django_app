FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG USER_ID
ARG GROUP_ID
ARG USER_NAME
ARG GROUP_NAME

RUN groupadd --gid $GROUP_ID $GROUP_NAME; \
    useradd --create-home --no-log-init --uid $USER_ID --gid $GROUP_ID $USER_NAME

EXPOSE 8000

WORKDIR /code
COPY . .

RUN set -eux && \
    apt-get update && \
    apt-get -y install curl && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R $USER_NAME:$GROUP_NAME /vol && \
    chown -R $USER_NAME:$GROUP_NAME /vol/web && \
    chmod -R 755 /vol

USER $USER_NAME
