from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework import routers, permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from blog.views import CommentViewSet, PostViewSet

router = routers.DefaultRouter()
router.register(r'comments', CommentViewSet)
router.register(r'posts', PostViewSet)

''' Документация API '''
schema_view = get_schema_view(
    openapi.Info(
        title='API для блог-постов',
        default_version='v1',
        description='Этот API блога облегчает создание, чтение, обновление и удаление записей, позволяет '
                    'аутентифицированным пользователям добавлять комментарии, использует JWT для аутентификации, '
                    'включает механизмы защиты от чрезмерных запросов, фильтрует данные с помощью django-filter и '
                    'поддерживает модульные тесты и функциональность модерации контента для администраторов через '
                    'Django admin.',
        contact=openapi.Contact(email="yurokbrat@yandex.ru"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
