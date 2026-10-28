from django.urls import path
from .views import (
    login,
    register,
    logout_view,
    admin_form,
    view_all_user,
    edit_profile,
    update_account_role,
)

urlpatterns = [

    path('login/', login, name ='login'),
    path('register/', register, name ='register'),
    path('logout_view/', logout_view, name ='logout_view'),
    path('view_all_user/', view_all_user, name='view_all_user'),
    path('admin_form/', admin_form, name ='admin_form'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('users/<int:account_id>/role/', update_account_role, name='update_account_role'),

        



]   
   
