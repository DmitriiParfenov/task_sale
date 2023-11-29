from django.db import models


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    model = models.CharField(max_length=150, verbose_name='Модель')
    release = models.DateField(db_index=True, verbose_name='Дата выхода')

    def __str__(self):
        return f'Продукт {self.title}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

