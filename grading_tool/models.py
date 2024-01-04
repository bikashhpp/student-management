from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


# Create your models here.
class Student_profile(models.Model):
    student_name = models.CharField(max_length=250)
    student_age = models.IntegerField()
    student_rollno = models.IntegerField()
    student_address = models.CharField(max_length=250)
    student_contact = models.IntegerField()
    student_email = models.CharField(blank=True, null=True, max_length=250)
    student_standard = models.IntegerField()
    student_photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)

    def __str__(self):
        return self.student_name  # Display name in admin panel


class Marks(models.Model):
    TERM_CHOICES = (
        ("First Term", "first_term"), ("Second Term", "second_term"), ("Final Term", "final_term")
    )
    marks_english = models.IntegerField(validators=[MaxValueValidator(100)])
    marks_nepali = models.IntegerField(validators=[MaxValueValidator(100)])
    marks_science = models.IntegerField(validators=[MaxValueValidator(100)])
    marks_math = models.IntegerField(validators=[MaxValueValidator(100)])
    marks_social = models.IntegerField(validators=[MaxValueValidator(100)])
    marks_eph = models.IntegerField(validators=[MaxValueValidator(100)])
    marks_occupation = models.IntegerField(validators=[MaxValueValidator(100)])
    marks_economics = models.IntegerField(validators=[MaxValueValidator(100)])
    students = models.ForeignKey(Student_profile, on_delete=models.CASCADE, blank=True, null=True)
    term = models.CharField(max_length=250, choices=TERM_CHOICES, default="first term")

    def __str__(self):
        if self.students:
            name = self.students.student_name
        else:
            name = "none"
        return name

    def Calculate_percentage(self):
        Total_marks = self.marks_english + self.marks_nepali + self.marks_science + self.marks_math + self.marks_social + self.marks_eph + self.marks_occupation
        Total_sub = 7
        maximum_marks_per_subject = 100
        total_maximum_marks = maximum_marks_per_subject * Total_sub
        percentage = (Total_marks / total_maximum_marks) * 100
        # percentage = (Total_marks/(Total_sub*100))
        return round(percentage, 2)

    def Obtained_marks(self):
        Total_marks = self.marks_english + self.marks_nepali + self.marks_science + self.marks_math + self.marks_social + self.marks_eph + self.marks_occupation
        return Total_marks
