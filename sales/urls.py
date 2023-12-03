from django.urls import path

from sales.apps import SalesConfig
from sales.views import SaleRetrieveAPIView, SaleCreateAPIView, SaleUpdateAPIView, SaleListAPIView, SaleDeleteAPIView

app_name = SalesConfig.name

urlpatterns = [
    path('<int:pk>/', SaleRetrieveAPIView.as_view(), name='sales_list'),
    path('create/', SaleCreateAPIView.as_view(), name='sales_create'),
    path('update/<int:pk>/', SaleUpdateAPIView.as_view(), name='sales_update'),
    path('', SaleListAPIView.as_view(), name='sales_list'),
    path('delete/<int:pk>/', SaleDeleteAPIView.as_view(), name='sales_delete')
]
