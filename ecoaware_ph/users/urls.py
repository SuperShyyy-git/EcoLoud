from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('admin/users/', views.user_list, name='user_list'),
    path('admin/users/<int:user_id>/edit/', views.user_edit, name='user_edit'), 
    path('admin/users/<int:user_id>/toggle/', views.toggle_user_status, name='toggle_user_status'),
    path('admin/users/<int:user_id>/delete/', views.delete_user, name='delete_user'),


    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('profile/edit/credentials/', views.edit_profile, name='edit_profile'),

    path('password-change/', 
         auth_views.PasswordChangeView.as_view(template_name='users/password_change.html', success_url='/users/password-change/done/'), 
         name='password_change'),
    path('password-change/done/', 
         auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), 
         name='password_change_done'),

    path('access-denied/', views.access_denied, name='access_denied'),
]
