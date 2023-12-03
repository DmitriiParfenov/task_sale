from rest_framework import serializers

from contacts.models import Contact
from users.models import User


class ContactSerializer(serializers.ModelSerializer):
    contact_user = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Contact
        fields = ('id', 'email', 'country', 'city', 'street', 'number', 'contact_user')


class ContactListSerializer(serializers.ModelSerializer):
    contact_user = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Contact
        fields = ('email', 'country', 'contact_user')
