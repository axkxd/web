from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


from .models import Question, Answer


class AskForm(forms.Form):
    title = forms.CharField(max_length = 255)
    text = forms.CharField(widget = forms.Textarea)

    def clean(self):
        return self.cleaned_data

    def clean_title(self):
        title = self.cleaned_data['title']
        if title == None or title.strip() == "":
            raise forms.ValidationError("Empty field Title")
        return title.strip()

    def clean_text(self):
        text = self.cleaned_data['text']
        if text == None or text.strip() == "":
            raise forms.ValidationError("Empty field Text")
        return text.strip()

    def save(self):
        question = Question(**self.cleaned_data)
        question.author_id = self._user.id
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget = forms.Textarea)
    question = forms.IntegerField(widget = forms.HiddenInput())

    def clean(self):
        return self.cleaned_data

    def clean_text(self):
        text = self.cleaned_data['text']
        if text == None or text.strip() == "":
            raise forms.ValidationError("Empty field Text")
        return text.strip()

    def clean_question(self):
         question = self.cleaned_data['question']
         if question == None:
             raise forms.ValidationError("Lost question")
         try:
             question = Question.objects.get(id = int(question))
         except Question.DoesNotExist:
             raise forms.ValidationError("Question does not exist")
             # question = None
         return question

    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.author_id = self._user.id
        answer.save()
        return answer


class SignupForm(forms.Form):
    username = forms.CharField(max_length = 100)
    email = forms.EmailField()
    password = forms.CharField(widget = forms.PasswordInput)

    def clean(self):
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if username == None or username.strip() == "":
            raise forms.ValidationError("Empty field Username")
        try:
            User.objects.get(username = username)
            raise forms.ValidationError("User with this username exist")
        except User.DoesNotExist:
            pass
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email == None or email.strip() == "":
            raise forms.ValidationError("Empty field Email")
        return email.strip()

    def clean_password(self):
        password = self.cleaned_data['password']
        if password == None or password.strip() == "":
            raise forms.ValidationError("Empty field Password")
        self.empty_password = password # save empty password
        return make_password(password) # return hash password

    def save(self):
        user = User(**self.cleaned_data)
        user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length = 100)
    password = forms.CharField(widget = forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if username == None or username.strip() == "":
            raise forms.ValidationError("Empty field Username")
        return username.strip()

    def clean_password(self):
        password = self.cleaned_data['password']
        if password == None or password.strip() == "":
            raise forms.ValidationError("Empty field Password")
        return password.strip()

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            raise forms.ValidationError("Uncorrect username/password")
        if not user.check_password(password):
            raise forms.ValidationError("Uncorrect username/password")