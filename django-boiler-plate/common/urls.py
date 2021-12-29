from django.urls import path
from . import views

app_name = 'common'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('mypage/', views.mypage, name='mypage'),
    path('editProfile/', views.editProfile, name='editProfile'),
    path('deleteMember/', views.deleteMember, name='deleteMember'),
    path('findIdPwd/', views.findIdPwd, name='findIdPwd')
]

