from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserInfo(models.Model):
    user_id =  models.ForeignKey(User, null = True, on_delete=models.SET_NULL)
    #user_id = models.IntegerField()
    name = models.CharField(max_length = 500,default = "")
    usernm = models.CharField(max_length = 500,default = "")
    level = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.name+" "+str(self.user_id)

class EventQuestions(models.Model):
    question_no = models.IntegerField()
    story =  models.CharField(max_length = 2000,default = "")
    answer = models.CharField(max_length = 500,default = "")
    hintInfo1 = models.CharField(max_length = 2000,default = "")
    hintInfo2 = models.CharField(max_length = 2000,default = "")
    hintInfo3 = models.CharField(max_length = 2000,default = "")
    expireTime = models.IntegerField(default=0)
    maxScore = models.IntegerField(default=0)
    ansFormat =  models.CharField(max_length = 2000,default = "")

    def __str__(self):
        return str(self.question_no)        

class HintDetail(models.Model):
    user_id = models.ForeignKey(User, null = True, on_delete=models.SET_NULL)        
    question_no = models.ForeignKey(EventQuestions, null = True, on_delete=models.SET_NULL)
    hint = models.BooleanField(default=False)
    hint1 = models.BooleanField(default=False)
    hint2 = models.BooleanField(default=False)
    hint3 = models.BooleanField(default=False)
    qPenalty = models.IntegerField(default=0)
    attempt =   models.BooleanField(default=False)
    dtime = models.FloatField()

    
    def __str__(self):
        return "User: "+str(self.user_id) + "qno: "+str(self.question_no)



