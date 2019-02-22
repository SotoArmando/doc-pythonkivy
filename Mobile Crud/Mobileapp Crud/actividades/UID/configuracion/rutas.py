#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
patch = os.path.dirname(os.path.abspath(__file__))
s = len("configuracion") * -1

asset = patch[:s] + 'assets/drawable-mdpi/'
color = patch[:s] + 'colors/'
font = patch[:s] + 'fonts/'