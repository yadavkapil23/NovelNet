"""
URL configuration for novelnet project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from books.views import user_profile, logout_view

# Customize Django Admin titles
admin.site.site_header = "Novel Net"  # Removes "Django administration" text
admin.site.site_title = "Novel Net Admin"  # Changes browser tab title
admin.site.index_title = "Welcome to Novel Net"  # Changes admin index page title

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
    path('reviews/', include('reviews.urls')),
    path('clubs/', include('clubs.urls')),
    # Override default logout to allow GET as used by navbar
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', user_profile, name='profile'),
]
 
# Serve media files in both development and production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Force serve media files (images) in production (DEBUG=False)
# This is required for Render/Heroku if not using external storage like S3
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
