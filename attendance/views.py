from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django.db.models import Q
from django.utils import timezone

from datetime import datetime

from users.permissions import IsBranchAdminUser, IsAdminUserOrBranchAdminUser
from students.models import Students
from .models import Attendace, Holiday
from .serializers import (
    StudentAttendanceSerializer, AttendanceSerializer,
    HolidaySerializer
)

class StudentAttendanceView(ListAPIView):
    serializer_class = StudentAttendanceSerializer
    permission_classes = [IsAdminUserOrBranchAdminUser]
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

        
        
        holiday = Holiday.objects.filter(
            branch=branch_id,
            date=date_filter
        ).first()
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
        
        attendance_filter = self.request.query_params.get('attendance')
        if attendance_filter:
            if attendance_filter == 'present':
                queryset = queryset.filter(is_absent=False)
            elif attendance_filter == 'absent':
                queryset = queryset.filter(is_absent=True)

        absent_count = queryset.filter(is_absent=True).count()

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

    def post(self, request, *args, **kwargs):
        attendance_serial = AttendanceSerializer(data=request.data)
        if attendance_serial.is_valid():
            attendance_serial.save()
            return Response({'status':True}, status=status.HTTP_201_CREATED)
        return Response({
            'status':False, 
            'errors':attendance_serial.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        if request.data['student'] and request.data['date']:
            attendance = Attendace.objects.filter(
                student=request.data['student'],
                date=request.data['date']
            ).first()
            if attendance:
                attendance.delete()
        
                return Response({'status':True}, status=status.HTTP_200_OK)
        
        return Response({'status':False}, status=status.HTTP_400_BAD_REQUEST)
    

class HolidayView(ListAPIView):
    permission_classes = [IsAdminUserOrBranchAdminUser]
    def post(self, request, *args, **kwargs):
        holiday_serial = HolidaySerializer(data=request.data)
        if holiday_serial.is_valid():
            holiday_serial.save()
            return Response({'status':True}, status=status.HTTP_201_CREATED)
        return Response({
            'status':False, 
            'errors':holiday_serial.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        if request.data['date']:
            holiday = Holiday.objects.filter(
                date=request.data['date'], 
                branch=request.data['branch']
            ).first()
            if holiday:
                holiday.delete()
                return Response({'status':True}, status=status.HTTP_200_OK)
        return Response({'status':False}, status=status.HTTP_400_BAD_REQUEST)

    
class TodayAttendanceOverview(ListAPIView):
    permission_classes = [IsAdminUserOrBranchAdminUser]

    def get(self, request, branch_id, *args, **kwargs):
        students = Students.objects.filter(
            student_branch__branch=branch_id
        )

        # get standard division wise attendance for all standard and division
        standard_division_wise_attendance = {}

        for student in students:
            standard = student.student_branch.standard
            division = student.student_branch.division

            if f"{standard} {division}" not in standard_division_wise_attendance:
                standard_division_wise_attendance[f"{standard} {division}"] = {
                    'total':0,
                    'present':0,
                    'absent':0
                }

            # if standard not in standard_division_wise_attendance:
            #     standard_division_wise_attendance[standard] = {}
            
            # if division not in standard_division_wise_attendance[standard]:
            #     standard_division_wise_attendance[standard][division] = {
            #         'total':0,
            #         'present':0,
            #         'absent':0
            #     }
            
            attendance = Attendace.objects.filter(
                student=student,
                date=timezone.localdate()
            ).first()

            standard_division_wise_attendance[f"{standard} {division}"]['total'] += 1
            if attendance:
                standard_division_wise_attendance[f"{standard} {division}"]['absent'] += 1
                
            else:
                standard_division_wise_attendance[f"{standard} {division}"]['present'] += 1
        
        return  Response({
            "status":True,
            "data":standard_division_wise_attendance
        }, status=status.HTTP_200_OK)
                    
        
