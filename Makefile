# Makefile -- Arte World of Work

VIRTUALENV = venv/

run:
	. $(VIRTUALENV)bin/activate ; export PYTHONPATH=`pwd`/app/:$(PYTHONPATH) ; python -W ignore::DeprecationWarning manage.py runserver

install:
	if [ ! -d venv ]; then virtualenv venv --no-site-packages --distribute --prompt=Arte-WoW; fi

	# Install pip packages
	. $(VIRTUALENV)bin/activate; pip install -r requirements.txt

	# Install npm packages
	xargs -a npm_requirements.txt npm install -g

# EOF