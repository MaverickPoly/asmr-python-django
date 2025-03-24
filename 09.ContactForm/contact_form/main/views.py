from django.shortcuts import render
from django.contrib import messages
from .forms import MessageForm

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def index(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            sender_email = form.cleaned_data.get("sender_email")
            password = form.cleaned_data.get("password")
            recipient_email = form.cleaned_data.get("recipient_email")
            subject = form.cleaned_data.get("subject")
            body = form.cleaned_data.get("message")
            print(form.as_table())

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            try:
                with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                    server.starttls()
                    server.login(sender_email, password)
                    server.send_message(message, sender_email, recipient_email)
                    messages.success(request, "Message sent successfully!")
            except Exception as e:
                messages.error(request, f"Error sending message: {e}")
        else:
            messages.error(request, "Please correct the errors in the form!")
    else:
        form = MessageForm()
    return render(request, "index.html", {"form": form})
