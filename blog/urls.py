from django.urls import path, include
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_lists'),
    path('post/<pk>', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<pk>/edit/', views.post_edit, name='post_edit'),
]
