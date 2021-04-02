from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.loginHome, name = 'loginHome'),
    path('NEXUS/', views.currentQuestion, name = "currentQuestion"),
    path('scoreboard/', views.scoreboard, name= "scoreboard"),
    path('api/',include("Api.urls"))
]