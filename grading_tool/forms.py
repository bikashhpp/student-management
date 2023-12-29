# forms.py
from django import forms
from .models import Student_profile
from .models import Marks

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student_profile
        # fields = ['student_age','student_name' ]  # Fields to include in the form
        fields = "__all__"


class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = "__all__"

        
