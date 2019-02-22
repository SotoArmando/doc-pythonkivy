#!/usr/bin/env python
# -*- coding: utf-8 -*-
#nelsonf881.nf@gmail.com
from __init__ import *
C1 = "[color=#13C0C7]"
C2 = "[color=#404040]"
C3 = "[color=#ff3333]"
C4 = "[color=#000000]"
C5 = "[color=#bfbfbf]"

metrics = MetricsBase()
try:
    android_dpi = metrics.dpi_rounded()
except:
    android_dpi = metrics.dpi_rounded
print android_dpi
asset_dpi = [120,160,240,320]
asset_dpi2 = ['ldpi','mdpi','hdpi','xhdpi','xxhdpi','xxxhdpi']
patch = os.path.dirname(os.path.abspath(__file__))

color = patch + '/hud/colors/'
sound = patch + '/sounds/'
font = patch + '/fonts/'
hud = patch + '/hud/'

asset = ''
for i in asset_dpi:
    if android_dpi == i:
        asset = patch + '/asset/drawable-'+str(asset_dpi2[asset_dpi.index(i)])+'/'

Window.clearcolor = (1,1,1,1)
 
Window.size = (360,640)

class InterfaceManager(RelativeLayout):
    def __init__(self, **kwargs):
    
        
