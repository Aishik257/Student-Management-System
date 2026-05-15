from django import forms
from .models import Student, Marks

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll', 'age', 'course']

    from .models import Marks

class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = ['subject', 'marks']