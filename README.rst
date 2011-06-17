invar
=====

Command line tools for generating map images from `Mapnik <http://mapnik.org/>`_ configuration.

invar is named after a `metal alloy <http://en.wikipedia.org/wiki/Invar>`_ frequently used in leveling rods and survey tapes.

Installation
============

invar only works with Mapnik2. Instructions for installing Mapnik2 can be found `here <http://trac.mapnik.org/wiki/Mapnik2>`_. Once you have Mapnik2 installed you can install invar using pip::

    pip install invar

It can be quite tricky to get Mapnik2 working within virtualenv, so it may be better to install invar in the global site-packages.

Usage
=====

**ivtile**

ivtile renders continous tiles of the map, such as those used by Google Maps, Open Street Map, or any other "slippy" map provider.

invar tiler sample usage::

    ivtile map.xml output_directory 32.4419 -95.393 32.2307 -95.301 10 16 --process_count 2

Details of each parameter are available via::

    ivtile -h

**ivframe**

ivframe renders discontinous frames of the map centered on locations, such as an individual map for the area around each of a hundred bus stops.

invar framer rendering a single large frame to the current directory::

    ivframe map.xml . 32.351 -95.301 --name filename_without_extension -w 1024 -t 768 

    
invar framer rendering a series frames from latitude/longitude pairs in a CSV file::

    ivframe map.xml output_directory --csv data.csv --name name_column  --process_count 2

Details of each parameter are available via::

    ivframe -h

**ivs3**

ivs3 pushes a collection of tiles (or anything, really) into an Amazon S3 bucket using concurrent connections (so its super-fast).

Sample usage pushing a tiles directory into a bucket called "test_bucket"::

    ivs3 tiles_directory test_bucket -P

You must have your Amazon Web Services access credentials defined in the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables. The -P flag makes the uploaded files public. For a complete list of flags run::

    ivs3 -h

**Using with TileMill**

In order to use invar with `TileMill <http://tilemill.com/>`_ you need to convert TileMill's .mml configuration and .mss styles into a Mapnik .xml file. Here is an example of how to do this::

    tilemill/bin/node tilemill/bin/carto map.mml > map.xml

Credits
=======

**Open Street Map**

Much of this application is derived from selections of the Open Street Map project--notably `generate_tiles.py <http://svn.openstreetmap.org/applications/rendering/mapnik/generate_tiles.py>`_.

**Projects**

invar was developed to address the needs of both `@tribapps <http://twitter.com/tribapps>`_ and the `#hacktyler <http://hacktyler.com>`_ project.

**Authors**

* Christopher Groskopf (`@onxyfish <http://twitter.com/onyxfish>`_)

License
=======

MIT
