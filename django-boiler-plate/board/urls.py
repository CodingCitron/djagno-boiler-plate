from django.urls import path

from . import views

app_name = 'board'

urlpatterns = [
    path('', views.list, name='list'),
    path('post/', views.post, name='post'),
    path('read/<int:post_id>/', views.read, name='read'),
    path('update/<int:post_id>/', views.update, name='update'),
    path('delete/<int:post_id>/', views.delete, name='delete'),
    path('ajaxList', views.ajaxList, name='ajaxList'),
]