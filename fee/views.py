from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from datetime import datetime
from .models import Fees, FeeMonth
from .serializers import FeeSerializer
from students.models import Students
from users.permissions import IsAdminUserOrBranchAdminUser

class FeeView(ListAPIView):
    serializer_class = FeeSerializer
    permission_classes = [IsAdminUserOrBranchAdminUser]
    filter_backends = [SearchFilter,]
    search_fields = ['^student__student_name', 'student__admission_number']
    def get_queryset(self):
        standard = self.request.query_params.get('standard')
        division = self.request.query_params.get('division')
        status = self.request.query_params.get('status')
        month = self.request.query_params.get('month')

        queryset = Fees.objects.all()

        if standard:
            queryset = queryset.filter(student__student_branch__standard=standard)
        if division:
            queryset = queryset.filter(student__student_branch__division=division)
        if status:
            queryset = queryset.filter(status=status)
        if month:
            month_number = datetime.strptime(month, "%b").month
            queryset = queryset.filter(month=month_number)

        return queryset

    def get(self, request, branchId, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        queryset = queryset.filter(student__student_branch__branch__id=branchId)
        serializer = self.serializer_class(queryset, many=True)
        return Response({
            'status':True,
            'total_count':queryset.count(),
            'unpaid_count':queryset.filter(status='unpaid').count(),
            'data':serializer.data,
            
        },status=status.HTTP_200_OK)
    
    def post(self, request, branchId, *args, **kwargs):
        # mark fee as paid and unpaid for a student in fee model
        fee_id = request.data.get('fee_id')
        fee_status = request.data.get('status')

        if not fee_id or not fee_status:
            return Response({
                'status':False,
                'message':'fee_id and status are required'
            },status=status.HTTP_400_BAD_REQUEST)
        
        if fee_status not in ['paid', 'unpaid']:
            return Response({
                'status':False,
                'message':'status should be either paid or unpaid'
            },status=status.HTTP_400_BAD_REQUEST)
        
        try:
            fee = Fees.objects.get(id=fee_id, student__student_branch__branch__id=branchId)
        except Fees.DoesNotExist:
            return Response({
                'status':False,
                'message':'Fee not found'
            },status=status.HTTP_404_NOT_FOUND)

        except:
            return Response({
                'status':False,
                'message':'Something went wrong'
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        fee.status = fee_status
        fee.save()

        return Response({
            'status':True,
            'message':'Fee status updated successfully',
        },status=status.HTTP_200_OK)

class GenerateFee(ListAPIView):
    permission_classes = [IsAdminUserOrBranchAdminUser]
    def post(self, request, branchId, *args, **kwargs):
        standard_fee = request.data.get('standard_fee')
        month = request.data.get('month')

        if not standard_fee or not month:
            return Response({
                'status':False,
                'message':'standard_fee and month are required'
            },status=status.HTTP_400_BAD_REQUEST)
        
        if month:
            month_number = datetime.strptime(month, '%B').month
            month_model = FeeMonth.objects.filter(month=month_number).first()

            if not month_model:
                month_model = FeeMonth.objects.create(
                    month=month_number
                )
                month_model.save()
                students = Students.objects.filter(student_branch__branch__id=branchId)
                for student in students:
                    fee = Fees.objects.create(
                        student=student,
                        amount=standard_fee.get(student.student_branch.standard),
                        month=month_number
                    )
                    fee.save()
                
                return Response({
                    'status':True,
                    'message':'Fee generated successfully'
                },status=status.HTTP_200_OK)
            
            else:
                return Response({
                    'status':False,
                    'message':'Fee already generated for this month'
                },status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response({
                'status':False,
                'message':'Something went wrong'
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)