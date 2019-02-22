import openpyxl

wb = openpyxl.load_workbook('PRUEBA.xlsx')
sheet = wb.get_sheet_by_name('Hoja1')
countyData = {}

print('Reading rows...')
data = []
letters = ['A','B','C','D','E','F','G','H','I','J',]
campos = []
for row in range(1, sheet.max_row + 1):
    if row == 1:
        for letter in letters:
            campos.append(sheet[letter + str(row)].value)
    else:
        n = {}
        for letter in letters:
            x = sheet[letter + str(row)].value
            if type(x) is long:
                x = int(x)
                print x
            n[campos[letters.index(letter)]] = x
        data.append(n)

for i in data: print i
