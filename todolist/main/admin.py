from django.contrib import admin
from .models import Task,TaskManager
admin.site.register(TaskManager)
admin.site.register(Task)
