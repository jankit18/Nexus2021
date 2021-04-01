from django.shortcuts import render,redirect
from rest_framework.response import Response
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import UserInfo, EventQuestions, HintDetail
from django.contrib.auth.decorators import login_required
import time
from django.utils.safestring import SafeString
import json

# Create your views here.

def loginHome(request):
    return render(request, 'index.html')


@login_required
def currentQuestion(request):
    user_id = request.user.id
    user_obj = UserInfo.objects.filter(user_id=request.user)
    name = request.user.first_name +" "+request.user.last_name
    print(user_obj)
    if len(user_obj)==0:
        UserInfo.objects.create(user_id=request.user,name=name,level=0,score=0)
        user_obj = UserInfo.objects.filter(user_id=request.user)
        
    level = user_obj[0].level

    if level == 0:
        question_obj = EventQuestions.objects.get(question_no = 0)
        hint_obj0 = HintDetail.objects.filter(user_id=request.user,question_no = question_obj) 
        if len(hint_obj0)==0:
          HintDetail.objects.create(user_id = request.user ,question_no = question_obj, hint=False, attempt= False, dtime = time.time())
          
       
    questions = []
    for i in range(level+1):
        question_obj = EventQuestions.objects.get(question_no = i)
        hint_obj = HintDetail.objects.filter(user_id=request.user,question_no = question_obj)
        
        
        hint1= ""
        hint2= ""
        hint3= ""
        if len(hint_obj)!=0:
            hint_obj=hint_obj[0]
          
            if hint_obj.hint == False :
                x =  time.time()-hint_obj.dtime 
                
                if x>question_obj.expireTime:
                    hint_obj.hint = True
                    hint_obj.save()
            hint_obj = HintDetail.objects.filter(user_id=request.user,question_no = question_obj)[0]
            if hint_obj.hint:
                if hint_obj.hint1:
                    hint1 = question_obj.hintInfo1
                if hint_obj.hint2:
                    hint2 = question_obj.hintInfo2
                if hint_obj.hint3:
                    hint3 = question_obj.hintInfo3
                
                question={
                    'qNo' : (i),
                    'qData' : question_obj.story,
                    'hintUnlock': 1,
                    'hint1': hint1,
                    'hint2': hint2,
                    'hint3': hint3,
                    'ansFormat': question_obj.ansFormat,
                }
                questions.append(question) 
            else:
                question={
                    'qNo' : (i),
                    'qData' : question_obj.story,
                    'hintUnlock': 0,
                    'hint1': hint1,
                    'hint2': hint2,
                    'hint3': hint3,
                    'ansFormat': question_obj.ansFormat,
                }
                questions.append(question) 
        else:
            question={
                'qNo' : (i),
                'qData' : question_obj.story,
                'hintUnlock': 0,
                'hint1':  hint1,
                'hint2':  hint2,
                'hint3':  hint3,
                'ansFormat': question_obj.ansFormat,
            }
            questions.append(question) 
    
    
    context = {
        'user_info' :user_obj,
        'questions' : SafeString(questions),
        'score' : user_obj[0].score
    }
    print(questions)
    return render(request,'LandingPage.html', context)    


@login_required
def scoreboard(request):
    return render(request,'LeaderBoard.html')