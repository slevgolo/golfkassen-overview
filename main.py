print('Start importing modules...')
import sys
import smtplib
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

print('Read arguments...')
# get arguments
sender_email = sys.argv[1]
sender_password = sys.argv[2]
receiver_emails = [addr for addr in sys.argv[3:]]

# set port for gmx.net
port = 465

# set defaul ssl context
context = ssl.create_default_context()

print('Create message')
# create message
datestamp = datetime.now().strftime("%d-%b-%Y")
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = sender_email
msg['Subject'] = datestamp + ': Aktueller Stand Golfkasse'

print('Get E-Mail text')
# email text
with open('golfkasse.csv', 'r') as f:
    data = f.read().splitlines()

dic = {'Marcel':0, 'Felix':0, 'Flo':0}
for line in data[1:]:
    split = line.split(',')
    dic[split[1]] += float(split[2])

body = 'Guten Morgen!\n\nAktuell verteilen sich die'
body += ' {:.2f}€ in der Golfkasse wie folgt:\n'.format(
    round(sum(dic.values()), 2))

a = ''
for key in sorted(dic.keys()):
    a += key + ': ' + '{:.2f}'.format(dic[key]) + '€\n'
body += a + '\nMit freundlichen Grüßen\nGolfKassenOverview'

msg.attach(MIMEText(body, 'plain'))

print('Send mail to:')
for receiver_email in receiver_emails:
    print(receiver_email)
    
# send mail
with smtplib.SMTP_SSL('mail.gmx.net', port, context=context) as server:
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_emails, msg.as_string())
