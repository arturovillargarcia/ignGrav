"""igngrav URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib.gis import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


admin.site.site_header  =  "Gravimetría"  
admin.site.site_title  =  "Custom bookstore admin site"
admin.site.index_title  =  "Administración de datos"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("chaining/", include("smart_selects.urls")),
    path('visualizador/', include('visualizador.urls')),
    path('visualizador/info/', include('visualizador.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
