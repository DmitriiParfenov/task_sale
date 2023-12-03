from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.serializers import ValidationError

from sales.models import Sale
from sales.permissions import IsActiveAndIsOwner
from sales.serializers import SaleSerializer, SaleRetrieveSerializer, SaleListSerializer


# Create your views here.
class SaleCreateAPIView(generics.CreateAPIView):
    """Для создания объектов модели Sale."""

    serializer_class = SaleSerializer
    queryset = Sale.objects.all()
    permission_classes = (IsActiveAndIsOwner,)

    def perform_create(self, serializer):
        """Метод присваивает текущего пользователя создаваемому объекту. Если пользователь при создании ввел электронный
        адрес другого пользователя, то ему вернется ответ с тем, что он указал другого пользователя."""

        sale_user_from_user = serializer.validated_data.get('sale_user')
        if sale_user_from_user != self.request.user:
            raise ValidationError({"sale_user": "Вы указали чужого пользователя"})
        new_mat = serializer.save()
        if not self.request.user.is_staff:
            new_mat.sale_user = self.request.user
        new_mat.save()


class SaleRetrieveAPIView(generics.RetrieveAPIView):
    """Для получения детальной информации об объекте модели Sale."""

    serializer_class = SaleRetrieveSerializer
    queryset = Sale.objects.all()
    permission_classes = (IsActiveAndIsOwner,)


class SaleUpdateAPIView(generics.UpdateAPIView):
    """Для изменения информации об объекте модели Sale."""

    serializer_class = SaleSerializer
    queryset = Sale.objects.all()
    permission_classes = (IsActiveAndIsOwner,)

    def perform_update(self, serializer):
        """Метод присваивает текущего пользователя создаваемому объекту. Если пользователь при создании ввел электронный
        адрес другого пользователя, то ему вернется ответ с тем, что он указал другого пользователя."""

        sale_user_from_user = serializer.validated_data.get('sale_user')
        if sale_user_from_user != self.request.user:
            raise ValidationError({"sale_user": "Вы указали чужого пользователя"})
        new_mat = serializer.save()
        if not self.request.user.is_staff:
            new_mat.sale_user = self.request.user
        new_mat.save()


class SaleListAPIView(generics.ListAPIView):
    """Для получения информации обо всех объектах модели Sale."""

    serializer_class = SaleListSerializer
    queryset = Sale.objects.all()
    permission_classes = (IsActiveAndIsOwner,)
    filter_backends = [SearchFilter, ]
    search_fields = ['contact__city', 'contact__country']


class SaleDeleteAPIView(generics.DestroyAPIView):
    """Для удаления объекта модели Sale."""

    serializer_class = SaleSerializer
    queryset = Sale.objects.all()
    permission_classes = (IsActiveAndIsOwner,)
