import sys
import smtplib
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

import pandas as pd


# get arguments
sender_email = sys.argv[1]
sender_password = sys.argv[2]
receiver_emails = [addr for addr in sys.argv[3:]]

# set port for gmx.net
port = 465

# set defaul ssl context
context = ssl.create_default_context()

# create message
timestamp = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = sender_email
msg['Subject'] = 'Aktueller Stand Golfkasse ' + timestamp

# email text
df = pd.read_csv('golfkasse.csv')
dic = {'Marcel':0, 'Felix':0, 'Flo':0}
for key in dic.keys():
    dic[key] = df.iloc[(df['name'] == key).values,2].sum()

body = 'Guten Morgen!\n\nAktuell verteilen sich die'
body += ' {:.2f}€ in der Golfkasse wie folgt:\n'.format(
    round(sum(dic.values()), 2))

a = ''
for key in dic.keys():
    a += '    ' + key + ': ' + '{:.2f}'.format(dic[key]) + '€\n'
body += a + '\nMit freundlichen Grüßen\nGolfKassenOverview'

msg.attach(MIMEText(body, 'plain'))

# send mail
with smtplib.SMTP_SSL('mail.gmx.net', port, context=context) as server:
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_emails, msg.as_string())
