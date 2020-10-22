from django.forms import ModelForm
from .models import Student, UserAnswer, ClassNumber
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class UserForm(UserChangeForm):
    username = forms.CharField(max_length=100, help_text='Логин')
    last_name = forms.CharField(max_length=100, help_text='Фамилия')
    first_name = forms.CharField(max_length=100, help_text='Имя')
    email = forms.EmailField(max_length=100, help_text='Электронная почта')

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name',
                  'email']
        exclude = ('data_joined', )

class SignUpStudentForm(forms.ModelForm):
    telephone_number = forms.CharField(max_length=18, help_text='Телефонный номер')
    class_number = forms.ModelChoiceField(queryset=ClassNumber.objects.all(), help_text='Год')
    name_school = forms.CharField(max_length=50, help_text='Название текущего учебного заведения')

    class Meta:
        model = Student
        fields = ['telephone_number', 'class_number',
                  'name_school']


class UserAnswerForm(forms.ModelForm):
    class Meta:
        model = UserAnswer
        fields = ['answer']
