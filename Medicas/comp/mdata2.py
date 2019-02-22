#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib2
import pprint

class Asistente():
    def __init__(self, **kwargs):
        pass

    def returngeo(self,longlat1,longlat2):
        RP = []
        for i in range(2):
            longlat1[i] = str(longlat1[i])
            longlat2[i] = str(longlat2[i])
        mapboxurl ="https://api.mapbox.com/directions/v5/mapbox/driving/"
        maproutes = longlat1[0]+"%2C"+longlat1[1]+"%3B"+longlat2[0]+"%2C"+longlat2[1]
        maphead = ".json?access_token=pk.eyJ1IjoibWFjYXR1cyIsImEiOiJjaXlubGRkdXAwMDJ1MzNwZjdwanhkdnd6In0.eYV9WVlCsI44Ku0HSup7Pg&geometries=geojson"
        url = mapboxurl + maproutes + maphead
        for i in range(10):
            try:
                result = json.load(urllib2.urlopen(url))
                break
            except:
                pass
            
            
        result = result['routes'][0]['geometry']['coordinates']  
        return result


