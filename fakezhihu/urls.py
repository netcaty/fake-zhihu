from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from main.views import index
urlpatterns = [
    # Examples:
    # url(r'^$', index, name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('account.urls',
                              namespace='account',
                              app_name='account')),

    url(r'^', include('main.urls')),
    # 主页
    url(r'^$', index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)