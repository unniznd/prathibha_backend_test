
from django.contrib import admin
from django.urls import path, include

from users.views import ObtainAuthTokenWithUserId


urlpatterns = [
    path('admin/', admin.site.urls),
    path('get-token/', ObtainAuthTokenWithUserId.as_view()),

    path('superuser/branch/', include('branch_class.urls'))
]
