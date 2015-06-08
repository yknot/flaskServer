#flaskServer

This is a flask server that runs on a heroku app. There is a tasks API at /api

##Tasks
###Inventory
* Multiple Inventories
* Designed for food inventories but can be modified in the future
* Functions
	* Create inventory
	* Create items
	* Read inventories
	* Update items
	* Delete items
	* Delete inventories
* Inventory attributes
	* id (auto generated PK)
	* name
* Item attributes (more can be added)
	* id (auto generated PK)
	* name
	* quantity (nullable)
	* purchaseDate (nullable)
	* expirationDate (nullable)
	* purchasePrice (nullable)

	
##Clients
###APIInterface.py
* Python command line interface for interacting with the API
* Simple text outputs and prints in JSON
* For testing purpsoes

###Android App...
* In Developement


##File structure


	/flaskApp/
		/static/ - Will hold css and static images 
		/templates/ - Holds template webpages like the splash page 
			index.html
		/views - Holds the views for the api
			/__init__.py
				import views
				routes to / and /api
			/inventory.py
				select * - GET /api/inventory
				insert - POST /api/inventory
				delete - DELETE /api/inventory/<name>
			/item.py
				select * - GET /api/inventory/<name>
				select 1 - GET /api/inventory/<name>/<int:item_id>
				insert/update - POST /api/inventory/<name>
				delete - DELETE /api/inventory/<name>/<int:item_id>
		/__init__.py
			create flask app
			imports
			error handlers
		/models.py - Holds the database models for the api
			date serializer
			define inventory
				serializer
			define item
				serializer
	/config.py - Config for production (overwritten by instance folder on dev)
	/Procfile - Startup file for heroku
	/README.md - Documentation
	/requirements.txt - python requirements
	/run.py - runs the app
	/shell.py - runs a shell with the app imported
	/APIinterface.py - python CLI for the api
