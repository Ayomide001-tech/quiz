from django.urls import path
from .views import (
    login,
    register,
    logout_view,
    admin_form,
    view_all_user,
)

urlpatterns = [

    path('login/', login, name ='login'),
    path('register/', register, name ='register'),
    path('logout_view/', logout_view, name ='logout_view'),
    path('view_all_user/', view_all_user, name='view_all_user'),
    path('admin_form/', admin_form, name ='admin_form'),


        



]   
   
