from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserInfoSerializer
from AppHome.models import UserInfo, EventQuestions, HintDetail
from django.contrib import messages
from AppHome.views import currentQuestion
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import time
from datetime import datetime

@login_required
@api_view(['POST'])
def checkAnswer(request, question_no):
    user_obj = UserInfo.objects.get(user_id = request.user)
    
    timeRequest = time.time()
    if timeRequest-user_obj.timeLast>60:
      user_obj.timeLast = timeRequest
      user_obj.numAttempt=0
      user_obj.save()
    elif user_obj.numAttempt>5:
        user_obj.numAttempt = 0
        user_obj.save()
        logout(request)
        return Response('Timeout')
    
   
    user_obj.numAttempt+=1
    user_obj.save()
    
    '''
    now = datetime.now()
   
    day = now.day
    month =  now.month
    year =  now.year
    hour =  now.hour
    minutes =  now.minute
    second =  now.second
    '''
  
    user_id = request.user.id
    q_obj= EventQuestions.objects.get(question_no=question_no)
    
    if request.data["answer"] == q_obj.answer:
        hint_obj = HintDetail.objects.filter(user_id=request.user,question_no = q_obj)
        print(hint_obj)
        hint_obj=hint_obj[0]
        if hint_obj.attempt ==True:
            return Response({'status':'Already','attemptl':6-user_obj.numAttempt})  

        x = EventQuestions.objects.all()
        x = len(x)-1
        
        

        if user_obj.level < x:
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
        else:
            return Response({'status':'NEXUS CAPTURED','attemptl':6-user_obj.numAttempt})     
    else:
        return Response({'status':"Failure",'attemptl':6-user_obj.numAttempt}) 
   
    return Response({'status':"Success",'attemptl':6-user_obj.numAttempt})

@login_required
@api_view(['GET'])
def LeaderboardInfo(request):
    user_obj = UserInfo.objects.get(user_id = request.user)
    timeRequest = time.time()
    if timeRequest-user_obj.timeLast>60:
      user_obj.timeLast = timeRequest
      user_obj.numAttempt=0
      user_obj.save()
    elif user_obj.numAttempt>5:
        user_obj.numAttempt = 0
        user_obj.save()
        logout(request)
        return Response('Timeout')
        
    user_obj.numAttempt+=1
    user_obj.save()
    detail = UserInfo.objects.all()
    serializer = UserInfoSerializer(detail, many =True)
    
    return Response(serializer.data)

@login_required
@api_view(['POST'])
def HintInfo(request,  question_no, hint_no):
    
    user_id = request.user.id
    q_obj= EventQuestions.objects.get(question_no=question_no)
    user_obj = UserInfo.objects.get(user_id = request.user)

    timeRequest = time.time()
    if timeRequest-user_obj.timeLast>60:
      user_obj.timeLast = timeRequest
      user_obj.numAttempt=0
      user_obj.save()
    elif user_obj.numAttempt>5:
        user_obj.numAttempt = 0
        user_obj.save()
        logout(request)
        return Response('Timeout')
    
   
    user_obj.numAttempt+=1
    user_obj.save()
    print(user_obj.numAttempt)

    hint_obj = HintDetail.objects.filter(user_id=request.user,question_no = q_obj)
   
    hint_obj=hint_obj[0]

    if hint_obj.hint == False :
        x = hint_obj.dtime - time.time()
        if x>1800:
            hint_obj.hint = True
    hint ="" 
    if hint_obj.hint == True:
        if hint_no == 1 and hint_obj.hint1 == False:
            hint_obj.qPenalty-=10
            hint+= q_obj.hintInfo1
            hint_obj.hint1 = True
        elif  hint_no == 2 and hint_obj.hint2 == False:
            hint_obj.qPenalty-=20
            hint+= q_obj.hintInfo2
            hint_obj.hint2 = True
        elif  hint_no == 3 and hint_obj.hint3 == False:
            hint_obj.qPenalty-=50 
            hint+= q_obj.hintInfo3
            hint_obj.hint3 = True
        else:
            return Response({'hint':"", 'attemptl':6-user_obj.numAttempt})
    else:
        return Response({'hint':"", 'attemptl':6-user_obj.numAttempt})
    hint_obj.save()
    return Response({'hint':hint, 'attemptl':6-user_obj.numAttempt})



       
