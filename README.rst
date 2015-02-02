
=========
Smugglers
=========

Installation
---------------------

requirements for psql:

- postgis
- binutils
- libproj-dev
- gdal-bin
- postgresql-9.3-postgis-2.1

create db

.. code-block:: bash

	$ createdb  <db name>
	$ psql <db name>
	> CREATE EXTENSION postgis;
	> CREATE EXTENSION postgis_topology;

django settings

.. code-block:: python

	'ENGINE': 'django.contrib.gis.db.backends.postgis',