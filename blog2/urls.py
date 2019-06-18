"""blog2 URL Configuration

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
from django.urls import path,include

import profile.views
import blog.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', profile.views.home, name='home'),
    path('about/', profile.views.about, name='about'),

    
    path('accounts/', include('accounts.urls')),
    path('blog/', include('blog.urls', namespace="blog")),
    
    path('portfolio/', profile.views.portfolio, name='portfolio'),
    path('portfolio/<int:profile_id>/', profile.views.detail, name='detail'),    

    path('markdownx/', include('markdownx.urls')),
    # path('martor/', include('martor.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 미디어 설정을 한다면 1. setting(root, url), 2.templates(.url), 3. url.py( static())
