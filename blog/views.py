from django.shortcuts import render
from django.http import HttpResponse
import fplsim.views as fplsim


posts = [
    {
        'title': 'Can we scrape web data to score more points in Fantasy Soccer?',
        'content': '''We all have those days. You prepare your best starting 11 but matchday comes and you realize 
        your star player is out sick. Or even worse, he's had a bust up with the manager and he has been frozen out 
        of the squad. You lose this week's matchup but you are undeterred. Instead, this week you spent all your time 
        looking at tabloid articles for news of your players. You see one of them has been photographed at Burger 
        King! This will surely cause him to be in trouble and you swap this player out for the next round of games. 
        You think that your extra research will bring you extra points and you pat yourself in the back. However, 
        you realize that the exact opposite happened - the player happened to score a hat trick on the next set of 
        games! So what is going on here? Are news a good predictor of a player's success in fantasy soccer? Or are 
        you better off ignoring this information and focusing solely on the player's stats? ''',
        'date_posted': 'October 17, 2020'
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
    testdata = fplsim.selection(request)
    context = {
        'posts': posts,
        'past_projects': past_projects,
        'fplsim': testdata,
    }

    return render(request, "blog/index.html", context)


def project(request):
    context = {
        'past_projects': past_projects,
    }
    return render(request, "blog/projects.html",  context)
