
#programa 1
def aumentar(exponente):
    numero = 2
    resultado1 = long(numero**exponente)
    resultado2 = 0
    dim = str(resultado1)
    for i in dim:
        print i
        if (i == '.') or (i == 'e') or (i == '+'): pass
        else: resultado2 += float(i)
        
    return resultado1,resultado2

print aumentar(10)
    
