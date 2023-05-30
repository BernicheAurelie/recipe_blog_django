from django.urls import path
from . import views


urlpatterns = [
    path('inscription/', views.inscriptionPage, name='inscription'),
    path('connexion/', views.accesPage, name='connexion'),
    path('deconnexion/', views.logoutUser, name='deconnexion'),
]