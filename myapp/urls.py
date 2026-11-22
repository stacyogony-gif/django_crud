from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('Add/', views.AddUser, name='add_user'),
    path('Edit/<int:id>', views.EditUser, name='edit_user'),
    path('Delete/<int:eid>', views.DeleteUser, name='delete_user'),
    path('View/<int:eid>', views.ViewUser, name='view_user'),
]