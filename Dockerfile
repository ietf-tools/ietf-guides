FROM opensuse/leap

RUN zypper -n update

RUN zypper -n install \
        apache2 \
        apache2-devel \
        gcc \
        gcc-c++ \
        mysql-client \
        python2 \
        python2-devel \
        python2-mysqlclient \
        python2-pip \
        sqlite3 \
        sudo

RUN update-alternatives --install /usr/bin/python python /usr/bin/python2 5

EXPOSE 8002:8002

RUN mkdir /code
WORKDIR /code
COPY --chown=wwwrun:www . /code/

RUN mkdir /code/logs
RUN chown wwwrun:www /code/logs

RUN pip install -r requirements.txt

RUN echo "import os" > ietf_guides/settings/local.py
RUN echo "BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))" >> ietf_guides/settings/local.py
RUN echo "SECRET_KEY='garbage'" >> ietf_guides/settings/local.py
RUN echo "DATABASES = {" >> ietf_guides/settings/local.py
RUN echo "    'default': {" >> ietf_guides/settings/local.py
RUN echo "        'ENGINE': 'django.db.backends.sqlite3'," >> ietf_guides/settings/local.py
RUN echo "        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')," >> ietf_guides/settings/local.py
RUN echo "    }" >> ietf_guides/settings/local.py
RUN echo "}" >> ietf_guides/settings/local.py

RUN echo "DB_PASSWORD='garbage'" >> ietf_guides/settings/secrets.py

ENV DJANGO_SETTINGS_MODULE=ietf_guides.settings.prod
RUN ./manage.py runmodwsgi --setup-only --port 8002 --user wwwrun --group www --access-log --server-root /code/mod_wsgi-express-8002 --log-directory /code/logs
RUN rm ietf_guides/settings/local.py

ENTRYPOINT ./docker-entry.sh

