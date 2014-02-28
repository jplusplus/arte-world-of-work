# Makefile -- Arte World of Work

VIRTUALENV = venv/

run:
	. $(VIRTUALENV)bin/activate ; export PYTHONPATH=`pwd`/app/:$(PYTHONPATH) ; python -W ignore::DeprecationWarning manage.py runserver 0.0.0.0:8000

install: create_virtualenv pip_install setup_db setup_statics setup_selenium	

create_virtualenv:
	# if venv folder is not created yet we do it
	if [ ! -d venv ]; then virtualenv venv --no-site-packages --distribute --prompt=Arte-WoW; fi

messages: sync_db_translations makemessages

sync_db_translations:
	. $(VIRTUALENV)bin/activate; django-admin.py sync_db_translations 

makemessages:
	. $(VIRTUALENV)bin/activate; cd app; django-admin.py makemessages -a --settings=settings

createsuperuser:
	. $(VIRTUALENV)bin/activate; python manage.py createsuperuser --username root

setup_statics:
	. $(VIRTUALENV)bin/activate; python manage.py compress --force
	ln -sfT `pwd`/app/static/arte_ww/img/ ./app/staticfiles/CACHE/img

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

test_django_app: . $(VIRTUALENV)bin/activate; python manage.py test --settings=app.settings_tests

test_translations:
	. $(VIRTUALENV)bin/activate; django-admin.py test app.translations.tests --settings=app.translations.settings

# EOF
