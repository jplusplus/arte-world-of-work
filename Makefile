# Makefile -- Arte World of Work

VIRTUALENV = venv/

run: npm_install pip_install
	. $(VIRTUALENV)bin/activate ; export PYTHONPATH=`pwd`/app/:$(PYTHONPATH) ; python -W ignore::DeprecationWarning manage.py runserver

install: npm_install create_virtualenv pip_install setup_db

create_virtualenv:
	# if venv folder is not created yet we do it
	if [ ! -d venv ]; then virtualenv venv --no-site-packages --distribute --prompt=Arte-WoW; fi

setup_db:
	# setup database
	. $(VIRTUALENV)bin/activate; python manage.py syncdb

npm_install:
	# Install npm packages
	if [ -s npm_requirements.txt ]; then xargs -a npm_requirements.txt npm install -g; else echo '\nNo NPM dependencies found in npm_requirements.txt'; fi

pip_install:
	# Install pip packages
	. $(VIRTUALENV)bin/activate; pip install -r requirements.txt

# EOF
