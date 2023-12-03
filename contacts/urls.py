from rest_framework.routers import DefaultRouter

from contacts.apps import ContactsConfig
from contacts.views import ContactViewSet

app_name = ContactsConfig.name
router = DefaultRouter()
router.register('', ContactViewSet, basename='contacts')

urlpatterns = router.urls
