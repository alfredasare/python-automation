import requests
import smtplib
import os
import paramiko

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')


def send_notification(email_msg):
    print('Sending an email...')
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = f"Subject: SITE DOWN\n{email_msg}"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)


def restart_container():
    print('Restarting the application...')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Confirm to add host key to server to allow connection
    ssh.connect(hostname='172.104.226.116', username='root', key_filename='/Users/alfredamoah/.ssh/id_rsa')
    stdin, stdout, stderr = ssh.exec_command('docker start 558d2a4099a0')
    print(stdout.readlines())
    ssh.close()


def monitor_application():
    try:
        response = requests.get("http://172-104-226-116.ip.linodeusercontent.com:8080")
        if response.status_code == 200:
            print("Application is running")
        else:
            print("Application Down. Fix it")
            msg = f'Application returned {response.status_code}'
            send_notification(msg)
            restart_container()
    except Exception as ex:
        print(f'Connection error happened: {ex}')
        msg = 'Application not accessible at all'
        send_notification(msg)


monitor_application()
