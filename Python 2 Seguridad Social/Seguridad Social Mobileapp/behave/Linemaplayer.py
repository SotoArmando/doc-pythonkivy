from kivy.graphics.context_instructions import Translate, Scale
from kivy.graphics import Color, Line
from kivy.garden.mapview import MapLayer

class LineMapLayer(MapLayer):
    def __init__(self, **kwargs):
        super(LineMapLayer, self).__init__(**kwargs)
        self.zoom = 0

    def reposition(self):
        mapview = self.parent

        #: Must redraw when the zoom changes 
        #: as the scatter transform resets for the new tiles
        if (self.zoom != mapview.zoom):
            self.draw_line()

    def draw_line(self, *args):
        mapview = self.parent
        self.zoom = mapview.zoom
        geo_dover   = [51.126251, 1.327067]
        geo_calais  = [50.959086, 1.827652]
        screen_dover  = mapview.get_window_xy_from(geo_dover[0], geo_dover[1], mapview.zoom)
        screen_calais = mapview.get_window_xy_from(geo_calais[0], geo_calais[1], mapview.zoom)

        # When zooming we must undo the current scatter transform
        # or the animation makes the line misplaced
        scatter = mapview._scatter
        x,y,s = scatter.x, scatter.y, scatter.scale
        point_list    = [ screen_dover[0], screen_dover[1], 
                                            screen_calais[0], screen_calais[1] ]

        with self.canvas:
            self.canvas.clear()
            Scale(1/s,1/s,1)
            Translate(-x,-y)
            Color(0, 0, 0, .6)
            Line(points=point_list, width=3, joint="bevel")