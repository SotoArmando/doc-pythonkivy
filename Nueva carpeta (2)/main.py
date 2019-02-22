import numpy
int(raw_input('Valor de m:'))
int(raw_input('Valor de n:'))
matrix = numpy.zeros((m,n))
= numpy.zeros((n))
x=numpy.zeros((m))
print 'Introduce la matriz de coeficientes y el vector solución'
for r in range():
    for c in range():
        matrix[(r),(c)]=(raw_input("Elemento a[] "))
        vector[(r)]=(raw_input('b[]: '))
        print(matrix)


for r in range(k+1,m):
    factor=(matrix[r,k]/matrix[k,k])
    vector[r]=vector[r]-(factor*vector[k])
        for c in range(0,n):
            matrix[r,c]=matrix[r,c]-(factor*matrix[k,c])

#sustitución hacia atrás
x[]=vector[m-1]/matrix[]
print x[]

for r in range():

for c in range(0,n):
suma=suma+matrix[r,c]*x[c]
x[]=(vector[r]-suma)/matrix[]

print 'Resultado matriz'
print()
print 'Resultado del vector'
print()
print 'Resultados: '
print()
