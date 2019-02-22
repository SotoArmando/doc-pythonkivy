personas = 30
nada = 8
lima = 20
naranja = 10

i_lima = []
i_naranja = []
for i in range(personas-nada-lima):
    i_lima.append("0")
for i in range(lima):
    i_lima.append("l")
for i in range(naranja):
    i_naranja.append("n")
for i in range(personas-nada-naranja):
    i_naranja.append("0")

nematodo = 0
for i in range(personas-nada):
    if (i_lima[i] == "l") and (i_naranja[i] == "n"):
        nematodo +=1


print i_lima
print i_naranja
print "nematodos ", nematodo


