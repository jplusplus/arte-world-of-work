# Makefile -- Arte World of Work

VIRTUALENV = venv/

run:
	. $(VIRTUALENV)bin/activate ; export PYTHONPATH=`pwd`/app/:$(PYTHONPATH) ; python -W ignore::DeprecationWarning manage.py runserver

install: create_virtualenv pip_install setup_db setup_selenium

create_virtualenv:
	# if venv folder is not created yet we do it
	if [ ! -d venv ]; then virtualenv venv --no-site-packages --distribute --prompt=Arte-WoW; fi

createsuperuser:
	. $(VIRTUALENV)bin/activate; python manage.py createsuperuser --username root

setup_db:
	# setup database
	. $(VIRTUALENV)bin/activate; python manage.py syncdb --noinput; . $(VIRTUALENV)bin/activate; python manage.py migrate --all

npm_install:
	# Install npm packages
	if [ -s npm_requirements.txt ]; then xargs -a npm_requirements.txt npm install -g; else echo '\nNo NPM dependencies found in npm_requirements.txt'; fi

pip_install:
	# Install pip packages
	. $(VIRTUALENV)bin/activate; pip install -r requirements.txt

test: test_django_app

test_django_app: . $(VIRTUALENV)bin/activate; python manage.py test app.core app.api app.authentication --settings=app.settings_tests

test_translations:
	. $(VIRTUALENV)bin/activate; python manage.py test app.translations.tests --settings=app.translations.tests.settings_tests

# EOF
