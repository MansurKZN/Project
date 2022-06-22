from django.contrib.auth.decorators import login_required
from django.urls import path
from app.views import mainPageView, Login, logout_user, Profie

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('main/', mainPageView, name='main'),
    path('profile/', login_required(Profie.as_view()), name='profile'),
]