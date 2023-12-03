from django.db import models

from users.models import NULLABLE


# Create your models here.
class Sale(models.Model):
    class Kinds(models.TextChoices):
        FACTORY = ('Завод', 'Завод')
        RETAIL = ('Розничная сеть', 'Розничная сеть')
        BUSINESSMAN = ('Индивидуальный предприниматель', 'Индивидуальный предприниматель')
    unit = models.CharField(max_length=30, choices=Kinds.choices, default=Kinds.FACTORY, verbose_name='Звено')
    title = models.CharField(max_length=150, verbose_name='Название')
    supplier = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Поставщик', **NULLABLE)
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    sale_user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Создатель сети')
    product = models.ForeignKey('products.Product', on_delete=models.DO_NOTHING, verbose_name='Продукты')
    contact = models.ForeignKey('contacts.Contact', on_delete=models.DO_NOTHING, verbose_name='Контакты')
    debt = models.DecimalField(max_digits=150, decimal_places=2, verbose_name='Задолженность')

    def __str__(self):
        return f'{self.title} ({self.unit})'

    class Meta:
        verbose_name = 'Сеть'
        verbose_name_plural = 'Сети'
