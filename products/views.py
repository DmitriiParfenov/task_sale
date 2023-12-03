from rest_framework import viewsets

from products.models import Product
from products.permissions import IsActiveAndIsOwner
from products.serializers import ProductSerializer, ProductListSerializer


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    """Для создания, удаления, изменения и получения объектов модели Product."""

    permission_classes = (IsActiveAndIsOwner,)
    queryset = Product.objects.all()
    default_serializer = ProductSerializer
    serializers = {
        'list': ProductListSerializer,
        'retrieve': ProductSerializer,
    }

    def perform_create(self, serializer):
        """При создании объекта модели Product текущему объекту присваивается текущий пользователь."""

        new_mat = serializer.save()
        if not self.request.user.is_staff:
            new_mat.product_user = self.request.user
        new_mat.save()

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)
