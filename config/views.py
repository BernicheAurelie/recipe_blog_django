from django.shortcuts import render
from sentry_sdk import capture_message


def handler404(request, *args, **argv):
    """function to custom 404 error page"""
    capture_message("error 404", level="error")
    context = {}
    return render(request, "404.html", context)


def handler500(request, *args, **argv):
    """function to custom 500 error page"""
    capture_message("error 500", level="error")
    context = {}
    return render(request, "500.html", context)
