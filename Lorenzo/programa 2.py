
#programa 2
def secuencia(N):
    y = (N*(N+1))/2
    resultado = []
    num = y/2
    R = num*2
    
    for i in range(R):
        if (y % (i+1)) == 0:
            resultado.append(i+1)
    if resultado[-1:][0] != y:
        resultado.append(y)
    return resultado
c = 1
while True:
    c += 1
    print len(secuencia(c))
    if len(secuencia(c)) >= 100:
        print secuencia(c), c, "GANADOR"
        break

    

