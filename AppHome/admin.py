from django.contrib import admin
from .models import UserInfo, EventQuestions,HintDetail

# Register your models here.
#hi

admin.site.register(UserInfo) #Registered ContentImage
admin.site.register(EventQuestions)
admin.site.register(HintDetail)
