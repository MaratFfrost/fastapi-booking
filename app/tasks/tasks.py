from app.tasks.celery import celery
import smtplib
from email.message import EmailMessage
from pydantic import  EmailStr

from app.config import settings

smt_host="smtp.gmail.com"

def get_email_template(code: int, mail:EmailStr):
  email = EmailMessage()
  email["Subject"] = "Подтверждение"
  email["From"] = settings.MAIL_USERNAME
  email["To"] = mail

  email.set_content(
    f"<h1>Потдтвердите аккаунт</h1>\n<p>{code}-код для завершения аунтефикации. На подтверждение аккаунта даётся 10 минут</p>",
    subtype="html"
  )
  return email

@celery.task
def send_email(code: int, mail : EmailStr):
  try:
    email = get_email_template(code, mail)
    with smtplib.SMTP_SSL(smt_host, settings.MAIL_PORT) as server:
      server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
      server.send_message(email)
  except:
    print("error")
