from django.urls import path
from .views import login_page, register, user_dashboard, user_profile, logout_page

app_name = 'account'

urlpatterns = [
    path('login/', login_page, name='login_page'),
    path('register/', register, name='register'),
    path('logout/', logout_page, name='logout'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('edit-profile/', user_profile, name='user_profile'),
]
