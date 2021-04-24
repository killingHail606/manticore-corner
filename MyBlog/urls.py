from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler400, handler403, handler404, handler500

from django.contrib.auth.views import auth_logout
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('blog.urls', 'blog'), namespace='blog')),
    path('books/', include(('books.urls', 'books'), namespace='books')),
    path('authorization/', include(('authorization.urls', 'authorization'), namespace='authorization')),
    path('wall_of_heroes/', include(('wall_of_heroes.urls', 'wall_of_heroes'), namespace='wall_of_heroes')),
    path('my_rules/', include(('my_rules.urls', 'my_rules'), namespace='my_rules')),
    path('tinymce/', include('tinymce.urls')),
    path('comment/', include('comment.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('api/', include('comment.api.urls')),  # only required for API Framework
    path('logout/', auth_logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'blog.views.handler404'
handler500 = 'blog.views.handler500'
