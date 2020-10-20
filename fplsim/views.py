from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

#todo migration to integrate within blog app
def selection(request):
    form = UserCreationForm()
    return 'Hello World'
