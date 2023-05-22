from rest_framework import serializers
from .models import Students

class ViewStudentSerializer(serializers.ModelSerializer):
    standard = serializers.CharField(source='student_branch.standard')
    division = serializers.CharField(source='student_branch.division')
    branch = serializers.CharField(source='student_branch.branch.branch_name')


    class Meta:
        model = Students
        fields = ('admission_number', 'student_name', 'standard', 'division',
                   'branch', 'phone_number', 'parent_name')
    

