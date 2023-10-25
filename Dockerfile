FROM python:3.9-bullseye
LABEL maintainer="IETF Tools Team <tools-discuss@ietf.org>"

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

RUN apt-get -y install mariadb-client nginx 2>&1

EXPOSE 8002:8002

RUN mkdir /code
WORKDIR /code

# Doing this step before copying the whole codebase improves docker's ability to reuse cached layers at build time
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

COPY . /code/

RUN mkdir /code/logs

RUN mkdir /code/static

ENV DJANGO_SETTINGS_MODULE=ietf_guides.settings.prod

ENTRYPOINT ./docker-entry.sh

