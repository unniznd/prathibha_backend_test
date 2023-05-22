from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django.db.models import Q
from django.utils import timezone

from datetime import datetime

from students.models import Students
from .models import Attendace, Holiday
from .serializers import StudentAttendanceSerializer

class StudentAttendanceView(ListAPIView):
    serializer_class = StudentAttendanceSerializer
    permission_classes = [IsAuthenticated,]
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
        date_filter = self.request.query_params.get('date')

        if not date_filter:
            date_filter = timezone.localdate().strftime("%Y-%m-%d")
        
        formatted_date = datetime.strptime(date_filter, "%Y-%m-%d").strftime("%B %d, %Y")

        
        
        holiday = Holiday.objects.filter(date=date_filter).first()
        if holiday:
            return Response({
                "status":True,
                "message":f"{holiday.reason}",
                "is_holiday":True,
                "date":formatted_date,
            }, status=status.HTTP_200_OK)

        queryset = self.get_queryset()
        queryset = queryset.filter(student_branch__branch=branch_id)
        
        
        absent_count = 0

        for query in queryset:
            attendace = Attendace.objects.filter(
                student=query,
                date=date_filter
            ).first()
            
            if attendace:
                query.is_absent = not attendace.is_present
            else:
                query.is_absent = False
            

            query.save()
                
            
            
           
        queryset = self.filter_queryset(queryset)
        absent_count = queryset.filter(is_absent=True).count()

        attendance_filter = self.request.query_params.get('attendance')
        if attendance_filter:
            if attendance_filter == 'present':
                queryset = queryset.filter(is_absent=False)
            elif attendance_filter == 'absent':
                queryset = queryset.filter(is_absent=True)

        
        serializer = self.serializer_class(
            queryset,
            context={
                'date':date_filter
            }, many=True)
        
        return Response({
            "status":True,
            "date":formatted_date,
            "is_holiday":False,
            "total_count":queryset.count(),
            "absent_count":absent_count,
            "data":serializer.data,
        }, status=status.HTTP_200_OK)
