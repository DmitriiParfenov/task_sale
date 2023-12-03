from rest_framework import serializers

from contacts.serializers import ContactSerializer
from products.serializers import ProductSerializer
from sales.models import Sale
from sales.validators import SupplierValidator, ProductValidator, ContactValidator
from users.models import User


class SaleRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для получения детальной информации конкретного объекта. """

    supplier = serializers.SerializerMethodField()
    sale_user = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())
    product = ProductSerializer(read_only=True)
    contact = ContactSerializer(read_only=True)

    class Meta:
        model = Sale
        fields = ('id', 'title', 'unit', 'supplier', 'created', 'product', 'contact', 'sale_user', 'debt')
        validators = [SupplierValidator(unit='unit', supplier='supplier')]

    def get_supplier(self, instance):
        """Метод для получения информации поля <supplier>."""

        if instance.supplier is not None:
            return SaleRetrieveSerializer(instance.supplier).data
        return []


class SaleSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и изменения информации об объекте. """

    sale_user = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Sale
        fields = ('id', 'title', 'unit', 'supplier', 'created', 'product', 'contact', 'sale_user', 'debt')
        validators = [SupplierValidator(unit='unit', supplier='supplier'),
                      ProductValidator(product_user='product', sale_user='sale_user'),
                      ContactValidator(contact='contact', sale_user='sale_user')]

    def update(self, instance, validated_data):
        """Метод изменяет данные из validated_data объекта instance. """

        instance.title = validated_data.get('title', instance.title)
        instance.unit = validated_data.get('unit', instance.unit)
        instance.supplier = validated_data.get('supplier', instance.supplier)
        instance.product = validated_data.get('product', instance.product)
        instance.contact = validated_data.get('contact', instance.contact)
        return instance


class SaleListSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации об объектах. """

    sale_user = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())
    supplier = serializers.SerializerMethodField()
    contact = ContactSerializer(read_only=True)

    class Meta:
        model = Sale
        fields = ('id', 'title', 'unit', 'supplier', 'sale_user', 'contact')

    def get_supplier(self, instance):
        """Метод для получения информации поля <supplier>."""

        if instance.supplier is not None:
            return SaleListSerializer(instance.supplier).data
        return []
