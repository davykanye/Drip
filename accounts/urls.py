from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('tutorial', views.tutorial, name='tutorial'),
    path('profile_pic', views.profile_pic, name='profile_pic'),
    ########## Handling Forgot Password ###############################
    path('reset_password', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_complete', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
