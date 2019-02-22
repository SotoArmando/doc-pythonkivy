#!/usr/bin/env python
# -*- coding: utf-8 -*-
Hola = "Hola a todos"

fs_multitexture = '''
$HEADER$

// New uniform that will receive texture at index 1
uniform sampler2D texture1;

void main(void) {

    // multiple current color with both texture (0 and 1).
    // currently, both will use exactly the same texture coordinates.
    gl_FragColor = frag_color * \
        texture2D(texture0, tex_coord0) * \
        texture2D(texture1, tex_coord0);
}
'''

