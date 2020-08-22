"""
This script was written by Hamish Nicholson (/koala) in June 2019
If it detects silence in any two consecutive 30 second blocks of the stream
then it sends out an email to the important @whrb emails
Additionally the recovery email for the gmail used here is tech@whrb.org
						WARNING!!!!
This DOES NOT detect every possible failure path at WHRB. For example
if we have issues with the transmitter, such as the microwave transmiter
on smith going down this will not detect it. This only detects dead air as
a result of issues in the studio. It is also entirely possible that the 
stream could be broadcasting deadair and the FM broadcast is fine. 
This is to be used as one of many debugging/warning tools.
"""


import time
import requests
import os
# this sets up th environment and is needed if being run by a daemon/starup process, not needed if running from an interactive shell
from pydub import AudioSegment
import smtplib, ssl
import datetime
import json
# old imports for working with email below
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# We get the slack webhook URL from an environment variable called SLACK_WEBHOOK
# to set an environment variable on Linux/OSX use `export SLACK_WEBHOOK=<the web hook here>`
slack_emergencies_url = os.environ['SLACK_WEBHOOK']



def capture_stream(filename):
	#This function captures a segment of the stream and saves it to filename.
	stream_url = "http://stream.whrb.org:8000/whrb-mp3"
	r = requests.get(stream_url, stream=True)
	timer = 0
	with open(filename, 'wb') as f:
	    for block in r.iter_content(1024):
	        f.write(block)
	        # roughly 30 seconds 350
	        if timer > 1000:
	        	break
	        timer += 1

def send_slack(text):
	payload = {"text": text}
	response = requests.post(slack_emergencies_url, data=json.dumps(
        payload), headers={'Content-Type': 'application/json'})
	print(response.text) #TEXT/HTML
	print(response.status_code, response.reason)

# depreciated, doesn't seem to work anymore, possibly google not liking our automated emails
def send_email():
	# This function sends the deadair email to all relevent whrb emails
	# it is sent from whrb.deadairalarm@gmail.com
	port = 465
	password = "Set password here"
	sender_email = "whrb.deadairalarm@gmail.com"
	receiver_emails = ["tech@whrb.org", "gm@whrb.org", "pd@whrb.org", "president@whrb.org", "se@whrb.org"]
	# Create a secure SSL context
	context = ssl.create_default_context()

	message = MIMEMultipart("alternative")
	message["Subject"] = "STREAM OFFAIR ALARM"
	message["From"] = sender_email
	message_text = """\
	Subject: STREAM OFF AIR ALARM 

	The stream appears to be broadcasting silence as of {0:%Y-%m-%d %H:%M:%S}

	This message is an automated message sent from Python.""".format(datetime.datetime.now())

	part1 = MIMEText(message_text, "plain")
	message.attach(part1)

	# for some reason googls smtp only worked without using the context
	# this is less secure, but it really doesn't matter who sees this message
	# context = ssl.create_default_context()
	server = smtplib.SMTP_SSL("smtp.gmail.com", port)
	server.set_debuglevel(1)
	server.login(sender_email, password)
	for receiver_email in receiver_emails:
		message["To"] = receiver_email
		server.sendmail(sender_email, receiver_email, message.as_string())
	server.quit()

#send_slack("test message from the offair bot")
prev_silent = False
email_last_sent = time.time() - 1800


# After a little bit of testing -50 dBFS seems reasonable. Mostly classical is in the -30 range
# and goes down to -40 occasionally and absolute silence/static is -65.
while True:
    try:
	capture_stream("/tmp/whrb_capture.mp3")
	capture_segment = AudioSegment.from_mp3("/tmp/whrb_capture.mp3")
	if capture_segment.dBFS < -55.0 and prev_silent == True:
		# only want to send an email at most every 30 minutes
		if time.time() - email_last_sent > 1800:
			warning_message = """ The stream appears to be broadcasting silence as of {0:%Y-%m-%d %H:%M:%S}""".format(datetime.datetime.now())
			print(warning_message)
			send_slack(warning_message)
			email_last_sent = time.time()
	if capture_segment.dBFS < -55.0:
		prev_silent = True
	else:
		prev_silent = False
	print("dbfs", capture_segment.dBFS)
        try:
	    os.remove("/tmp/whrb_capture.mp3")
        except:
            continue
    except:
        continue












	
