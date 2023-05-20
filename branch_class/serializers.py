from rest_framework import serializers

from branch_class.models import OfficeBranchModel, ClassDivisionModel

class CreateOfficeBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeBranchModel
        fields = ('branch_name', 'branch_label')

class ViewOfficeBranchSerializer(serializers.ModelSerializer):
    branch_id = serializers.IntegerField(source='id')
    class Meta:
        model = OfficeBranchModel
        fields = ('branch_id', 'branch_name', 'branch_label',)

class CreateClassDivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassDivisionModel
        fields = ('branch', 'standard', 'division', 'medium')

class ViewClassDivisionSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.branch_name', read_only=True)
    medium = serializers.SerializerMethodField()

    class_division_id = serializers.IntegerField(source='id')

    def get_medium(self, obj):
        return obj.get_medium_display()
    
    class Meta:
        model = ClassDivisionModel
        fields = ('class_division_id', 'branch_name', 'standard', 'division', 'medium')
    
class ViewClassDivisionBranchSerializer(serializers.ModelSerializer):

    class_division_id = serializers.IntegerField(source='id')
    medium = serializers.SerializerMethodField()

    def get_medium(self, obj):
        return obj.get_medium_display()
    
    class Meta:
        model = ClassDivisionModel
        fields = ('class_division_id', 'standard', 'division', 'medium')