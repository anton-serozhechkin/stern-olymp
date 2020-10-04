from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.models import User

class SignUpStudentForm(forms.ModelForm):
    telephone_number = forms.CharField(max_length=11, help_text='Телефонный номер')
    class_number = forms.ModelChoiceField(queryset=ClassNumber.objects.all(), help_text='Год обучения')
    name_school = forms.CharField(max_length=50, help_text='Название текущего учебного заведения')

    class Meta:
        model = Student
        fields = ['telephone_number', 'class_number',
                  'name_school']

                
class UserAnswerForm(forms.ModelForm):
    class Meta:
        model = UserAnswer
        fields = ['answer']
