# Makefile -- Arte World of Work

VIRTUALENV = venv/

run:
	. $(VIRTUALENV)bin/activate ; export PYTHONPATH=`pwd`/app/:$(PYTHONPATH) ; python -W ignore::DeprecationWarning manage.py runserver --nothreading

install:
	virtualenv venv --no-site-packages --distribute --prompt=Detective.io
	# Install pip packages
	. $(VIRTUALENV)bin/activate; pip install -r requirements.txt
	# Install npm packages
	cat npm_requirements.txt | echo $1

# EOF