"""rest_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from rest_framework import routers
from leaderboard import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'school', views.SchoolViewSet, 'school')
router.register(r'topalltime', views.TopAllTimeViewSet, 'topalltime')
router.register(r'topyear', views.TopYearViewSet, 'topyear')
router.register(r'topterm', views.TopTermViewSet, 'topterm')
router.register(r'topmonth', views.TopMonthViewSet, 'topmonth')
router.register(r'mostrecentq', views.MostRecentQViewSet, 'mostrecentq')


urlpatterns = [
	path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
