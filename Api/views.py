from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserInfoSerializer
from AppHome.models import UserInfo, EventQuestions, HintDetail
from django.contrib import messages
from AppHome.views import currentQuestion
from django.contrib.auth.decorators import login_required
import time
from datetime import datetime

@login_required
@api_view(['POST'])
def checkAnswer(request, question_no):
    now = datetime.now()
    print("now =", now)
    # dd/mm/YY H:M:S
    day = now.day
    month =  now.month
    year =  now.year
    hour =  now.hour
    minutes =  now.minute
    second =  now.second
    print(request.data["answer"])

    user_id = request.user.id
    q_obj= EventQuestions.objects.get(question_no=question_no)
    if day < 2 or day == 30 or day == 31:
        if request.data["answer"] == q_obj.answer:
            hint_obj = HintDetail.objects.filter(user_id=request.user,question_no = q_obj)
            print(hint_obj)
            hint_obj=hint_obj[0]
            if hint_obj.attempt ==True:
                return Response("Already")  

            questionScore = 50
            user_obj = UserInfo.objects.get(user_id = request.user)
            if user_obj.level < 10:
               user_obj.level = user_obj.level+1

               
            if hint_obj.hint == False :
                x = hint_obj.dtime - time.time()
                if x>1800:
                    hint_obj.hint = True;
            
            if hint_obj.hint == True:
                questionScore-=20

            user_obj.score+=questionScore
            hint_obj.attempt=True
            user_obj.save()
            hint_obj.save()
            if question_no < 10:
                q_obj1= EventQuestions.objects.get(question_no=question_no+1)
                HintDetail.objects.create(user_id = request.user, question_no = q_obj1, hint=False, attempt= False,dtime = time.time())
                currentQuestion(request)
            else:
               return Response('NEXUS CAPTURED')      
        else:
            return Response("Failure") 
    else:       
        return Response("Over") 
    
    return Response("Success")

@login_required
@api_view(['GET'])
def LeaderboardInfo(request):
    detail = UserInfo.objects.all()
    serializer = UserInfoSerializer(detail, many =True)
    
    print(serializer.data)
    
    return Response(serializer.data)
