from django.contrib import admin
from app.core.models import Question

class QuestionAdmin(admin.ModelAdmin):
    pass 

# Register your models here.
admin.site.register(Question, QuestionAdmin)