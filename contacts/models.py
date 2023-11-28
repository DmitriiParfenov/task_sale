from django.db import models


# Create your models here.
class Contact(models.Model):
    email = models.CharField(max_length=150, verbose_name='email')
    country = models.CharField(max_length=150, verbose_name='страна')
    city = models.CharField(max_length=150, verbose_name='город')
    street = models.CharField(max_length=150, verbose_name='улица')
    number = models.PositiveIntegerField(verbose_name='номер дома')
    contact_user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='создатель контактов')

    def __str__(self):
        return f'{self.email} ({self.country})'

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'
