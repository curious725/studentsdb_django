# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Student, Group


class StudentAdmin(admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Group)
