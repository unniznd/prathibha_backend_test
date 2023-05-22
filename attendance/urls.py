from django.urls import path

from attendance import views

urlpatterns = [
    path('<int:branch_id>/',views.StudentAttendanceView.as_view()),
]
