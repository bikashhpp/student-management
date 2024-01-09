# forms.py
from django import forms
from .models import Student_profile
from .models import Marks
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student_profile
        # def name(value):
        #  if len(value) <= 3:
        #    raise ValidationError("Name must be more than 3 characters long.")
        #  if not value[0].isupper():
        #    raise ValidationError("First letter of the name must be a capital character.")
        # def age(value):
        #  if value < 0 or value > 120:  # Modify these conditions as needed
        #   raise ValidationError('Invalid age') 
        # fields = ['student_age','student_name' ]  # Fields to include in the form
        fields = "__all__"


class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = "__all__"

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    
    
   
        

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@gmail.com'):  # Replace 'example.com' with your desired domain
            raise forms.ValidationError("Please use a valid example.com email address.")
        return email
       

        
