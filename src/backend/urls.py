from django.contrib import admin
from django.urls import path, include

from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from users import views as user_views
from products import views as product_views

router = routers.DefaultRouter()
router.register(r'users', user_views.UserViewSet, basename="users")
router.register(r'products', product_views.ProductViewsets, basename="products")

schema_view = get_schema_view(
   openapi.Info(
      title="E-commerce API",
      default_version='v1',
      description="A project that simulates an e-commerce API.",
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path('admin/', admin.site.urls),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('api/v1/', include(router.urls)),
]
