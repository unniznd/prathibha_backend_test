from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from users.permissions import (
    IsAdminUserOrBranchAdminUser,
    IsAdminUser,
    IsBranchAdminUser
)

from branch_class.serializers import (
    ViewOfficeBranchSerializer,
    CreateOfficeBranchSerializer,

    ViewClassDivisionSerializer,
    CreateClassDivisionSerializer, 
    ViewClassDivisionBranchSerializer
)
from branch_class.models import OfficeBranchModel, ClassDivisionModel

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_branch(request, id=None):
    if id:
        office = OfficeBranchModel.objects.filter(id=id).first()
        if not office:
            return Response({'message': 'Branch not found'}, status=status.HTTP_404_NOT_FOUND)
        office_serial = ViewOfficeBranchSerializer(office)
        return Response({'status':True, 'data':office_serial.data}, status=status.HTTP_200_OK)
    
    office = OfficeBranchModel.objects.all()
    office_serial = ViewOfficeBranchSerializer(office, many=True)
    return Response({'status':True, 'data':office_serial.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_branch(request):
    office_serial = CreateOfficeBranchSerializer(data=request.data)
    if office_serial.is_valid():
        office_serial.save()
        return Response({'status':True}, status=status.HTTP_201_CREATED)
    return Response({'status':False, 'errors':office_serial.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_branch(request, id):
    office = OfficeBranchModel.objects.filter(id=id).first()
    if not office:
        return Response({'message': 'Branch not found'}, status=status.HTTP_404_NOT_FOUND)
    office_serial = CreateOfficeBranchSerializer(office, data=request.data, partial=True)
    if office_serial.is_valid():
        office_serial.save()
        return Response({'status':True, 'data':office_serial.data}, status=status.HTTP_200_OK)
    return Response({'status':False, 'errors':office_serial.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_branch(request, id):
    office = OfficeBranchModel.objects.filter(id=id).first()
    if not office:
        return Response({'message': 'Branch not found'}, status=status.HTTP_404_NOT_FOUND)
    office.delete()
    return Response({'message': 'Branch deleted'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUserOrBranchAdminUser])
def get_class_division(request, id=None):
    if id:
        division = ClassDivisionModel.objects.filter(id=id).first()
        if not division:
            return Response({'message': 'Class division not found'}, status=status.HTTP_404_NOT_FOUND)
        division_serial = ViewClassDivisionSerializer(division)
        return Response({'status':True, 'data':division_serial.data}, status=status.HTTP_200_OK)
    
    division = ClassDivisionModel.objects.all()
    division_serial = ViewClassDivisionSerializer(division, many=True)
    return Response({'status':True, 'data':division_serial.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUserOrBranchAdminUser])
def create_class_division(request):
    division_serial = CreateClassDivisionSerializer(data=request.data)
    if division_serial.is_valid():
        division_serial.save()
        return Response({'status':True}, status=status.HTTP_201_CREATED)
    return Response({'status':False, 'errors':division_serial.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUserOrBranchAdminUser])
def update_class_division(request, id):
    division = ClassDivisionModel.objects.filter(id=id).first()
    if not division:
        return Response({'message': 'Class division not found'}, status=status.HTTP_404_NOT_FOUND)
    division_serial = CreateClassDivisionSerializer(division, data=request.data, partial=True)
    if division_serial.is_valid():
        division_serial.save()
        division = ClassDivisionModel.objects.filter(id=id).first()
        division_serial = ViewClassDivisionSerializer(division)
        return Response({'status':True, 'data':division_serial.data}, status=status.HTTP_200_OK)
    return Response({'status':False, 'errors':division_serial.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUserOrBranchAdminUser])
def delete_class_division(request, id):
    division = ClassDivisionModel.objects.filter(id=id).first()
    if not division:
        return Response({'message': 'Class division not found'}, status=status.HTTP_404_NOT_FOUND)
    division.delete()
    return Response({'message': 'Class division deleted'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUserOrBranchAdminUser])
def get_class_division_branch_wise(request, branch_id):
    division = ClassDivisionModel.objects.filter(branch=branch_id)
    division_serial = ViewClassDivisionBranchSerializer(division, many=True)
    return Response({'status':True, 'data':division_serial.data}, status=status.HTTP_200_OK)
