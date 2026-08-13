FROM python:3.12-trixie
LABEL maintainer="IETF Tools <tools-discuss@ietf.org>"

# Update system packages
RUN apt-get update \
    && apt-get -qy upgrade \
    && apt-get -y install --no-install-recommends apt-utils dialog locales 2>&1

# Set locale to en_US.UTF-8
RUN echo "LC_ALL=en_US.UTF-8" >> /etc/environment && \
    echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && \
    echo "LANG=en_US.UTF-8" > /etc/locale.conf && \
    dpkg-reconfigure locales && \
    locale-gen en_US.UTF-8 && \
    update-locale LC_ALL en_US.UTF-8

RUN apt-get -y install postgresql-client nginx 2>&1

# The container runs as this unprivileged user rather than root. The uid/gid are
# fixed so bind-mounted volumes and any runAsUser setting can be matched to them.
ARG APP_UID=1000
ARG APP_GID=1000
RUN groupadd --gid ${APP_GID} guides && \
    useradd --uid ${APP_UID} --gid ${APP_GID} --create-home --shell /bin/bash guides

# Adjust nginx for a non-root master process:
#  - the "user" directive only works when the master starts as root, so drop it
#    and let the workers inherit the app user
#  - /run stays root-owned, so the pid file, the gunicorn socket and the access
#    log FIFO all move to a directory the app user owns
#  - nginx cannot reopen /dev/stdout unprivileged (the container's stdout belongs
#    to root), so it writes access logs to a FIFO the entrypoint relays instead
#  - Debian's stock default site is a symlink into root-owned sites-available,
#    which the entrypoint could not overwrite; both entrypoints install their own
RUN sed -i -e '/^user /d' \
           -e 's#^pid .*#pid /run/guides/nginx.pid;#' /etc/nginx/nginx.conf && \
    mkdir -p /run/guides && \
    mkfifo /run/guides/access.log && \
    rm -f /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default && \
    chown -R guides:guides \
        /run/guides \
        /var/lib/nginx \
        /var/log/nginx \
        /etc/nginx/conf.d \
        /etc/nginx/sites-enabled

# An unprivileged process cannot bind port 80, so nginx listens high and the port
# mapping does the rest
EXPOSE 8080/tcp

# Dependencies live in a virtualenv the app user owns, so that pip install works
# without root (the devcontainer re-runs it on create).
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"
RUN python -m venv ${VIRTUAL_ENV}

WORKDIR /code

# Doing this step before copying the whole codebase improves docker's ability to reuse cached layers at build time
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt && chown -R guides:guides ${VIRTUAL_ENV}

COPY --chown=guides:guides . /code/

# Allow mkdir to succeed if directories already exists
RUN mkdir -p /code/logs && \
    mkdir -p /code/static && \
    chown -R guides:guides /code

ENV DJANGO_SETTINGS_MODULE=ietf_guides.settings.prod

# Set HOME explicitly: gunicorn's control server writes to $HOME/.gunicorn, and
# USER alone does not reliably set it.
ENV HOME=/home/guides
USER guides

ENTRYPOINT ./docker-entry.sh

