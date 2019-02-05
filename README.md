# ietf-guides
A small django project to help match IETF guide program guides to participants

## setup for a development environment
* check out a working copy
* create and activate a python2.7 virtualenv
* create ietf_guides/settings/secrets.py and add values for
  - SECRET_KEY   (this is the usual django SECRET_KEY)
  - DB_PASSWORD  (see settings/base.py for how this is used)
  - HASHSALT     (some short string - see guides/utils.py for how this is used)
* set up a mysql database and a user that has all privileges with it. It might be easiest at this point to use the database name and user in settings/base.py. If you need to use something different, please extend settings with a local.py (add that to .gitignore) to override base.
* export which settings you want to use as DJANGO_SETTINGS_MODULE (e.g. ietf_guides.settings.dev) or supply settings on the command line as necessary
* ./manage.py migrate
* ./manage.py test --settings=ietf_guides.settings.test
* ./manage.py createsuperuser

## dummy data
running ./manage.py make_dummy_data will create ten guides and ten participants with field values populated by Faker.
