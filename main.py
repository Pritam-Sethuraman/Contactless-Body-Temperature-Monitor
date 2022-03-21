import RPi.GPIO as gpio
import picamera
import time
 
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from email.mime.image import MIMEImage
 
from smbus2 import SMBus
from mlx90614 import MLX90614
 
fromaddr = "tbot31415@gmail.com"
toaddr = "pronoobkakashi@gmail.com"
 
mail = MIMEMultipart()
 
mail['From'] = fromaddr
mail['To'] = toaddr
mail['Subject'] = "Temperature value exceed alert"
body = "Please find the attached image"
 
data=""
 
def sendMail(data):
    mail.attach(MIMEText(body, 'plain'))
    print data
    dat='%s.jpg'%data
    print dat
    attachment = open(dat, 'rb')
    image=MIMEImage(attachment.read())
    attachment.close()
    mail.attach(image)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "testbot31415")
    text = mail.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
 
def capture_image():
    data= time.strftime("%d_%b_%Y|%H:%M:%S")
    camera.start_preview()
    time.sleep(5)
    print data
    camera.capture('%s.jpg'%data)
    camera.stop_preview()
    time.sleep(1)
    sendMail(data)
 
camera = picamera.PiCamera()
camera.rotation=0
camera.awb_mode= 'auto'
camera.brightness=55
 
while 1:
    bus = SMBus(1)
    sensor = MLX90614(bus, address=0x5A)
    print "Ambient Temperature :", sensor.get_ambient()
    print "Object Temperature :", sensor.get_object_1()
    temp = sensor.get_object_1()
    bus.close()
    if temp>34:
        capture_image()
        time.sleep(0.1)
    else:
        time.sleep(0.01)
