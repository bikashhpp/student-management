from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from typing import Any
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Student_profile
from .models import Marks
from django.views.generic.list import ListView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, UpdateView, DeleteView, View, TemplateView
from .forms import StudentForm
from .forms import MarksForm
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.db.models import F, FloatField, ExpressionWrapper
# from django.template.loader import render_to_string

#################STUDENT##############

class StudentListView(ListView):
    model = Student_profile
    template_name = 'student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        qs = Student_profile.objects.all()
        return qs


class ProfileCreateView(CreateView):
    model = Student_profile
    form_class = StudentForm
    template_name = 'student_profile_form.html'
    success_url = reverse_lazy('student_list')


    def form_valid(self, form):
        # Custom validations for multiple fields
        student_name = form.cleaned_data.get('student_name')
        student_age = form.cleaned_data.get('student_age')
        student_email = form.cleaned_data.get('student_email')
        student_address = form.cleaned_data.get('student_address')
        

        # Add your validation logic here for each field
        if len(student_name) < 3:  # Example validation: student_name should have at least 3 characters
            form.add_error('student_name', 'name should be at least 3 characters long.')

        if student_age < 18 or student_age > 120:  # Example validation: student_age should be between 18 and 120
            form.add_error('student_age', 'age should be between 18 and 120.')

        # Example validation for student_email format using regular expression
        import re
        if not re.match(r"[^@]+@[^@]+\.[^@]+", student_email):
            form.add_error('student_email', 'Enter a valid Email address.')

        if len(student_address) < 4:  # Example validation: student_address should have at least 10 characters
            form.add_error('student_address', 'address should be at least 5 characters long.')

        # Check if any validation errors occurred
        if form.errors:
            return self.form_invalid(form)

        return super().form_valid(form)



class StudentDetailView(DetailView):
    model = Student_profile
    template_name = 'student_Detail.html'
    context_object_name = 'detail'


class StudentUpdateView(UpdateView):
    model = Student_profile
    form_class = StudentForm
    template_name = 'update.html'
    success_url = reverse_lazy('student_list')


class StudentDeleteView(DeleteView):
    model = Student_profile
    template_name = 'delete.html'
    success_url = reverse_lazy('student_list')


################# marks ############


class marksListView(ListView):
    model = Marks
    template_name = 'marksheet.html'
    context_object_name = 'marks'

    def get_queryset(self):
        student_id = self.request.GET.get("student_id", None)
        if student_id:
            qs = Marks.objects.filter(students__id=student_id)
        else:
            qs = None
        return qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        student_id = self.request.GET.get("student_id", None)
        context["latest_marks"] = Marks.objects.filter(students__id=student_id).latest('id')
        return context


class MarksCreateView(CreateView):
    model = Marks
    form_class = MarksForm
    template_name = 'marks.html'
    success_url = reverse_lazy('marks')


################ term ######################


class AjaxView(View):
    def get(self, request, *args, **kwargs):
        from django.forms.models import model_to_dict

        student_id = self.request.GET.get("student_id", None)
        term = self.request.GET.get("term", None)
        print(student_id, term)

        try:
            query = Marks.objects.filter(students__id=student_id, term=term).latest("id")
            value = model_to_dict(query)
            percentage = query.Calculate_percentage()
            obtained = query.Obtained_marks()
        except:
            percentage = None
            value = None
            obtained = None
        return JsonResponse({"marks": value, "percentage": percentage, "obtained": obtained})




#############login ////  #############

class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('create_profile')  # Replace 'dashboard' with your desired URL name after successful login
        else:
            messages.error(request, ' ⚠️ Invalid username or password.')
            return render(request, self.template_name)


#################### REGISTER #################
class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        form = CustomUserCreationForm()  # Use the CustomUserCreationForm
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)  # Use the CustomUserCreationForm
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('login')  # Replace 'login' with your login URL name
        return render(request, self.template_name, {'form': form})
    
################  LANDING PAGE ###############################    

class Landing_page(TemplateView):
    template_name = 'landing_page.html'

################## RANK #############################
class StudentRankListView(ListView):
    model = Marks
    template_name = 'student_rank.html'  # Update with your actual template name
    context_object_name = 'object_list'

    def get_queryset(self):
        term = self.request.GET.get('term')
        if term:
            queryset = Marks.objects.filter(term=term).annotate(
                percentage=ExpressionWrapper(
                    (
                        F('marks_english') + F('marks_nepali') + F('marks_science') +
                        F('marks_math') + F('marks_social') + F('marks_eph') + F('marks_occupation')
                    ) * 100 / (7 * 100),
                    output_field=FloatField()
                 )
            ).order_by('-percentage')
        else:
            queryset = Marks.objects.annotate(
                percentage=ExpressionWrapper(
                    (
                        F('marks_english') + F('marks_nepali') + F('marks_science') +
                        F('marks_math') + F('marks_social') + F('marks_eph') + F('marks_occupation')
                    ) * 100 / (7 * 100),
                    output_field=FloatField()
                 )
            ).order_by('-percentage')

        return queryset
