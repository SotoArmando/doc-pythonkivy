
#programa 3
def secuencia2(N):
    c = 1
    resultado = [N]
    while True:
        x = int(resultado[-1:][0])
        if x%2 == 0:
            r = x / 2
            resultado.append(r)
        if x%2 != 0:
            r = (3*x) + 1
            resultado.append(r)
        if r == 1:
            break
    return resultado
data = []
for i in range(1000):
    x = secuencia2(i+1)
    data.append(len(x))
    print "puesto No.", i+1, len(x)

print "el ganador es el puesto",data.index(max(data))+1," con ",max(data)," elementos"
