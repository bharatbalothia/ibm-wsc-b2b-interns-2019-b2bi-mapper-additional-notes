# Additional Notes Usage Report
import smtplib
import mimetypes
import couchdb
import csv
import datetime
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from itertools import groupby
import os

couch = couchdb.Server("http://admin:admin123@9.199.145.193:5984/")
sorted_record = []
db = couch['additionalnotes']
month_ago=datetime.datetime.now().month-1
path="/tmp"
os.chdir(path)

for docid in db.view('_all_docs'):
    i = docid['id']
    for j in range(0,len(db[i]['usage'])):
        check_date=datetime.datetime.strptime(db[i]['usage'][j]['time'],'%Y/%m/%d %H:%M:%S')
        #sorted_record.append({"username": db[i]['username'],"email": db[i]['email'],"fileName": db[i]['usage'][j]['fileName'],"time": db[i]['usage'][j]['time']})
        if month_ago == check_date.month :
         sorted_record.append({"Employee Name": db[i]['username'],"IBM Internet ID": db[i]['email'],"Map Name": db[i]['usage'][j]['fileName'],"Time of Execution": db[i]['usage'][j]['time']})
a=[]
b=[]
sorted_record=sorted(sorted_record,key=lambda k: k['Employee Name'])
for k,v in groupby(sorted_record,key=lambda x:x['IBM Internet ID']):
    a.append(list(v))
for i in range(0,len(a)):
    b.append(sorted(a[i], key=lambda k: k['Time of Execution']))
# b[0][2]
Date = datetime.datetime.now().strftime("%Y-%m-%d")
fileToSend = "AN-UsageReport-"+Date+".csv"
with open(fileToSend, 'w',newline='') as csvfile:
    fieldnames = ['Employee Name','IBM Internet ID','Map Name','Time of Execution']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(0,len(b)):  
      for j in range(0,len(b[i])):
        writer.writerow({"Employee Name": b[i][j]['Employee Name'],"IBM Internet ID": b[i][j]['IBM Internet ID'],"Map Name": b[i][j]['Map Name'],"Time of Execution": b[i][j]['Time of Execution']})

emailfrom = "smanjit@in.ibm.com"
emailto = "smanjit@in.ibm.com"
#emailto = "Vidhya.Balasubramanian@in.ibm.com"
#emailcc=["tavinod@in.ibm.com","harikrishna.kothamasam@in.ibm.com","smanjit@in.ibm.com"]
emailcc=["smanjit@in.ibm.com"]

msg = MIMEMultipart()
msg["From"] = emailfrom
msg["To"] = emailto
msg["cc"] = ",".join(emailcc)
emailto=[emailto]+emailcc
msg["Subject"] = "Additional Notes Usage Report " +Date
msg.preamble = "Attachment sent using python"

ctype, encoding = mimetypes.guess_type(fileToSend)
if ctype is None or encoding is not None:
    ctype = "application/octet-stream"

maintype, subtype = ctype.split("/", 1)

fp = open(fileToSend, "rb")
attachment = MIMEBase(maintype, subtype)
attachment.set_payload(fp.read())
fp.close()
encoders.encode_base64(attachment)
attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
msg.attach(attachment)

server = smtplib.SMTP('localhost',587)
server.sendmail(emailfrom, emailto, msg.as_string())
server.quit()
