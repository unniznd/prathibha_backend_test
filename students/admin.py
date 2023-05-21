from django.contrib import admin
from .models import Students

@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ['admission_number', 'student_name', 'standard', 'division', 
                    'branch', 'phone_number', 'parent_name']

    def standard(self, obj):
        return obj.student_branch.standard
    
    def division(self, obj):
        return obj.student_branch.division
    
    def branch(self, obj):
        return obj.student_branch.branch.branch_name
    
