import re
from django import forms
from app.models import Question, Profile
from django.core.files.images import get_image_dimensions
from django.contrib.auth.models import User as DjangoUser


class LoginForm(forms.Form):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput)

  def clean_username(self):
    username = self.cleaned_data["username"]
    if ' ' in username:
      raise forms.ValidationError("Username contained whitespace")

    return username


class QuestionForm(forms.Form):
  title = forms.CharField(min_length = 8)
  text  = forms.CharField(widget = forms.Textarea)
  tag   = forms.CharField(min_length = 1,
                          label      = "Теги",
                          help_text  = "Введите теги через пробел"
                        )


class RegisterForm(forms.Form):
  username = forms.CharField()
  email    = forms.CharField()
  password = forms.CharField(
                min_length = 8,
                widget     = forms.PasswordInput
              )
  repeatpassword = forms.CharField(
                min_length = 8,
                widget     = forms.PasswordInput
              )

  def clean_username(self):
    username = self.cleaned_data["username"]
    if DjangoUser.objects.filter(username = username):
      raise forms.ValidationError("This name is already taken")
    if re.search(r"\W", username):
      raise forms.ValidationError("Name contains invalid characters")

    return username

  def clean_email(self):
    email = self.cleaned_data["email"]
    if not re.match(r"(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)", email):
      raise forms.ValidationError("Invalid email")

    return email

  def clean_password(self):
    password = self.cleaned_data["password"]
    if " " in password:
      raise forms.ValidationError("Whitespaces in password")

    return password

  def clean_repeatpassword(self):
    repeatpassword = self.cleaned_data["repeatpassword"]
    password = self.cleaned_data["password"]
    if password != repeatpassword:
      raise forms.ValidationError("Passwords do not match")

    return repeatpassword


class SettingsForm(forms.Form):
  username = forms.CharField(required = False)
  email    = forms.CharField(required = False)
  password = forms.CharField(
      min_length = 8,
      widget     = forms.PasswordInput,
      required   = False
    )

  avatar = forms.ImageField(required=False)


class AnswerForm(forms.Form):
  field = forms.CharField(widget = forms.Textarea)
