invar
=====

Scripts for generating tiles from `Mapnik <http://mapnik.org/>`_ configuration.

invar is named after a `metal alloy <http://en.wikipedia.org/wiki/Invar>`_ frequently used in leveling rods and survey tapes.

Installation
============

invar only works with Mapnik2. Instructions for installing Mapnik2 can be found `here <http://trac.mapnik.org/wiki/Mapnik2>`_. Once you have Mapnik2 installed you can install invar using pip::

    pip install invar

It can be quite tricky to get Mapnik2 working within virtualenv, so it may be better to install invar in the global site-packages.

Usage
=====

**ivtile**

invar tiler sample usage::

    ivtile map.xml output_directory 32.4419 -95.393 32.2307 -95.301 10 16 2

Details of each parameter are available via::

    ivtile -h

**ivframe**

invar framer rendering a single frame::

    ivframe map.xml output_directory 32.351 -95.301

    
invar framer rendering a series frames from latitude/longitude pairs in a CSV file::

    ivframe map.xml output_directory --csv data.csv --name name_column

Details of each parameter are available via::

    ivframe -h

**Using with TileMill**

In order to use invar with TileMill you need to convert TileMill's .mml configuration and .mss styles into a Mapnik .xml file. Here is an example of how this might work::

    tilemill/bin/node tilemill/bin/carto map.mml > map.xml

Credits
=======

**Open Street Map**

Much of this application is derived from selections of the Open Street Map project--notably `generate_tiles.py <http://svn.openstreetmap.org/applications/rendering/mapnik/generate_tiles.py>`_.

**Authors**

* Christopher Groskopf (`@onxyfish <http://twitter.com/onyxfish>`_)

License
=======

MIT
