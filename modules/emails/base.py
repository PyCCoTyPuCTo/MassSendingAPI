from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from schemas.sending_messages import SendingMessageView
from core.config import settings


def create_email_message(info: SendingMessageView):
    msg = MIMEMultipart()
    msg["Subject"] = info._message_id.subject
    msg["From"] = info._sender_bot_id.login
    msg["Bcc"] = ",".join(info.recipients)
    text = MIMEText(info._message_id.text, "plain", "utf-8")
    msg.attach(text)
    return msg

def get_stmp_conn(addr: str, login: str, password: str):
    server = smtplib.SMTP(addr, settings.SMTP_PORT)
    server.starttls()
    server.login(login, password)
    return server

def get_stmp_ssl_conn(addr: str, login: str, password: str):
    server = smtplib.SMTP(addr, settings.SMTP_PORT)
    server.login(login, password)
    server.auth_plain()
    return server