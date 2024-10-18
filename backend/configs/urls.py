from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from rest_framework.permissions import AllowAny

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Auto Parks",
        default_version='v1',
        description="About Auto Parks",
        contact=openapi.Contact(email="admin@gmail.com"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)
urlpatterns = [
    path('api/cars', include('apps.cars.urls')),
    path('api/auto_parks', include('apps.auto_parks.urls')),
    path('api/users', include('apps.users.urls')),
    path('api/auth', include('apps.auth.urls')),
    path('api/doc', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
