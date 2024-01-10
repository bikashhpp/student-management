from django.urls import path
from .views import StudentListView, ProfileCreateView,StudentDetailView,StudentUpdateView,StudentDeleteView,MarksCreateView,marksListView,AjaxView,RegisterView,LoginView,Landing_page,StudentRankListView
from .views import GenerateMarksheetPDF
# from django.contrib.auth import views as auth_views
urlpatterns = [
     path('',Landing_page.as_view(), name='landing_page'),
     path('student_list', StudentListView.as_view(),name='student_list'),
     path('create_profile', ProfileCreateView.as_view(),name='create_profile'),
     path('detail/<int:pk>/', StudentDetailView.as_view(),name='detail'),
     path('update/<int:pk>/update/', StudentUpdateView.as_view(),name='update'),
     path('delete/<int:pk>/delete/', StudentDeleteView.as_view(),name='delete'),
     path('marks/create/', MarksCreateView.as_view(),name='marks'),
     path('marksheet/list/', marksListView.as_view(),name='marksheet'),
     path('AjaxView/marksheet_filter/',AjaxView.as_view(),name='marksheet_filter'),
     path('login/', LoginView.as_view(), name='login'),
     path('register/', RegisterView.as_view(), name='register'),
     path('landing_page/',Landing_page.as_view(), name='landing_page'),
     path('student_rank/', StudentRankListView.as_view(), name='student_rank'),
     path('generate_marksheet_pdf/<int:student_id>/', GenerateMarksheetPDF.as_view(), name='generate_marksheet_pdf'),


   
   
 ]
 
