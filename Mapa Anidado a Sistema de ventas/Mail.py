import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import datetime

fp = open('registro.txt')
msg = MIMEText(fp.read())
fp.close()

#msg = MIMEMultipart()
msg['Subject'] = "Constancia de su Aplicacion - " + str(datetime.datetime.now().date())
msg['From'] = "noreplydata4" + '@gmail.com' 
msg['To'] = "armando29@live.com"





print("connecting")
s = smtplib.SMTP('smtp.gmail.com', '587')
s.ehlo()
s.starttls()
s.ehlo()
s.login('noreplydata4@gmail.com' , "76468674764")
print("connected")
s.sendmail("noreplydata4" + '@gmail.com', "armando29@live.com", msg.as_string())
print("sent")
s.quit()