from rest_framework import serializers

from products.models import Product
from users.models import User


class ProductSerializer(serializers.ModelSerializer):
    product_user = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'title', 'model', 'release', 'product_user')


class ProductListSerializer(serializers.ModelSerializer):
    product_user = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Product
        fields = ('title', 'product_user')
