from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import PersonForm, LoginForm, TaskForm
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from .models import Person, TaskList, Task
from datetime import datetime


def register(request):
    if request.method == 'POST':
        p1 = PersonForm(request.POST)
        if p1.is_valid():
            first_name = p1.cleaned_data.get("first_name")
            last_name = p1.cleaned_data.get("last_name")
            username = p1.cleaned_data.get("username")
            password = p1.cleaned_data.get("password")

            user = Person(first_name=first_name, last_name=last_name, username=username)
            user.set_password(password)
            user.is_staff = True
            user.save()
            return HttpResponse("Registered successfully")
        else:
            context = {'register_form': p1}
            return render(request, template_name='ManageTask/register.html', context=context)
    else:
        form = PersonForm()
        context = {'register_form': form}
        return render(request, template_name='ManageTask/register.html', context=context)

# ################################################################################################### #


def main_page(request):
    return render(request=request, template_name='ManageTask/main_page.html', context={})


# ################################################################################################### #


def login_user(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                request.session['current_user'] = username
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect('/ManageTask/dashboard/')
            else:
                return HttpResponse('User with provided CREDENTIALS not found. '
                                    'Please check your username and password. ')

        else:
            return render(request=request, template_name='ManageTask/login.html',
                          context={'login_form': login_form})
    else:
        current_user = request.user
        try:
            if str(request.session['current_user']) == str(current_user):
                return HttpResponseRedirect('/ManageTask/dashboard/')
        except KeyError:
            login_form = LoginForm()
            return render(request=request, template_name='ManageTask/login.html',
                          context={'login_form': login_form})


# ################################################################################################### #


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/ManageTask/')


# ################################################################################################### #


def get_user_list(username):
    user = Person.objects.get(username=username)
    user_list = TaskList.objects.filter(owner=user.user_ptr_id)
    return user_list


# ################################################################################################### #


def dashboard(request):
    try:

        user = Person.objects.get(username=request.session['current_user'])
        task_list = get_user_list(user.username)
        tasks = {}
        for lists in task_list:
            task = Task.objects.filter(task_list=lists)
            if task is not None:
                tasks[task] = lists
        fullname = user.first_name + ' ' + user.last_name
        fullname = fullname.title()
        tasks_dict = {}
        for ind, tl in enumerate(task_list):
            tasks_dict[ind] = Task.objects.filter(task_list=tl)
        data = {
            'user': fullname,
            'task_list': task_list,
            'tasks': tasks_dict
        }
        return render(request=request, template_name='ManageTask/dashboard.html',
                      context={'data': data})
    except KeyError:
        return HttpResponseRedirect('/ManageTask/login/')
    except Person.DoesNotExist:
        raise Http404(f'No Person Exist with username: {request.user}')


# ################################################################################################### #


def task_list(request, list_name):
    if not validate_request(request):
        return HttpResponseForbidden()
    else:
        list_of_task = TaskList.objects.filter(id=list_name)
        name_of_list = list_of_task[0]
        tasks = Task.objects.filter(task_list=list_name)
        completed_tasks = tasks.filter(is_complete=True)
        incomplete_tasks = tasks.filter(is_complete=False)
        data = {'name_of_list': name_of_list,
                'tasks': tasks,
                'id': name_of_list.id,
                'completed_tasks': completed_tasks,
                'incomplete_tasks': incomplete_tasks
                }
        return render(request=request, template_name='ManageTask/task_list.html', context=data)


# ################################################################################################### #


def specific_task(request, list_name, task_id):
    if not validate_request(request):
        return HttpResponseForbidden()
    else:
        task = Task.objects.filter(id=task_id)
        task = task[0]
        current_address = request.get_full_path()
        context = {'task_title': task.task_title,
                   'task_id': task.id,
                   'task_description': task.task_description,
                   'start_date': task.start_date,
                   'is_complete': task.is_complete,
                   'completed_date': task.completed_date,
                   'address': current_address

                   }
        return render(request=request, template_name='ManageTask/specific_task.html', context=context)


# ################################################################################################### #


def mark_as_done(request, task_id):
    if not validate_request(request):
        return HttpResponseForbidden()
    else:
        my_task = Task.objects.filter(pk=task_id)
        my_task = my_task[0]
        my_task.is_complete = True
        my_task.completed_date = datetime.now()
        my_task.save()
        current_address = request.get_full_path()
        print(current_address)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# ################################################################################################### #


def update_task(request, task_id):
    if validate_request(request):
        task = Task.objects.filter(pk=task_id)
        task_form = TaskForm()
        return render(request=request, template_name=update_task,context={})
    else:
        return HttpResponse('Updating')


# ################################################################################################### #


def delete_task(request, task_id):
    if validate_request(request):
        task = Task.objects.filter(pk=task_id)
        task.delete()
        return HttpResponseRedirect('/ManageTask/dashboard/')
    else:
        return HttpResponseForbidden()


# ################################################################################################### #


def add_task(request, list_name):
    if validate_request(request):
        if request.method == 'POST':
            task_form = TaskForm(request.POST)
            if task_form.is_valid():
                task_title = task_form.cleaned_data.get('task_title')
                task_description = task_form.cleaned_data.get('task_description')
                task_list_id = task_form.cleaned_data.get('task_list')
                current_time = datetime.now()
                print(current_time)

                required_list = TaskList.objects.filter(pk=list_name)
                required_list = required_list[0]

                task = Task(task_title=task_title, task_description=task_description,
                            task_list=required_list, is_complete=False, start_date=current_time)
                task.save()
                return HttpResponse('Task inserted.')
            else:
                return render(request=request, template_name='ManageTask/add_task.html',
                              context={'form': task_form})
        else:
            task_form = TaskForm()
            return render(request=request, template_name='ManageTask/add_task.html',
                          context={'form': task_form})
    else:
        return HttpResponseForbidden()


# ################################################################################################### #


def validate_request(request):
    try:
        user = Person.objects.get(username=request.user)
        return True
    except Person.DoesNotExist:
        return False


# ################################################################################################### #
