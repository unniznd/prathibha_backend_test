from django.contrib import admin
from .models import Fees, FeeMonth

import calendar

@admin.register(Fees)
class FeesAdmin(admin.ModelAdmin):
    list_display = ['name', 'standard','divison','status','branch', 'month_name','date_of_payment']

    def name(self, obj):
        return obj.student.student_name
    
    def standard(self, obj):
        return obj.student.student_branch.standard
    
    def divison(self, obj):
        return obj.student.student_branch.division
    
    def branch(self, obj):
        return obj.student.student_branch.branch.branch_name
    
    def month_name(self, obj):
        return calendar.month_name[int(obj.month)]
    

@admin.register(FeeMonth)
class FeeMonthAdmin(admin.ModelAdmin):
    list_display = ['month_name', 'is_generated']

    def month_name(self, obj):
        return calendar.month_name[int(obj.month)]
    