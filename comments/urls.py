from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_comments, name='my_comments'),
    path('create/<int:recipe_id>/', views.createComment, name='create_comment'),
    path('delete_comment/<int:comment_id>/', views.deleteComment, name='delete_comment'),
    path('modify_comment/<int:comment_id>/', views.modifyComment, name='modify_comment'),
]