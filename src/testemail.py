import smtplib, ssl



def sendscript(message, reciever_email):

	port = 465 
	password ="HackAZ2020"

	context = ssl.create_default_context()
	sender_email = "hackdaj@gmail.com"

	with smtplib.SMTP_SSL("smtp.gmail.com", port, context = context) as server:
		server.login("hackdaj@gmail.com", password)
		server.sendmail(sender_email, reciever_email, message)
	


