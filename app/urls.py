from django.urls import path
from app.views import mainPageView, Login

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('main/', mainPageView, name='main'),
]