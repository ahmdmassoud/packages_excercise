"""packages URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
import packages.views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('show-sample-package/',packages.views.show),
    path('latest-user-package/',packages.views.show_all_package_user),
    path('show-sample-package/<str:package_name>/',packages.views.show_package),
    path('latest-user-package/<str:package_name>/',packages.views.show_package_user),
    path('about/',packages.views.about),
    path('error/',packages.views.error),
    path('',packages.views.home),
]
