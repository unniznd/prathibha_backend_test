from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from django.db.models import Q

from datetime import datetime

from .models import Students
from .serializers import ViewStudentSerializer

from users.permissions import IsAdminUserOrBranchAdminUser
from fee.models import Fees

class ViewStudents(ListAPIView):
    
    serializer_class = ViewStudentSerializer
    permission_classes = [IsAdminUserOrBranchAdminUser,]
    filter_backends = [SearchFilter,]
    search_fields = ['^student_name', 'admission_number']

    def get_queryset(self):
        queryset = Students.objects.all()

        standard_filter = self.request.query_params.get('standard')
        division_filter = self.request.query_params.get('division')

        if standard_filter and division_filter:
            queryset = queryset.filter(
                Q(student_branch__standard=standard_filter) &
                Q(student_branch__division=division_filter)
            )
        elif standard_filter:
            queryset = queryset.filter(student_branch__standard=standard_filter)
        elif division_filter:
            queryset = queryset.filter(student_branch__division=division_filter)

      
        return queryset




    def get(self, request, branch_id, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(student_branch__branch=branch_id)
        queryset = self.filter_queryset(queryset)
        serializer = ViewStudentSerializer(queryset.order_by('admission_number'), many=True)
        return Response({
            "status":True, 
            "data":serializer.data
        }, status=status.HTTP_200_OK)

class DashboardOverview(ListAPIView):
    permission_classes = [IsAdminUserOrBranchAdminUser,]

    def get(self, request,branch_id, *args, **kwargs):
        total_students = Students.objects.filter(
            student_branch__branch=branch_id
        ).count()
        # total fee paid for this month
        fee_paid = Fees.objects.filter(
            month=datetime.now().month,
            status='paid',
            student__student_branch__branch=branch_id
        )
        total_fee_paid = 0
        for fee in fee_paid:
            total_fee_paid += fee.amount
        

        # total fee unpaid for this month
        fee_unpaid = Fees.objects.filter(
            month=datetime.now().month,
            status='unpaid',
            student__student_branch__branch=branch_id
        )

        total_fee_unpaid = 0
        for fee in fee_unpaid:
            total_fee_unpaid += fee.amount

        return Response({
            'status':True,
            'total_students':total_students,
            'total_fee_paid':total_fee_paid,
            'total_fee_unpaid':total_fee_unpaid
        })


