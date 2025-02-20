from django import forms


class MessageForm(forms.Form):
    sender_email = forms.EmailField(label="Your Email", required=True)
    password = forms.CharField(label="Your Password", widget=forms.PasswordInput, required=True,)
    recipient_email = forms.EmailField(label="Recipient Email", required=True)
    subject = forms.CharField(label="Subject", required=True)
    message = forms.CharField(label="Message...", widget=forms.Textarea, required=True)
