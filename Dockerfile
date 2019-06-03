FROM opensuse/leap

RUN zypper -n update

RUN zypper -n install \
        apache2 \
        apache2-devel \
        gcc \
        gcc-c++ \
        libmysqlclient-devel\
        mysql-client \
        python3 \
        python3-devel \
        python3-mysqlclient \
        python3-pip \
        sqlite3 \
        sudo

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 5

EXPOSE 8002:8002

RUN mkdir /code
WORKDIR /code
COPY --chown=wwwrun:www . /code/

RUN mkdir /code/logs
RUN chown wwwrun:www /code/logs

RUN mkdir /code/static
RUN chown wwwrun:www /code/static

RUN pip install -r requirements.txt

ENTRYPOINT ./docker-entry.sh

