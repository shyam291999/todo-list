from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from . models import Task


class Login(LoginView):

    template_name = 'app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('task')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class Register(FormView):
    template_name = 'app/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Register, self).form_valid(form)

    def get(self, *args, **kwargs):

        if self.request.user.is_authenticated:
            return redirect('task')
        return super(Register, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'app/task_list.html'
    context_object_name = 'tasks'   #default name object_list

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(is_completed=False).count()
        search_input = self.request.GET.get('search-area') or ""
        if search_input:
            context['tasks'] = context['tasks'].filter(task__icontains=search_input)
        context['search_input'] = search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'  #default name object


class CreateTask(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['task', 'description', 'is_completed']
    success_url = reverse_lazy('task')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)


class UpdateTask(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['task', 'description', 'is_completed']
    context_object_name = 'task'
    success_url = reverse_lazy('task')


class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    fields = '__all__'
    context_object_name = 'task'
    success_url = reverse_lazy('task')
    template_name = 'app/task_confirm_delete.html'
