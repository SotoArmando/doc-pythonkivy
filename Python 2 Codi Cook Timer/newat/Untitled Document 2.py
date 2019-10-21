

960 x 720 dp --- 2	-  xhdpi 320pi
640 x 480 dp --- 1.5	-  hdpi  240pi
470 x 320 dp --- 1	-  mdpi  160pi
426 x 320 dp --- 0.75	-  ldpi  120pi

KIVY_DPI=320 KIVY_METRICS_DENSITY=2 python main.py --size 720x960
KIVY_DPI=240 KIVY_METRICS_DENSITY=1.5 python main.py --size 480x640
KIVY_DPI=160 KIVY_METRICS_DENSITY=1 python main.py --size 320x470
KIVY_DPI=120 KIVY_METRICS_DENSITY=0.75 python main.py --size 320x426

set KIVY_METRICS_DENSITY=1 
set KIVY_DPI=160
set KIVY_METRICS_FONTSCALE=1