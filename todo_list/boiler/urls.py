from django.contrib import admin
from django.urls import path
from .views import TaskList, TaskDetailView,TaskCreate,DeleteView,TaskUpdateView, CustomLoginView, CustomLogoutView, RegisterPage
from django.contrib.auth.views import LogoutView
from . import views
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name="login"),
    path('register/', RegisterPage.as_view(), name="register"),
    path('logout/', views.logout_user , name='logout'),
    path('', TaskList.as_view() , name= "tasks" ),
    path('task/<int:pk>/', TaskDetailView.as_view(), name="task"),
    path('task-create', TaskCreate.as_view(),name="task-create"),
    path('task-update/<int:pk>/', TaskUpdateView.as_view(),name="task-update"),
    path('task-delete/<int:pk>/', DeleteView.as_view(),name="task-delete"),
]
