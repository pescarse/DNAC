import env_lab
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def create_smtp_server(smtp_server=env_lab.email_server, smtp_port=env_lab.email_port,
                       email_user=env_lab.email_user, email_password=env_lab.email_password):
    s = smtplib.SMTP(host=smtp_server, port=smtp_port)
    s.starttls()
    s.login(email_user, email_password)
    return s


def create_message(recipient, subject, message, sender=env_lab.email_user):
    msg = MIMEMultipart()

    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    return msg

