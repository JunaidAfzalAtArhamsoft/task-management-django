from django.urls import path
from . import views

app_name = 'ManageTask'
urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/task-lists/<int:list_name>', views.task_list, name='task_list'),
    path('dashboard/task-lists/<str:list_name>/<int:task_id>/',views.specific_task, name='specific_task'),
    path('mark-as-done/<int:task_id>/', views.mark_as_done, name='mark_as_done'),
    path('update-task/<int:task_id>/', views.update_task, name='update_task'),
    path('dashboard/task-lists/<str:list_name>/add-task/', views.add_task, name='add_task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),


]
