from django.urls import path,include
from . import views

urlpatterns = [
    path('<int:question_no>',views.checkAnswer, name = "checkAnswer"),
    path('LeaderboardInfo/', views.LeaderboardInfo, name= "LeaderboardInfo"),
    path('HintInfo/<int:question_no>/<int:hint_no>', views.HintInfo, name= "HintInfo"),
]