#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 
 

class Asistente():
    def __init__(self, **kwargs):

        self.msg = MIMEMultipart()

    def enviar(self,**kwargs):

        
        fromaddr = "armando29@live.com"
        toaddr = "armando29@live.com"
        body = "PRUEBA"
        self.msg.attach(MIMEText(body, 'plain'))
         
        self.msg['From'] = fromaddr
        self.msg['To'] = toaddr
        self.msg['Subject'] = "SUBJECT OF THE MAIL"
         
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "76468674a1s2")
        text = self.msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        

armando = Asistente()
armando.enviar()