#!/usr/bin/env python

import json
import multiprocessing
import os
import Queue

import mapnik

import constants
import projections

class Renderer(multiprocessing.Process):
    """
    A Mapnik renderer process.
    """
    def __init__(self, tile_queues, config, width=constants.DEFAULT_WIDTH, height=constants.DEFAULT_HEIGHT, filetype=constants.DEFAULT_FILE_TYPE, buffer_size=None, skip_existing=False):
        multiprocessing.Process.__init__(self)

        self.config = config
        self.tile_queues = tile_queues
        self.width = width
        self.height = height
        self.buffer_size = buffer_size if buffer_size else max(width, height)
        self.filetype = filetype
        self.skip_existing = skip_existing

    def run(self):
        self.mapnik_map = mapnik.Map(self.width, self.height)
        mapnik.load_map(self.mapnik_map, self.config, True)

        self.map_projection = mapnik.Projection(self.mapnik_map.srs)
        self.tile_projection = projections.GoogleProjection()  

        while True:
            tile_parameters = None

            # Try to fetch a tile from any queue
            for tile_queue in self.tile_queues:
                try:
                    tile_parameters = tile_queue.get_nowait()
                    break 
                except Queue.Empty:
                    pass

            # Couldn't get tile parameters from any queue--all done
            if not tile_parameters:
                return

            # Skip rendering existing tiles
            if self.skip_existing:
                filename = tile_parameters[0]

                if os.path.exists(filename):
                    print 'Skipping %s' % (filename)
                    tile_queue.task_done()

                    continue

            self.render(*tile_parameters)
            tile_queue.task_done()

    def render(self):
        """
        Render a segment from the queue. Must be overridden in subclasses.
        """
        raise NotImplementedError('You should not use Renderer directly, but rather one of its subclasses.')

class TileRenderer(Renderer):
    """
    Renderer for tiles. 
    """
    def __init__(self, tile_queues, config, width=constants.DEFAULT_WIDTH, height=constants.DEFAULT_HEIGHT, filetype=constants.DEFAULT_FILE_TYPE, buffer_size=None, skip_existing=False, **kwargs):
        super(TileRenderer, self).__init__(tile_queues, config, width, height, filetype, buffer_size, skip_existing)
        self.grid = kwargs.get('grid', False)
        self.key =  kwargs.get('key', None)
        self.fields =  kwargs.get('fields', None)

    def render(self, filename, tile_x, tile_y, zoom):
        """
        Render a single tile to a given filename.
        """
        print 'Rendering %s' % (filename)

        # Calculate pixel positions of bottom-left & top-right
        half_width = self.width / 2
        half_height = self.height / 2
        px0 = (tile_x * self.width, (tile_y + 1) * self.height)
        px1 = ((tile_x + 1) * self.width, tile_y * self.height)

        # Convert tile coords to LatLng
        ll0 = self.tile_projection.fromPixelToLL(px0, zoom);
        ll1 = self.tile_projection.fromPixelToLL(px1, zoom);
        
        # Convert LatLng to map coords
        c0 = self.map_projection.forward(mapnik.Coord(ll0[0], ll0[1]))
        c1 = self.map_projection.forward(mapnik.Coord(ll1[0], ll1[1]))

        # Create bounding box for the render
        bbox = mapnik.Box2d(c0.x, c0.y, c1.x, c1.y)

        self.mapnik_map.zoom_to_box(bbox)
        self.mapnik_map.buffer_size = self.buffer_size 

        # Render image with default renderer
        image = mapnik.Image(self.width, self.height)
        mapnik.render(self.mapnik_map, image)
        image.save(filename, self.filetype)
        
        if self.grid:
            if self.key:
                grid = mapnik.Grid(self.width, self.height)
            else:
                grid = mapnik.Grid(self.width, self.height, key=self.key)

            fields = []

            if self.fields:
                fields.extend(self.fields)

            mapnik.render_layer(self.mapnik_map,grid,layer=0,fields=fields)
            # then encode the grid array as utf, resample to 1/4 the size, and dump features
            # this comes from https://github.com/springmeyer/gridsforkids/blob/master/generate_tiles.py 
            # with little consideration
            grid_utf = grid.encode('utf', resolution=4, features=True)

            # client code uses jsonp, so fake by wrapping in grid() callback
            base, ext = os.path.splitext(filename)
            grid_filename = '%s.grid.json' % base
            print 'Rendering %s' % (grid_filename)

            with open(grid_filename,'wb') as f:
                f.write('grid(' + json.dumps(grid_utf) + ')')
            
            

class FrameRenderer(Renderer):
    """
    Renderer for frames (centered map fragments).
    """
    def render(self, filename, latitude, longitude, zoom):
        """
        Render a single tile to a given filename.
        """
        print 'Rendering %s' % (filename)
    
        x, y = self.tile_projection.fromLLtoPixel([longitude, latitude], zoom) 

        # Calculate pixel positions of bottom-left & top-right
        half_width = self.width / 2
        half_height = self.height / 2
        px0 = (x - half_width, y + half_height)
        px1 = (x + half_width, y - half_height)

        # Convert tile coords to LatLng
        ll0 = self.tile_projection.fromPixelToLL(px0, zoom);
        ll1 = self.tile_projection.fromPixelToLL(px1, zoom);
        
        # Convert LatLng to map coords
        c0 = self.map_projection.forward(mapnik.Coord(ll0[0], ll0[1]))
        c1 = self.map_projection.forward(mapnik.Coord(ll1[0], ll1[1]))

        # Create bounding box for the render
        bbox = mapnik.Box2d(c0.x, c0.y, c1.x, c1.y)

        self.mapnik_map.zoom_to_box(bbox)
        self.mapnik_map.buffer_size = self.buffer_size

        # Render image with default renderer
        image = mapnik.Image(self.width, self.height)
        mapnik.render(self.mapnik_map, image)
        image.save(filename, self.filetype)

