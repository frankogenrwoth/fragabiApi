from django.contrib import admin

from .models import Question, Answer, AssignmentQuestion, Assignment, Consultation, FragabiUser


admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Assignment)
admin.site.register(AssignmentQuestion)
admin.site.register(Consultation)
admin.site.register(FragabiUser)
