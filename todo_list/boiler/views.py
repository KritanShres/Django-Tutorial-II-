from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Task
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView 
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def logout_user(request): 
    logout(request) 
    messages.success(request, "You have been logged out") 
    return redirect('login')

class CustomLoginView(LoginView): 
    template_name = 'boiler/login.html'
    fields = '__all__ '
    redirect_authenticated_user =  True

    def get_success_url(self): 
        return reverse_lazy('tasks')

    
class RegisterPage(FormView): 
    template_name = 'boiler/register.html' 
    form_class = UserCreationForm
    redirect_authenticated_user = True 
    success_url = reverse_lazy('tasks') 

    def form_valid(self, form): 
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form) 

    def get(self, *args, **kawags): 
        if self.request.user.is_authenticated: 
            return redirect ('tasks')
        return super(RegisterPage, self).get(*args, **kawags) 

    
class CustomLogoutView(LogoutView): 
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task 
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete = False).count()
        
        search_input = self.request.GET.get('search-area') or " "
        if search_input: 
            context['tasks'] = context['tasks'].filter(title__startswith = search_input) 
        context['search_input'] = search_input 
        return context

class TaskDetailView(DetailView): 
    model = Task 

class TaskCreate(CreateView): 
    model = Task 
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks') 

    def form_valid(self, form):
        form.instance.user =self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdateView(UpdateView): 
    model = Task 
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class DeleteView(DeleteView): 
    model = Task 
    context_object_name = 'task' 
    success_url = reverse_lazy('tasks') 






