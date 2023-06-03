from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('program-master', views.program_master, name='program_master'),
    path('insert-program', views.insert_program, name='insert_program'),
    path('edit-program/<str:id>',views.edit_program, name='edit_program')
]