from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
#   path('admin/', admin.site.urls),
  path('custom_report/',custom_report ,name="custom_report"),
  path('single_report/<int:pid>/',single_report ,name="single_report"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
