from django.urls import path
from . import views  # from current directory, import the views.py module

urlpatterns = [
    path('', views.squad_pick, name='fplsim-squad_pick'),

]
