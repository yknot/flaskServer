flaskServer
===========

This is a flask server that runs on a heroku app, used for it's items api. Will interface with android app in the future but for now contains RESTful api at /api.



File structure

	/config.py
	/Procfile
	/requirements.txt
	/run.py
	/shell.py
	/instance.py
		/config.py
	/flaskApp
		/__init__.py
		/models.py
		/views.py
		/static/
		/templates/
			/index.html

File purpose

File  		       | Purpose
---------------- | -------------
config.py        | Contains the configuration for production
Procfile         | Contains the command to run server on production (Heroku specific)
requirements.txt | List of python libraries that need to be installed to run 
run.py           | Use `python run.py` to run locally in dev mode
shell.py         | Run `./shell.py` to enter python shell with all libraries imported
instance         | Local folder not tracked in git for dev configs
flaskApp         | Folder in which the app is located
\_\_init__.py    | Creates app, db connection, and other initilizations
models.py        | Contains database models
views.py         | Provides mapping to apis and template pages
static           | Location of CSS, JS, and images
templates        | Location of template html files like index.html


