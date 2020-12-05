from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import (
    include,
    path,
)
from django.views.decorators.cache import never_cache

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("social/", include("social_django.urls", namespace="social")),
    path("captcha/", include("captcha.urls")),
    path("api/", include("api.urls")),
    path("", include("cinema.urls", namespace="")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
    urlpatterns.append(path("static/<path:path>", never_cache(serve)))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
