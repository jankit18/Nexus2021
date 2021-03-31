from django.urls import path,include
from . import views

urlpatterns = [
    path('<int:question_no>',views.checkAnswer, name = "checkAnswer"),
    path('LeaderboardInfo/', views.LeaderboardInfo, name= "LeaderboardInfo"),
]