from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.signUp, name='student-sign-up'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('test/', views.test_token, name='test-token'),
    path('users/', views.get_users, name='get_user'),
    path('<int:id>', views.user_detail, name='get_user'),
    path('users/filter', views.get_some_users, name='get_some_users'),
    path('users/staff/', views.get_staff_users, name='get_staff_users'),
    path('counts/', views.get_counts, name='get_counts'),
]