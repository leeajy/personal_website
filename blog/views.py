from django.shortcuts import render
from django.http import HttpResponse
import fplsim.views as fplsim


posts = [
    {
        'title': 'Can we scrape Tweets to score more points in Fantasy Soccer?',
    }
]

past_projects = [
    {
        'title': 'MyHomePT',
        'caption': 'App to help physical therapy patients perform exercises correctly',
        'image_path': 'assets/img/portfolio/MyHomePT.jpg',
        'link': 'https://antoniolee-personal.s3.us-east-2.amazonaws.com/projects/MyHomePT.pdf',
        'date_posted': 'October 17, 2020',
    },
    {
        'title': 'Energy Jackets',
        'caption': 'Monitoring energy usage at Georgia Tech dorms',
        'image_path': 'assets/img/portfolio/EnergyJackets.jpg',
        'link': 'https://antoniolee-personal.s3.us-east-2.amazonaws.com/projects/Turn+Down+for+Watt.pdf',
        'date_posted': 'October 17, 2020',
    },
    {
        'title': 'Cognito Diagnostics',
        'caption': 'Using eye tracking to diagnose concussions earlier',
        'image_path': 'assets/img/portfolio/Cognito.jpg',
        'link': 'https://antoniolee-personal.s3.us-east-2.amazonaws.com/projects/HackATL+Cognito+Diagnostics.pdf',
        'date_posted': 'October 17, 2020',
    },
    {
        'title': 'Axis',
        'caption': 'Helping immigrants establish credit through loan circles',
        'image_path': 'assets/img/portfolio/Axis.jpg',
        'link': 'https://antoniolee-personal.s3.us-east-2.amazonaws.com/projects/Axis.pdf',
        'date_posted': 'October 17, 2020',
    },
]

content = []

# Create your views here.
def home(request):

    render1 = fplsim.squad_pick(request)
    context = {
        'posts': posts,
        'past_projects': past_projects,
        'fplsim': render1,
        'bProject_section': True,
    }

    return render(request, "blog/index.html", context)


def project(request):
    context = {
        'past_projects': past_projects,
        'bProject_section': True,
    }
    return render(request, "blog/projects.html",  context)

def fplsim_analysis(request):
    context = {
        'content': content,
        'bProject_section': False,
    }
    return render(request, "blog/blog-post.html",  context)

def fplsim_creation(request):
    context = {
        'content': content,
        'bProject_section': False,
    }
    return render(request, "blog/blog-post.html",  context)