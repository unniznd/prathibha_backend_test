
from django.contrib import admin
from django.urls import path, include

from users.views import ObtainAuthTokenWithUserId, GetDashboardDetails


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', ObtainAuthTokenWithUserId.as_view()),
    path('dashboard/', GetDashboardDetails.as_view()),

    path('branch/', include('branch_class.urls')),
    path('students/', include('students.urls'))
]
