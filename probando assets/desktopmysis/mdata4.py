#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 
 

class Asistente():
    def __init__(self, **kwargs):

        self.msg = MIMEMultipart()

    def enviar(self,**kwargs):
        self.msg['From'] = fromaddr
        self.msg['To'] = toaddr
        self.msg['Subject'] = "SUBJECT OF THE MAIL"
        
        fromaddr = "RAG_TIRE@noreply.com"
        toaddr = "ADDRESS YOU WANT TO SEND TO"
        body = "YOUR MESSAGE HERE"
        self.msg.attach(MIMEText(body, 'plain'))
         
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "YOUR PASSWORD")
        text = self.msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        

