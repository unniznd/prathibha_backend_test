from django.db import models
from students.models import Students

STATUS = (
    ('paid', 'Paid'),
    ('unpaid', 'Unpaid'),
)

class Fees(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    amount = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS, default='unpaid')
    month = models.CharField(max_length=20, default=5)
    date_of_payment = models.DateField(auto_now=True)

    class Meta:
        unique_together = ['student', 'month']

    def __str__(self):
        return self.student.student_name

class FeeMonth(models.Model):
    month = models.CharField(max_length=20)
    is_generated = models.BooleanField(default=True)

    def __str__(self):
        return self.month