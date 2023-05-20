from django.contrib import admin

from branch_class.models import OfficeBranchModel, ClassDivisionModel

@admin.register(OfficeBranchModel)
class OfficeBranchAdmin(admin.ModelAdmin):
    list_display = ('branch_name', 'branch_label')

@admin.register(ClassDivisionModel)
class ClassDivisionAdmin(admin.ModelAdmin):
    list_display = ('branch_name', 'standard', 'division', 'medium')

    def branch_name(self, obj):
        return obj.branch.branch_name