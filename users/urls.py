from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('inscription/', views.inscriptionPage, name='inscription'),
    path('connexion/', views.accesPage, name='connexion'),
    path('deconnexion/', views.logoutUser, name='deconnexion'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('moi/<int:user_id>/', views.profilUtilisateur, name='my_profile'),
    path('modifier/<int:user_id>/', views.modifierUtilisateur, name='modify_profile'),
    path('supprimer/<int:user_id>/', views.desactiverUtilisateur, name='deactivate_profile'),
    path("change-password/", auth_views.PasswordChangeView.as_view(), name='password_change'),
    path("change-password/done/", auth_views.PasswordChangeDoneView.as_view(template_name='users/successfully_modified.html'), name='password_change_done'),
    path("reset-password/", auth_views.PasswordResetView.as_view(), name='password_reset'),
    path("reset-password/done/", auth_views.PasswordResetDoneView.as_view(template_name='users/reset_password_ongoing.html'), name='password_reset_done'),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name='users/successfully_modified.html'), name='password_reset_complete'),

]
