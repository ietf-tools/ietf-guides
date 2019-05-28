# ietf-guides
A small django project to help match IETF guide program guides to participants

## setup for a development environment
* check out a working copy
* create and activate a python2.7 virtualenv
  - virtualenv .
  - . bin/activate
  - pip install -r requirements.txt
* set up a database and a user that has all privileges with it.
* create ietf_guides/settings/local.py and add values for
  - SECRET_KEY   (this is the usual django SECRET_KEY)
  - HASHSALT     (some short string - see guides/utils.py for how this is used)
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

## dummy data
running ./manage.py make_dummy_data will create ten guides and ten participants with field values populated by Faker.
