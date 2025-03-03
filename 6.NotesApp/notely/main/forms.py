from django import forms


"""
Login Form, Register Form

Create new note form

Update Note Form(Can implement without)
"""


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, label="Username")
    email = forms.EmailField(required=True, label="Email")
    password = forms.CharField(required=True, label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(required=True, label="Confirm Password", widget=forms.PasswordInput)


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, label="Email")
    password = forms.CharField(required=True, label="Password", widget=forms.PasswordInput)


class NewNoteForm(forms.Form):
    title = forms.CharField(max_length=500, required=True, label="Title")
    content = forms.CharField(required=True, label="Content", widget=forms.Textarea)
    tag = forms.CharField(max_length=100, required=True, label="Tag")
