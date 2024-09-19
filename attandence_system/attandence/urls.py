from django.urls import path
from attandence import views

urlpatterns = [
    path('markattandence/', views.markattandence, name='markattandence'),
]
