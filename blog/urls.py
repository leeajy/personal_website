from django.urls import path
from . import views  # from current directory, import the views.py module

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('projects/', views.project, name='blog-projects'),
    path('fplsim-analysis/', views.fplsim_analysis, name='blog-fplsim-analysis'),
    path('fplsim-creation/', views.fplsim_creation, name='blog-fplsim-creation'),
    # path('projects/<str:project_id>/', views.projectid, name='blog-'+project_id), - add details on previous projects
]
