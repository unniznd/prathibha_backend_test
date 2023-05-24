from rest_framework import serializers
from .models import Fees

class FeeSerializer(serializers.ModelSerializer):
    fee_id = serializers.IntegerField(source='id')
    admission_number = serializers.CharField(source='student.admission_number')
    student_name = serializers.CharField(source='student.student_name')
    standard = serializers.CharField(source='student.student_branch.standard')
    division = serializers.CharField(source='student.student_branch.division')
    branch = serializers.CharField(source='student.student_branch.branch.branch_name')
    status = serializers.CharField(source='get_status_display')
    date_of_payment = serializers.SerializerMethodField()

    class Meta:
        model = Fees
        fields = ['fee_id' , 'admission_number','student_name', 'standard', 'division', 'branch', 
                  'amount', 'status', 'date_of_payment']
        

    def get_date_of_payment(self, obj):
        return obj.date_of_payment.strftime("%B %d, %Y")