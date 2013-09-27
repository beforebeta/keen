import sys, traceback

def print_stack_trace():
    print '-'*60
    traceback.print_exc(file=sys.stdout)
    print '-'*60

import smtplib
_user="beforebetabot@gmail.com"
_password='123dfvlabs'


def _send_mail(msg="Alert from Keen"):
	fromaddr = _user
	toaddrs  = 'amrish.singh@gmail.com'
	# Credentials (if needed)
	username = _user
	password = _password

	# The actual mail send
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()

def immediate_alert(message):
    try:
        _send_mail(message)
    except:
        print_stack_trace()