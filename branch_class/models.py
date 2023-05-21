from django.db import models

MEDIUM = (
    (0, "NA"),
    (1, "English Medium"),
    (2, "Malayalam Medium"),
) 

class OfficeBranchModel(models.Model):
    branch_name = models.CharField(max_length=256)
    branch_label = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self) -> str:
        return self.branch_name

class ClassDivisionModel(models.Model):
    branch = models.ForeignKey(OfficeBranchModel, on_delete=models.CASCADE)
    standard = models.CharField(max_length=10)
    division = models.CharField(max_length=4)
    medium = models.IntegerField(choices=MEDIUM, default=0)

    class Meta:
        unique_together = ('branch', 'standard', 'division')

    def __str__(self) -> str:
        return f"{self.branch.branch_name} - {self.standard} - {self.division}"

