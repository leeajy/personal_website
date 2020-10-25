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
        'link': 'https://drive.google.com/file/d/1GhRsjtWY2TAZ2ClHthXLDpY_TFyPmAA7/view?usp=sharing',
        'date_posted': 'October 17, 2020',
    },
    {
        'title': 'Energy Jackets',
        'caption': 'Monitoring energy usage at Georgia Tech dorms',
        'image_path': 'assets/img/portfolio/EnergyJackets.jpg',
        'link': 'https://drive.google.com/file/d/1KY60GwCPzQCHJZrkF-FvJ-NKYiL7mtSW/view?usp=sharing',
        'date_posted': 'October 17, 2020',
    },
    {
        'title': 'Cognito Diagnostics',
        'caption': 'Using eye tracking to diagnose concussions earlier',
        'image_path': 'assets/img/portfolio/Cognito.jpg',
        'link': 'https://drive.google.com/file/d/1IV51n-QTmxLTHgx1ZBQKv5zHI-J6kvAo/view?usp=sharing',
        'date_posted': 'October 17, 2020',
    },
    {
        'title': 'Axis',
        'caption': 'Helping immigrants establish credit through loan circles',
        'image_path': 'assets/img/portfolio/Axis.jpg',
        'link': 'https://drive.google.com/file/d/1V8qQxIEfX9IgV-XImtW3qaIi4L047JW5/view?usp=sharing',
        'date_posted': 'October 17, 2020',
    },
]


# Create your views here.
def home(request):

    render1 = fplsim.squad_pick(request)
    context = {
        'posts': posts,
        'past_projects': past_projects,
        'fplsim': render1,
    }

    return render(request, "blog/index.html", context)


def project(request):
    context = {
        'past_projects': past_projects,
    }
    return render(request, "blog/projects.html",  context)
