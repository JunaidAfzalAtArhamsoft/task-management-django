from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import PersonForm, LoginForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Person, TaskList, Task


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


def main_page(request):
    return render(request=request, template_name='ManageTask/main_page.html', context={})


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
                return HttpResponse(f'Welcome {username}')
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
                # return HttpResponse('<h1>You are Already logedIn!</h1><h3>Redirecting to dashboard</h3>')
                return HttpResponseRedirect('/ManageTask/dashboard/')
                # return HttpResponse('<h1>You are Already logedIn!</h1><h3>Redirecting to dashboard</h3>')

        except KeyError:
            login_form = LoginForm()
            return render(request=request, template_name='ManageTask/login.html',
                          context={'login_form': login_form})


def get_user_list(username):
    user = Person.objects.get(username=username)
    user_list = TaskList.objects.filter(owner=user.user_ptr_id)
    return user_list


def dashboard(request):
    try:

        user = Person.objects.get(username=request.session['current_user'])
        task_list = get_user_list(user.username)
        tasks = {}
        for lists in task_list:
            task = Task.objects.filter(task_list=lists)
            if task is not None:
                tasks[lists] = task
        fullname = user.first_name + ' ' + user.last_name
        fullname = fullname.title()
        data = {
            'user': fullname,
            'task_list': task_list,
            'tasks': tasks
        }
        return render(request=request, template_name='ManageTask/dashboard.html',
                      context={'data': data})
    except KeyError:
        return HttpResponseRedirect('/ManageTask/login/')
    except Person.DoesNotExist:
        raise Http404(f'No Person Exist with username: {request.user}')


def task_list(request):
    return render(request=request, template_name='ManageTask/task_list.html', context={})