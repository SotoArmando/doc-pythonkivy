from __future__ import division


L = ["X","Y","Z","="]

def IntroducirDatos():
    INX = []
    for i in range(3):
        ARRAY = []
        print("Ecuacion["+str(i+1)+"]")
        for i in range(4):
            print (L[i])+":","",
            try:
                IN = input("")
                ARRAY.append(IN)
            except:
                print("Introdusca el valor adecuadamente")
                IntroducirDatos()
        INX.append(ARRAY)
    return INX

def ImprimirDatos(X):
    for i in X:
        for y in range(len(i)):
            if y == 3:
                print "=","",
                print str(i[y]),"",
            else:
                print str(i[y])+L[y],"",
        print "\n"

"""1) Pasar el sistema de ecuacion a notacion matricial, para si poder asumir los coeficientes respectivos.
ecuacion:           3x + 6y - z = 5
notacion matricial: 3 ,+ 6 ,- 1 , 5
"""


""" Usando la notacion matricial de la funcion el agoritmo puede usar GAUSS para determinar los resultados
por medio del metodo respectivo. """



A = [[1,-1,-1,0],[1,2,-5,2],[3,-2,-4,1]]



def GAUSS(A, m, n):
    """
    Aplica el metodo de eliminacion de Gauss a una matriz 'A', de m filas
    y n columnas. 
    
    Asi la matriz queda en forma triangular donde los elementos debajo de la diagonal principal van a ser cero.
    """



    for i in range(n): 
        for k in range(i + 1, n):
            p = -A[k][i] / A[i][i]
            for j in range(i, n + 1):
                if (i == j):
                    A[k][j] = 0
                else:
                    A[k][j] = A[k][j] + p * A[i][j]

                    

        """
        Expreciones usadas para los elementos de la diagonal.
        f2 = f2 - (2*f1)
        f3 = f3 - (3*f1)
        """
        




def Forma_Escalonada(A, m, n):
        

    """
    Una vez tenemos la medida de los resultados y su forma triangular.
    Solo queda transformar la matriz aumentada en una matriz en forma escalonada.
    """

    for i in range(n - 1, -1, -1):
        for k in range(i - 1, -1, -1):
            if (A[i][i] == 0):
                p = A[i][i]
            else:
                p = -A[k][i] / A[i][i]
            for j in range(i, -2, -1):
                if (i == j):
                    A[k][j] = 0
                else:
                    A[k][j] = A[k][j] + p * A[i][j]
    for i in range(m):
        for j in range(n):
            if (A[i][j] != 0 and A[i][j] != 1):
                t = A[i][j]
                for k in range(0, n + 1):
                    A[i][k] = A[i][k] / t
            
    for i in range(0,n):
        print "Solucion ["+L[i]+"]:", A[i][n]




def main():
        try:
            A = IntroducirDatos()
            ImprimirDatos(A)
            GAUSS(A,3,3)
            Forma_Escalonada(A,3,3)
        except:
            print("Introdusca datos apropiadamente. Verifique e intente denuevo.")
            main()

        
        

main()

