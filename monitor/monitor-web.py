import requests
import smtplib
import os
import paramiko
import linode_api4
import time
import schedule

EMAIL_PASSWD = os.environ.get('EMAIL_PASSWD')
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
LINODE_TOKEN = os.environ.get('LINODE_TOKEN')

dockerID = ''
serverID = ''

def restartContainerAndServer():
    # restart server
    print("Rebooting the server... :)")
    client = linode_api4.LinodeClient(LINODE_TOKEN)
    nginx_server = client.load(linode_api4.Instance, serverID)
    nginx_server.reboot()

    # restart app
    while True:
        nginx_server = client.load(linode_api4.Instance, serverID)
        if nginx_server.status == 'running':
            time.sleep(7)
            restartContainer()
            break

def mailer(email, passwd):
    print('Sending mail... :)')
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWD)
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, "Subject: SITE DOWN \n Fix the issue!")

def restartContainer():
    print('Restarting the application...')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='', username='root', key_filename='')
    stdin, stdout, stderr = ssh.exec_command(f'docker start {dockerID}')
    ssh.close()

def monitorContainer():
    try:
        response = requests.get('http://127.0.0.1:4000')
        print(response.text)

        if int(response.status_code) == 200:
            print("server is working")
        else:
            print("server down please can you check what's wrong. \n Thanks")
            # send email
            mailer(EMAIL_ADDRESS, EMAIL_PASSWD)

            #resart the application
            restartContainer()

    except Exception as ex:
        print(f"Connection fialed: {ex}")
        mailer(EMAIL_ADDRESS, EMAIL_PASSWD)

        # restart server and container
        restartContainerAndServer()

schedule.every(5).minutes.do(monitorContainer)

while True:
    schedule.run_pending()