from rest_framework import viewsets

from contacts.models import Contact
from contacts.permissions import IsActiveAndIsOwner
from contacts.serializers import ContactSerializer, ContactListSerializer


# Create your views here.
class ContactViewSet(viewsets.ModelViewSet):
    """Для создания, удаления, изменения и получения объектов модели Contact."""

    permission_classes = (IsActiveAndIsOwner, )
    queryset = Contact.objects.all()
    default_serializer = ContactSerializer
    serializers = {
        'list': ContactListSerializer,
        'retrieve': ContactSerializer,
    }

    def perform_create(self, serializer):
        """При создании объекта модели Contact текущему объекту присваивается текущий пользователь."""

        new_mat = serializer.save()
        if not self.request.user.is_staff:
            new_mat.contact_user = self.request.user
        new_mat.save()

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)
