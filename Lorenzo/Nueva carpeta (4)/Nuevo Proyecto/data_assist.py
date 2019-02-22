#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
patch = os.path.dirname(os.path.abspath(__file__))

class Asistente():
    def __init__(self,**kwargs):
        self.data = []
        try:
            self.R_Data()
        except:
            pass
        
    def W_Dato(self,a,b,c,d,e,f):
        nuevoreg = {}
        nuevoreg['ID'] = a
        nuevoreg['Cliente'] = b
        nuevoreg['Total'] = c
        nuevoreg['Fecha'] = d
        nuevoreg['Descuento'] = e
        nuevoreg['Subtotal'] = f
        self.data.append(nuevoreg)
    
    def R_Data(self):
        file = open(patch+'/data.rec','r')
        data = []
        try:
            exec('data[:]='+file.read())
        except:
            pass
        file.close()
        self.data = data
        return data
        
    def S_Data(self):
        file = open(patch+'/data.rec','w')
        file.write(str(self.data))
        file.close()
        


