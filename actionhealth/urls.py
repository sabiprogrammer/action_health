from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('', include('base.urls', namespace='base')),
    path('account/', include('account.urls', namespace='account')),
    path('article/', include('article.urls', namespace='article')),
    path('articles/', include('article.urls', namespace='article')),
    path('journal/', include('journal.urls', namespace='journal')),
    path('event/', include('event.urls', namespace='event')),
    path('admin/', admin.site.urls),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
