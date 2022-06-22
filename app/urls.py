from django.contrib.auth.decorators import login_required
from django.urls import path
from app.views import Login, logout_user, Profie, MainPage

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('main/', login_required(MainPage.as_view()), name='main'),
    path('profile/', login_required(Profie.as_view()), name='profile'),
]