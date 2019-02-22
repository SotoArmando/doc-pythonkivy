import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QLabel
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout,QAbstractItemView, QFrame
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot,Qt
from pyqtgraph import PlotItem
import pyqtgraph as pg
import numpy as np
import datetime
import calendar
from data_assist import Asistente

pg.setConfigOption('background', (244, 244, 244))
pg.setConfigOption('foreground', 'k')
class Ventana(QMainWindow):
    def __init__(self):
            QMainWindow.__init__(self)
            self.datostemporales = {}
            self.datostemporales["facturas"] = []
            uic.loadUi("untitled.ui",self)
            self.tableWidget.setRowCount(100)
            self.datosestaticos = Asistente()
            self.pushButton.clicked.connect(self.agregarfactura)
            self.pushButton_3.clicked.connect(self.guardardatos)
            self.pushButton_2.clicked.connect(self.graficar)
            self.pushButton_4.clicked.connect(self.cargardatos)
            curvePen1 = pg.mkPen(color=(255,255,0), width=2.4)
            curvePen = pg.mkPen(color=(255,0,0), width=2.4)
            self.graph = pg.PlotWidget(self,title = "")

            self.graph.setGeometry(10,330,451,311)
            #self.frame_3 = QFrame(self)
            #self.frame_3.setGeometry(10,330,41,340)
            x = [1,2,3,4,5,6,7,8,9,10,11]
            y = [90000,180000,20000,30000,50000,70000,80000,100000,90000,90000,100000]   
            #self.graph.plotItem.plot(x,y,pen=curvePen)
    ''' def prop(self,y,maxy):
        max_number = max(maxy)
        i_number = max_number
        y_max = max(y)
        i_max = (10**len(str(y_max)))/5
        while True: 
            i_number /= 10
            i_max *= 10
            #print (i_number)
            try: 
                string = str(int(i_number))
            except:
                pass
            print (string,i_max)
            if string[-1:] == '0': pass
            else: break
        n_y = []
        for i in y:
            n_y.append(i*i_max)
        return n_y'''
        
    def graficar(self):
        x = []
        y = []  
        desc_t = 0
        dias = []
        meses = []
        sub_t = []
        sub_tt = 0
        for i in self.datostemporales["facturas"]:
            i_fecha = i[3]
            if len(dias) < 1: dias.append(i[3])
            if len(meses) < 1: dias.append(i[3][2:5])
            for fecha in dias: 
                print (fecha, i_fecha)
                if fecha == (i_fecha):
                    pass
                elif fecha == dias[len(dias)-1]:
                    dias.append(i_fecha)
            
 
            sub_t.append(i[5])
            desc_t += int(i[4])
            x_valor = self.datostemporales["facturas"].index(i)
            y_valor = int(i[5])
            #print (x_valor,y_valor)
            x.append(x_valor)
            y.append(y_valor)
        try:
            desc_p = desc_t/len(self.datostemporales["facturas"])
        except:
            desc_p = desc_t/1
        try:
            cl_semanas = len(self.datostemporales["facturas"]) / ((len(dias))*7)
        except:
            cl_semanas = "sin semanas"
        print ("HOLA"),(len(dias)), "AQUI---------"
        cl_diarios = len(self.datostemporales["facturas"]) / (len(dias))
            
        #print (x)    
        #print (y)    
        for i in sub_t: sub_tt += int(i)
        sub_tt1 = sub_tt /len(dias)
        print (meses)
       
         
        self.label_20.setText(str(int(desc_p)))
        self.label_22.setText(str(len(self.datostemporales["facturas"])))
        self.label_39.setText(str(len(dias)))
        self.label_47.setText(str(int(len(dias)/7)))
        self.label_24.setText(str(int(cl_diarios*7)))
        self.label_26.setText(str(int(cl_diarios)))
        self.label_28.setText(str(int(sub_tt1)))
        self.label_30.setText(str(int(sub_tt)))
        self.label_26.setText(str(int(cl_diarios)))
        
        self.graph.plotItem.clear()
        curvePen = pg.mkPen(color=(255,0,0), width=2.4)
        self.graph.plotItem.plot(x,y,pen=curvePen)
        self.label_41.setText(str(max(y)))
        self.label_43.setText(str(min(y)))
        somedate = datetime.date.today()
        self.label_35.setText(str(somedate))
        somedate = self.add_months(somedate,1)
        self.label_36.setText(str(somedate))
    def guardardatos(self):
        for i in self.datostemporales["facturas"]:
            self.datosestaticos.W_Dato(i[0],i[1],i[2],i[3],i[4],i[5])
            self.datosestaticos.S_Data()
            
        
    def R_Data(self):
        file = open('data.rec','r')
        data = []
        try:
            exec('data='+file.read())
        except:
            pass
        file.close()
        self.data = data
        return data
        
    def cargardatos(self):
        datos = self.datosestaticos.R_Data()
        #exec("datos[:] = " + self.datosestaticos.R_Data())
        
        print (datos)
        for i in datos:
            i_id = len(self.datostemporales["facturas"])
            self.lineEdit.setText(str(i_id+1))
            i_factura = [ i["ID"],
            i["Cliente"],
            i["Total"],
            i["Fecha"],
            i["Descuento"],
            i["Subtotal"]]
            for i in range(6): self.tableWidget.setItem(i_id,i, QTableWidgetItem(str(i_factura[i])))
            self.datostemporales["facturas"].append(i_factura)
            self.lineEdit.setText(str(i_id+2))
            self.tableWidget.scrollToItem(self.tableWidget.selectRow(i_id), QAbstractItemView.PositionAtCenter)

    
        
    def add_months(self,sourcedate,months):
        month = sourcedate.month - 1 + months
        year = int(sourcedate.year + month / 12 )
        month = month % 12 + 1
        day = min(sourcedate.day,calendar.monthrange(year,month)[1])
        return datetime.date(year,month,day)
        
    def agregarfactura(self):
        try:
            i_id = len(self.datostemporales["facturas"])
            self.lineEdit.setText(str(i_id+1))
            i_factura = [self.lineEdit.text(),
            self.lineEdit_2.text(),
            self.lineEdit_3.text(),
            self.lineEdit_4.text(),
            self.lineEdit_5.text(),
            self.lineEdit_6.text()]
            for i in range(6): self.tableWidget.setItem(i_id,i, QTableWidgetItem(str(i_factura[i])))
            self.datostemporales["facturas"].append(i_factura)
            self.lineEdit.setText(str(i_id+2))
            self.tableWidget.scrollToItem(self.tableWidget.selectRow(i_id), QAbstractItemView.PositionAtCenter)
        except:
            pass
    def gen(self):
        print('Hello, World!')
        
app = QApplication(sys.argv)
ventana = Ventana()
ventana.show()
app.exec_()