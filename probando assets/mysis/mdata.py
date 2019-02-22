#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib2
import requests

class Asistente():
    def __init__(self, **kwargs):
        self.url = ""
        self.tables = []
        self.tables_data = []
        self.current_data = None
        self.last_id = 0
    def seturl(self, URL):
        self.url = URL
        response = self.requesturl()
        for i in response:
            self.tables.append(i)
            print "Tabla encontrada", i
        print "Actualizando Datos Temporales."
        self.returndata()

    def requesturl(self):
        result = json.load(urllib2.urlopen(self.url))
        return result

    def requestdata(self, tabla):
        result = json.load(urllib2.urlopen(self.url + tabla))
        return result

    def returndata(self):

        for i in self.tables:
            if self.url[-1] == "/":
                print "La URL no tiene problemas."
                pass
            else:
                print self.url, "Formateando URL."
                self.url += "/"
                print self.url, "Formato completado."
            result = self.requestdata(i)
            campos = []
            

            for i in result[0].keys():
                campos.append(i)
            RP = [result, campos]
            self.tables_data.append(RP)


    def returntables(self):
        RP = [self.tables, ]
        return self.tables

    def returncampos(self,tablesIndex):
        return self.tables_data[tablesIndex][1]

    def buscar(self, tablesIndex, tablesIndex2, ValorY):
        for i in self.tables_data[tablesIndex][0]:
            Campo = str(self.tables_data[tablesIndex][1][tablesIndex2])
            print ("Indice de tabla")
            print (self.tables_data[tablesIndex][1])
            ValorX = i[Campo]
            if (ValorX == ValorY) == True:
                return [ValorX == ValorY,i]
    def put(self,tablaid,newdata):
        url = self.url + tablaid + "/"
        print url
        
        json_obj = urllib2.urlopen(url)
        Datos_Tabla = json.load(json_obj)
        data = newdata

        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        req.get_method = lambda: 'PUT'
        response = urllib2.urlopen(req, json.dumps(data))
            
    def buscar1(self, tablesIndex, tablesIndex2, ValorY):
        for i in self.tables_data[tablesIndex][0]:
            Campo = str(self.tables_data[tablesIndex][1][tablesIndex2])
            print ("Indice de tabla")
            print (self.tables_data[tablesIndex][1])
            ValorX = i[Campo]
            from django.contrib.auth.hashers import check_password, make_password
            from django.conf import settings
            
            try:
                settings.configure()
            except:
                pass
            print ValorX, ValorY
            if (check_password(ValorY,ValorX)) == True:
                print "USUARIO CORRECTO"
                return (check_password(ValorY,ValorX),i)

    def filtrar(self, tablesIndex, CampoX, ValorY):
        datos = []
        for i in self.tables_data[tablesIndex][0]:
            Campo = CampoX
            print ("Indice de tabla")
            print (self.tables_data[tablesIndex][1])
            ValorX = str(i[Campo])
            try:
                ValorX.index(ValorY)
                datos.append(i)
            except:
                pass
        return datos
                

    def actualizar(self, tablesIndex):
        if self.url[len(self.url) - 1] == "/":
            print "La URL no tiene problemas."
            pass
        else:
            print self.url, "Formateando URL."
            self.url += "/"
            print self.url, "Formato completado."
        result = self.requestdata(self.tables[tablesIndex])
        campos = []

        for i in result[0]:
            campos.append(i)
        RP = [result, campos]
        self.tables_data[tablesIndex] = RP

    def insertar(self, tablesIndex, ValorY):

        print "La tabla tiene", len(self.tables_data[tablesIndex][1]),"campos"
        print "La tabla tiene", len(self.tables_data[tablesIndex][0]),"Registros"
        registro = {}
        for i in self.tables_data[tablesIndex][1]:
            if i == "id":
                registro[str(i)] = len(self.tables_data[tablesIndex][0]) + 1
            else:
                try:
                    print i, ValorY[i]
                    registro[str(i)] = ValorY[i]
                except:
                    print("Asegurese de usar los Campos correspondientes.")
        registro = json.dumps(registro)
      
        print registro
        urlreq = self.url + self.tables[tablesIndex] + "/"
        print urlreq
        #req = urllib2.Request(urlreq)
        #req.add_header('Content-Type', 'application/json')
        #response = urllib2.urlopen(req, json.dumps(registro))
        req = urllib2.Request(urlreq)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, registro)
        self.actualizar(tablesIndex)

    def returntablesdata(self):
        return self.tables_data



Armando = Asistente()
Armando.seturl("http://127.0.0.1:8000/Router/")
Campos = Armando.returncampos(2)
#for i in Campos:
#    print i
#Armando.insertar(2,"ProbandoX")

