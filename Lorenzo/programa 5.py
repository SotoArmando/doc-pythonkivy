# -*- coding: cp1252 -*-
lineas  = int(input("cuantas lineas?: "))
i_lineas = []
for i in range(lineas):
    texto = raw_input("introduzca el caso. "+str(i+1)+"\n")
    if len(texto) >= 100000:
        print ("se ha excedido el numero de lineas.")
    else:
        i_lineas.append(texto+" ")



for i in i_lineas:
    familia = [] 
    print " "*3
    print i
    hijos = 0
    
    for x in i:
        if x == '.':
            hijos+=1
        else:
            if hijos == 0: pass
            else:
                familia.append(hijos)
                print hijos
            hijos = 0
            
        if hijos == 0:
            if x == " ": pass
            else: print "familia", x
    x = []
    x1 = []
    x2 = ""
    for i in familia:
        if i == 2: x.append(i)
        elif i >= 3: x2 = "excepcion"
        else: x1.append(i)
    print "------------------"    
    if (len(x) == len(familia)) and (len(x)>=1):
        print ("todos los matrimonios tienen 2 hijos")
    if len(x1) == len(familia): print ("ningún matrimonio tiene más de un hijo")
        
        
    if x2 == "excepcion": print "N"
        

        
        
        
            
    
        
            
    
    



    
    
