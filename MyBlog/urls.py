"""MyBlog URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('blog.urls', 'blog'), namespace='blog')),
    path('books/', include(('books.urls', 'books'), namespace='books')),
    path('authorization/', include(('authorization.urls', 'authorization'), namespace='authorization')),
    path('wall_of_heroes/', include(('wall_of_heroes.urls', 'wall_of_heroes'), namespace='wall_of_heroes')),
    path('my_rules/', include(('my_rules.urls', 'my_rules'), namespace='my_rules')),
    path('tinymce/', include('tinymce.urls')),
    path('comment/', include('comment.urls')),
    path('api/', include('comment.api.urls')),  # only required for API Framework
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
