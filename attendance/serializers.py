from rest_framework import serializers
from students.models import Students
from .models import Attendace, Holiday

class StudentAttendanceSerializer(serializers.ModelSerializer):
    standard = serializers.CharField(source='student_branch.standard')
    division = serializers.CharField(source='student_branch.division')
    reason = serializers.SerializerMethodField()

    class Meta:
        model = Students
        fields = ('admission_number', 'student_name', 'standard', 
                  'division','is_absent', 'reason')
    
    def get_reason(self, obj):
        attendance = Attendace.objects.filter(student=obj, date=self.context['date']).first()
        if attendance:
            return attendance.reason
        return None

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendace
        fields = '__all__'

class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = '__all__'