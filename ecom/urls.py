"""
URL configuration for ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import urls as core_urls
from django.conf.urls import(handler400, handler403, handler404, handler500) # noqa
# Define your URL patterns here.
urlpatterns = [
    path('grappelli/', include('grappelli.urls')),  # grappelli URLS
    path(settings.ADMIN_URL, admin.site.urls),
    path("", include(core_urls)),
    path('captcha/', include('captcha.urls')),
    path("", include("apps.authenticate.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'ecom.views.custom_404_view'
handler500 = 'ecom.views.custom_500_view'
handler403 = 'ecom.views.custom_403_view'
handler400 = 'ecom.views.custom_400_view'
