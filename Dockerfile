FROM opensuse/leap

RUN zypper -n update

RUN zypper -n install \
        apache2 \
        apache2-devel \
        bind-utils \
        command-not-found \
        coreutils \
        findutils \
        gcc \
        gcc-c++ \
        iputils \
        less \
        lftp \
        libmysqlclient-devel\
        mysql-client \
        net-tools \
        net-tools-deprecated \
        python3 \
        python3-devel \
        python3-mysqlclient \
        python3-pip \
        rsync\
        sqlite3 \
        sudo \
        vim

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 5

EXPOSE 8002:8002

RUN mkdir /code
WORKDIR /code

# Doing this step before copying the whole codebase improves docker's ability to reuse cached layers at build time
COPY --chown=wwwrun:www ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

COPY --chown=wwwrun:www . /code/

RUN mkdir /code/logs
RUN chown wwwrun:www /code/logs

RUN mkdir /code/static
RUN chown wwwrun:www /code/static

ENTRYPOINT ./docker-entry.sh

