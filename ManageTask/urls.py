from django.urls import path
from . import views

app_name = 'ManageTask'
urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/task-lists/', views.task_list, name='task_list'),

]
