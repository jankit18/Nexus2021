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
   
    day = now.day
    month =  now.month
    year =  now.year
    hour =  now.hour
    minutes =  now.minute
    second =  now.second
  
    user_id = request.user.id
    q_obj= EventQuestions.objects.get(question_no=question_no)
    if (day>=3 and hour>=12)==False:
        if request.data["answer"] == q_obj.answer:
            hint_obj = HintDetail.objects.filter(user_id=request.user,question_no = q_obj)
            print(hint_obj)
            hint_obj=hint_obj[0]
            if hint_obj.attempt ==True:
                return Response("Already")  

            
            user_obj = UserInfo.objects.get(user_id = request.user)
            if user_obj.level < 10:
               user_obj.level = user_obj.level+1

               
            if hint_obj.hint == False :
                x = hint_obj.dtime - time.time()
                if x>1800:
                    hint_obj.hint = True;
            user_obj.score+= q_obj.maxScore
            if hint_obj.hint == True:
                user_obj.score+= hint_obj.qPenalty
            
            
            hint_obj.attempt=True
            user_obj.save()
            hint_obj.save()
            x = EventQuestions.objects.all()
            x = len(x)-1
           
            if question_no < x:
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

@login_required
@api_view(['POST'])
def HintInfo(request,  question_no, hint_no):

    user_id = request.user.id
    q_obj= EventQuestions.objects.get(question_no=question_no)
    user_obj = UserInfo.objects.get(user_id = request.user)
    hint_obj = HintDetail.objects.filter(user_id=request.user,question_no = q_obj)
    print(hint_obj)
    hint_obj=hint_obj[0]

    if hint_obj.hint == False :
        x = hint_obj.dtime - time.time()
        if x>1800:
            hint_obj.hint = True;
    hint ="" 
    if hint_obj.hint == True:
        print("reach")
        if hint_no == 1:
            hint_obj.qPenalty-=10
            hint+= q_obj.hintInfo1
            hint_obj.hint1 = True
        elif  hint_no == 2:
            hint_obj.qPenalty-=20
            hint+= q_obj.hintInfo2
            hint_obj.hint2 = True
        elif  hint_no == 3:
            hint_obj.qPenalty-=30 
            hint+= q_obj.hintInfo3
            hint_obj.hint3 = True
    else:
        return Response("")
    hint_obj.save()
    return Response(hint)



       
