from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from typing import Any
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Student_profile
from .models import Marks
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, UpdateView, DeleteView, View, TemplateView
from .forms import StudentForm
from .forms import MarksForm
from django.urls import reverse_lazy
# from io import BytesIO
# from django.http import HttpResponse
# from reportlab.pdfgen import canvas
# from django.http import HttpResponse
# from django.template.loader import render_to_string
# from weasyprint import HTML

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


# class TermCreateView(CreateView):
#     model = Marks
#     form_class = MarksForm
#     template_name = 'marks.html'
#     success_url= reverse_lazy('marks')


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


# class pass_fail(Marks):


#############login ////  logout #############

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


class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('login')  # Replace 'login' with your login URL name
        return render(request, self.template_name, {'form': form})


class Landing_page(TemplateView):
    template_name = 'landing_page.html'

    #########################pdf###########

    class GeneratePDFView(TemplateView):
        template_name = 'marksheet.html'


# class GeneratePDFView(TemplateView):
#     template_name = 'marksheet.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Add necessary context variables here
#         return context

#     def render_to_response(self, context, **response_kwargs):
#         html_template = get_template(self.template_name).render(context)
#         pdf_file = HTML(string=html_template).write_pdf()

#         response = HttpResponse(pdf_file, content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="marksheet.pdf"'
#         return response
# class GeneratePDF(View):
#     def get(self, request, *args, **kwargs):
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="marksheet.pdf"'

#         buffer = BytesIO()
#         pdf = canvas.Canvas(buffer)
        
#         # Add content to the PDF (replace with your marksheet details)
#         pdf.drawString(100, 100, "Your marksheet content here")
        
#         pdf.showPage()
#         pdf.save()

#         pdf_data = buffer.getvalue()
#         buffer.close()
        
#         response.write(pdf_data)
#         return response
# class GeneratePDF(View):
#     def get(self, request, *args, **kwargs):
#         # Assuming you have an HTML template for your marksheet
#         html_string = render_to_string('marksheet.html', {'context_data': 'your_data_here'})
        
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="marksheet.pdf"'

#         HTML(string=html_string).write_pdf(response)

#         return response
        
