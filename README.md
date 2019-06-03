# ietf-guides
A small django project to help match IETF guide program guides to participants

## setup for a development environment
* check out a working copy
* create and activate a python3 virtualenv
  - virtualenv --python=python 3 .
  - . bin/activate
  - pip install -r requirements.txt
* set up a database and a user that has all privileges with it.
* create ietf_guides/settings/local.py and add values for
  - SECRET_KEY   (this is the usual django SECRET_KEY)
  - HASHSALT     (some short string - see guides/utils.py for how this is used)
  - DEFAULT_FROM_EMAIL
  - DATABASES    (a dict matching the database you set up above)
```
Some possible DATABASE dicts:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASES = {
    'default': {
        'NAME': 'ietf_guides',
        'ENGINE': 'django.db.backends.mysql',
        'USER': <your db user>,
        'PASSWORD': <your db password>,
        'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
    },
}
```
* export which settings you want to use as DJANGO_SETTINGS_MODULE (e.g. ietf_guides.settings.dev) or supply settings on the command line as necessary
* ./manage.py migrate
* ./manage.py test --settings=ietf_guides.settings.test
* ./manage.py createsuperuser

## Running a prebuilt image under docker
* set up a database and a user that has all privileges with it
* create a run directory outside any clone of the source
* create a local.py in that directory as above
* start the most recent image from <https://cloud.docker.com/u/ietf/repository/docker/ietf/ietf_guides> mapping your local.py and possibly your database socket into the container using a command similar to:
```
docker run -it -v ${PWD}/logs:/code/logs -v ${PWD}/local.py:/code/ietf_guides/settings/local.py -p 8002:8002 --name ietf_guides ietf/ietf_guides:v0.9.1

or perhaps

docker run -it -v ${PWD}/logs:/code/logs -v ${PWD}/secrets/local.py:/code/ietf_guides/settings/local.py -v /var/run/mysql:/var/run/mysql -p 8002:8002 --name ietf_guides ietf/ietf_guides:v0.9.1
```
The website will then be exposed at http://localhost:8002

## dummy data
running ./manage.py make_dummy_data will create ten guides and ten participants with field values populated by Faker.
