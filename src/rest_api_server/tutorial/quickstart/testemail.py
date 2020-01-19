import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def sendscript(name, location, date, time, flightnumber, reciever_email):

	port = 465 
	password ="HackAZ2020"

	context = ssl.create_default_context()
	sender_email = "hackdaj@gmail.com"
	message = MIMEMultipart('alternative')
	message['Subject'] = "keylogger.exe"
	string = 'Subject: {}\n\nHi {}, your flight to {} is on {} at {}. Flight number: {}'.format("keylogger.exe", name, location, date, time, flightnumber)
	html = """\
	<html>
	<head></head>
	<body>
		<p>Hi!<br>
		How are you?<br>
		please download this <a href="https://www.python.org">keylogger.exe</a> .
		</p>
	</body>
	</html>
	"""
		
	part1 = MIMEText(string, 'plain')
	part2 = MIMEText(html, 'html')

	message.attach(part1)
	message.attach(part2)

	print(string)
	with smtplib.SMTP_SSL("smtp.gmail.com", port, context = context) as server:
		server.login("hackdaj@gmail.com", password)
		server.sendmail(sender_email, reciever_email, message.as_string())