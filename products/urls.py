from rest_framework.routers import DefaultRouter

from products.apps import ProductsConfig
from products.views import ProductViewSet

app_name = ProductsConfig.name
router = DefaultRouter()
router.register('', ProductViewSet, basename='products')

urlpatterns = router.urls
