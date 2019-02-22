def rellenar(self):
    for i in ws:
        print "Linea "+str(linea)
        linea += 1
        columna = 0
        for x in i:
            print "Columna "+str(columna) +" = " + str(x.value)
            columna += 1