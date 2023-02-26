from django.shortcuts import render
from django.http import HttpResponse 

def comments_index(request): 
    return HttpResponse("**** Welcome to the comments")