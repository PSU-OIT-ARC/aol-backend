from django.shortcuts import render


def home(request):
    """The homepage of the site"""
    return render(request, "home/home.html", {
    })
