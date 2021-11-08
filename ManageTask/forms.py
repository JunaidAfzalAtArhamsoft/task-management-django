from django.forms import ModelForm, Form
from django import forms
from .models import Person, Task


class PersonForm(ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        # Making fields required
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    class Meta:
        model = Person
        # fields = '__all__'
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'gender']
        exclude = ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions', 'date_joined', 'last_login')


class LoginForm(forms.Form):

    # def __init__(self, *args, **kwargs):
    #     super(Form, self).__init__(*args, **kwargs)
    #     # Making fields required
    #     self.fields['username'].required = True
    #     self.fields['password'].required = True

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('task_title', 'task_description')