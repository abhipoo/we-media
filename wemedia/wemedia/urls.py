"""wemedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path
from discuss import views

urlpatterns = [
	path('create_topic/', views.create_topic, name='create_topic'),
	path('create_content/', views.create_content, name='create_content'),
	path('ask_recommendation/', views.ask_recommendation, name = 'ask_recommendation'),
	path('discuss/', include('discuss.urls')),
    path('admin/', admin.site.urls),
]
