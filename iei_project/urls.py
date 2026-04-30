from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'IEI Jharkhand State Centre - Admin'
admin.site.site_title = 'IEI Admin Portal'
admin.site.index_title = 'Content Management'

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('website.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
