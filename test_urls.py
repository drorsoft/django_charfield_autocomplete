from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/testapp/book/', include('admin_autocomplete.urls')),
    path('admin/', admin.site.urls),
]
