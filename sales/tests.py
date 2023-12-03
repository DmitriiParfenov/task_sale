from rest_framework import status

from contacts.models import Contact
from products.models import Product
from sales.models import Sale
from users.tests import UserModelTestCase


# Create your tests here.
class SaleModelTestCase(UserModelTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Создание объектов Product
        self.product_1 = Product.objects.create(
            title='Грени',
            model='Яблоки',
            release='2023-12-01',
            product_user=self.user_test
        )
        self.product_1.save()

        self.product_2 = Product.objects.create(
            title='Москвич',
            model='Автомобиль',
            release='2023-12-31',
            product_user=self.inactive_user
        )
        self.product_2.save()

        # Создание объектов Contact
        self.contact_1 = Contact.objects.create(
            email='test@test.com',
            country='Россия',
            city='СПб',
            street='Невский',
            number='21',
            contact_user=self.user_test
        )
        self.contact_1.save()

        self.contact_2 = Contact.objects.create(
            email='inactive@test.com',
            country='Россия',
            city='Москва',
            street='Ломоносовская',
            number='21',
            contact_user=self.inactive_user
        )
        self.contact_2.save()

        # Создание объектов Sale (завод)
        self.sale_factory_1 = Sale.objects.create(
            unit='Завод',
            title='Завод 1',
            sale_user=self.user_test,
            product=self.product_1,
            contact=self.contact_1,
            debt=0.00,
        )
        self.sale_factory_1.save()

        self.sale_factory_2 = Sale.objects.create(
            unit='Завод',
            title='Завод 2',
            sale_user=self.inactive_user,
            product=self.product_2,
            contact=self.contact_2,
            debt=0.00,
        )
        self.sale_factory_2.save()

        # Создание объектов Sale (розничная сеть)
        self.sale_retail_1 = Sale.objects.create(
            unit='Розничная сеть',
            title='Розничная сеть 1',
            supplier=self.sale_factory_1,
            sale_user=self.user_test,
            product=self.product_1,
            contact=self.contact_1,
            debt=0.00,
        )
        self.sale_retail_1.save()

        self.sale_retail_2 = Sale.objects.create(
            unit='Розничная сеть',
            title='Розничная сеть 2',
            supplier=self.sale_factory_2,
            sale_user=self.user_test,
            product=self.product_2,
            contact=self.contact_2,
            debt=0.00,
        )
        self.sale_retail_2.save()

        # Создание объектов Sale (ИП)
        self.sale_businessman_1 = Sale.objects.create(
            unit='Индивидуальный предприниматель',
            title='Индивидуальный предприниматель 1',
            supplier=self.sale_retail_1,
            sale_user=self.user_test,
            product=self.product_1,
            contact=self.contact_1,
            debt=0.00,
        )
        self.sale_businessman_1.save()

        self.sale_businessman_2 = Sale.objects.create(
            unit='Индивидуальный предприниматель',
            title='Индивидуальный предприниматель 2',
            supplier=self.sale_retail_2,
            sale_user=self.user_test,
            product=self.product_2,
            contact=self.contact_2,
            debt=0.00,
        )
        self.sale_businessman_2.save()

    def tearDown(self) -> None:
        return super().tearDown()


class SaleCreateTestCase(SaleModelTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Получение маршрутов
        self.sale_create_url = '/sales/create/'

        # Данные для создания объекта Sale
        self.sale_create_data = {
            'title': 'Завод тестовый',
            'unit': 'Завод',
            'product': self.product_1.pk,
            'contact': self.contact_1.pk,
            'sale_user': 'test@test.com',
            'debt': 0.00
        }

    def test_user_can_create_sale_factory_correctly(self):
        """Активные пользователи могут создавать объекты модели Sale (завод) корректно."""

        # Количество объектов до создания
        self.assertTrue(
            Sale.objects.count() == 6
        )

        # POST-запрос на создание объекта
        response = self.client.post(
            self.sale_create_url,
            self.sale_create_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Количество объектов после создания
        self.assertTrue(
            Sale.objects.count() == 7
        )

    def test_user_cannot_create_sale_without_authentication(self):
        """Неавторизованные пользователи не могут создавать объекты Sale."""

        # POST-запрос на создание объекта
        response = self.client.post(
            self.sale_create_url,
            self.sale_create_data,
            headers=None,
            format='json'
        )

        # Получение статус-кода
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Получение содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )

    def test_inactive_user_cannot_create_sale_without_activation(self):
        """Неактивные пользователи не могут создавать объекты Sale."""

        # Отключение пользователя
        self.user_test.is_active = False
        self.user_test.save()

        # POST-запрос на создание объекта
        response = self.client.post(
            self.sale_create_url,
            self.sale_create_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Получение статус-кода
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Получение содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'Пользователь неактивен', 'code': 'user_inactive'}
        )

    def test_user_cannot_create_sale_factory_to_factory(self):
        """Пользователь не может создавать объекты Sale типа завод, поставщиком которого является другой завод."""

        # Данные для создания объекта Sale
        self.sale_create_factory_data = {
            'title': 'Завод тестовый',
            'unit': 'Завод',
            'supplier': self.sale_factory_1.pk,
            'product': self.product_1.pk,
            'contact': self.contact_1.pk,
            'sale_user': 'test@test.com',
            'debt': 0.00
        }

        # Количество объектов до создания
        self.assertTrue(
            Sale.objects.count() == 6
        )

        # POST-запрос на создание объекта
        response = self.client.post(
            self.sale_create_url,
            self.sale_create_factory_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Количество объектов после создания
        self.assertTrue(
            Sale.objects.count() == 6
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'supplier': ['Звено не может ссылаться на такой же тип звена.'],
             'supplier_factory': ['Звено "Завод" не может ссылаться на другие звенья.']}
        )

    def test_user_cannot_create_sale_retail_to_retail(self):
        """Пользователь не может создавать объекты Sale типа розничная сеть, поставщиком которого является
        другая розничная сеть."""

        # Данные для создания объекта Sale
        self.sale_create_retail_data = {
            'title': 'Розничная сеть тестовый',
            'unit': 'Розничная сеть',
            'supplier': self.sale_retail_1.pk,
            'product': self.product_1.pk,
            'contact': self.contact_1.pk,
            'sale_user': 'test@test.com',
            'debt': 0.00
        }

        # Количество объектов до создания
        self.assertTrue(
            Sale.objects.count() == 6
        )

        # POST-запрос на создание объекта
        response = self.client.post(
            self.sale_create_url,
            self.sale_create_retail_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Количество объектов после создания
        self.assertTrue(
            Sale.objects.count() == 6
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'supplier': ['Звено не может ссылаться на такой же тип звена.']}
        )

    def test_user_cannot_create_sale_businessman_to_businessman(self):
        """Пользователь не может создавать объекты Sale типа ИП, поставщиком которого является другой ИП."""

        self.businessman_test = Sale.objects.create(
            unit='Индивидуальный предприниматель',
            title='Индивидуальный предприниматель 10',
            supplier=self.sale_factory_1,
            sale_user=self.user_test,
            product=self.product_1,
            contact=self.contact_1,
            debt=0.00,
        )

        # Данные для создания объекта Sale
        self.sale_create_businessman_data = {
            'title': 'Индивидуальный предприниматель тестовый',
            'unit': 'Индивидуальный предприниматель',
            'supplier': self.businessman_test.pk,
            'product': self.product_1.pk,
            'contact': self.contact_1.pk,
            'sale_user': 'test@test.com',
            'debt': 0.00
        }

        # Количество объектов до создания
        self.assertTrue(
            Sale.objects.count() == 7
        )

        # POST-запрос на создание объекта
        response = self.client.post(
            self.sale_create_url,
            self.sale_create_businessman_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Количество объектов после создания
        self.assertTrue(
            Sale.objects.count() == 7
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'supplier': ['Звено не может ссылаться на такой же тип звена.']}
        )

    def test_user_cannot_create_sale_factory_with_supplier(self):
        """Пользователь не может создавать объект Sale типа завод, который имеет поставщика."""

        # Данные для создания объекта Sale
        self.sale_create_factory_data = {
            'title': 'Завод тестовый',
            'unit': 'Завод',
            'supplier': self.sale_retail_1.pk,
            'product': self.product_1.pk,
            'contact': self.contact_1.pk,
            'sale_user': 'test@test.com',
            'debt': 0.00
        }

        # Количество объектов до создания
        self.assertTrue(
            Sale.objects.count() == 6
        )

        # POST-запрос на создание объекта
        response = self.client.post(
            self.sale_create_url,
            self.sale_create_factory_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Количество объектов после создания
        self.assertTrue(
            Sale.objects.count() == 6
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'supplier_factory': ['Звено "Завод" не может ссылаться на другие звенья.']}
        )

    def test_user_cannot_create_sale_businessman_without_supplier(self):
        """Пользователь не может создавать объекты Sale типа ИП без поставщика."""

        # Данные для создания объекта Sale
        self.sale_create_businessman_data = {
            'title': 'Индивидуальный предприниматель тестовый',
            'unit': 'Индивидуальный предприниматель',
            'product': self.product_1.pk,
            'contact': self.contact_1.pk,
            'sale_user': 'test@test.com',
            'debt': 0.00
        }

        # Количество объектов до создания
        self.assertTrue(
            Sale.objects.count() == 6
        )

        # POST-запрос на создание объекта
        response = self.client.post(
            self.sale_create_url,
            self.sale_create_businessman_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Количество объектов после создания
        self.assertTrue(
            Sale.objects.count() == 6
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'supplier_empty': ['Выберете поставщика.']}
        )

    def test_user_cannot_create_sale_retail_without_supplier(self):
        """Пользователь не может создавать объекты Sale типа розничная сеть без поставщика."""

        # Данные для создания объекта Sale
        self.sale_create_retail_data = {
            'title': 'Розничная сеть тестовый',
            'unit': 'Розничная сеть',
            'product': self.product_1.pk,
            'contact': self.contact_1.pk,
            'sale_user': 'test@test.com',
            'debt': 0.00
        }

        # Количество объектов до создания
        self.assertTrue(
            Sale.objects.count() == 6
        )

        # POST-запрос на создание объекта
        response = self.client.post(
            self.sale_create_url,
            self.sale_create_retail_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Количество объектов после создания
        self.assertTrue(
            Sale.objects.count() == 6
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'supplier_empty': ['Выберете поставщика.']}
        )

    def test_user_cannot_create_sale_with_more_than_three_level_of_unit(self):
        """Пользователь не может создавать объект Sale со структурой данных, имеющей более 3 уровней вложенности."""

        # Данные для создания объекта Sale
        self.sale_create_retail_data = {
            'title': 'Розничная сеть тестовый',
            'unit': 'Розничная сеть',
            'product': self.product_1.pk,
            'contact': self.contact_1.pk,
            'supplier': self.sale_businessman_1.pk,
            'sale_user': 'test@test.com',
            'debt': 0.00
        }

        # Количество объектов до создания
        self.assertTrue(
            Sale.objects.count() == 6
        )

        # POST-запрос на создание объекта
        response = self.client.post(
            self.sale_create_url,
            self.sale_create_retail_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Количество объектов после создания
        self.assertTrue(
            Sale.objects.count() == 6
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'count_supplier': ['Уровень вложенности не должен превышать 3.']}
        )

    def test_user_cannot_create_sale_with_foreign_data(self):
        """Пользователь не может создавать объект Sale с чужими продуктами и контактами"""

        # Данные для создания объекта Sale
        self.sale_create_retail_data = {
            'title': 'Розничная сеть тестовый',
            'unit': 'Розничная сеть',
            'product': self.product_2.pk,
            'contact': self.contact_2.pk,
            'supplier': self.sale_factory_1.pk,
            'sale_user': 'test@test.com',
            'debt': 0.00
        }

        # Количество объектов до создания
        self.assertTrue(
            Sale.objects.count() == 6
        )

        # POST-запрос на создание объекта
        response = self.client.post(
            self.sale_create_url,
            self.sale_create_retail_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Количество объектов после создания
        self.assertTrue(
            Sale.objects.count() == 6
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'wrong_owner': ['Нельзя добавлять продукты чужих пользователей']}
        )


class SaleGetDetailTestCase(SaleModelTestCase):

    def setUp(self) -> None:
        super().setUp()

        # Получение маршрутов
        self.sale_detail_url = f'/sales/{self.sale_factory_1.pk}/'

    def test_user_can_get_detail_sale_factory_correctly(self):
        """Активные пользователи могут получить информацию об объекте модели Sale корректно."""

        # GET-запрос на получение информации об объекте
        response = self.client.get(
            self.sale_detail_url,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Проверка на создателя объекта
        self.assertEqual(
            response.json().get('sale_user'),
            'test@test.com'
        )

        # Проверка на получение всех полей
        self.assertEqual(
            len(list(response.json().keys())),
            9
        )

    def test_user_cannot_get_detail_sale_without_authentication(self):
        """Неавторизованные пользователи не могут получить информацию об объекте Sale."""

        # GET-запрос на получение информации об объекте
        response = self.client.get(
            self.sale_detail_url,
            headers=None,
            format='json'
        )

        # Получение статус-кода
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Получение содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )

    def test_inactive_user_cannot_get_detail_sale_without_activation(self):
        """Неактивные пользователи не могут получить информацию об объекте Sale."""

        # Отключение пользователя
        self.user_test.is_active = False
        self.user_test.save()

        # GET-запрос на получение информации об объекте
        response = self.client.get(
            self.sale_detail_url,
            headers=self.headers_user_1,
            format='json'
        )

        # Получение статус-кода
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Получение содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'Пользователь неактивен', 'code': 'user_inactive'}
        )

    def test_user_cannot_get_detail_sale_another_user(self):
        """Пользователи не могут получить информацию об объекте Sale чужих пользователей."""

        # GET-запрос на получение информации об объекте
        response = self.client.get(
            self.sale_detail_url,
            headers=self.headers_user_2,
            format='json'
        )

        # Получение статус-кода
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        # Получение содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
        )


class SaleGetListTestCase(SaleModelTestCase):

    def setUp(self) -> None:
        super().setUp()

        # Получение маршрутов
        self.sale_list_url = '/sales/'

    def test_user_can_get_sale_correctly(self):
        """Активные пользователи могут получить информацию об объектах модели Sale корректно."""

        # GET-запрос на получение информации
        response = self.client.get(
            self.sale_list_url,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Проверка на количество объектов
        self.assertEqual(
            Sale.objects.count(),
            len(response.json())
        )

    def test_user_cannot_get_list_sale_without_authentication(self):
        """Неавторизованные пользователи не могут получить информацию об объектах Sale."""

        # GET-запрос на получение объектов
        response = self.client.get(
            self.sale_list_url,
            headers=None,
            format='json'
        )

        # Получение статус-кода
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Получение содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )

    def test_inactive_user_cannot_get_list_sale_without_activation(self):
        """Неактивные пользователи не могут получить информацию об объектах Sale."""

        # Отключение пользователя
        self.user_test.is_active = False
        self.user_test.save()

        # GET-запрос на получение информации об объектах
        response = self.client.get(
            self.sale_list_url,
            headers=self.headers_user_1,
            format='json'
        )

        # Получение статус-кода
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Получение содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'Пользователь неактивен', 'code': 'user_inactive'}
        )


class SaleUpdateTestCase(SaleModelTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Получение маршрутов
        self.sale_update_url = f'/sales/update/{self.sale_retail_1.pk}/'

        # Данные для обновления объекта Sale
        self.sale_update_data = {
            'title': 'Розничная сеть тестовый',
            'unit': 'Розничная сеть',
            'supplier': self.sale_factory_1.pk,
            'product': self.product_1.pk,
            'contact': self.contact_1.pk,
            'sale_user': 'test@test.com',
            'debt': 0.00
        }

    def test_user_can_update_sale_correctly(self):
        """Активные пользователи могут изменять объекты модели Sale (розничная сеть) корректно."""

        # PATCH-запрос на изменение объекта
        response = self.client.patch(
            self.sale_update_url,
            self.sale_update_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Получение названия после изменения
        self.assertEqual(
            response.json().get('title'),
            'Розничная сеть тестовый'
        )

    def test_user_cannot_update_sale_without_authentication(self):
        """Неавторизованные пользователи не могут обновлять объекты Sale."""

        # PATCH-запрос на изменение объекта
        response = self.client.patch(
            self.sale_update_url,
            self.sale_update_data,
            headers=None,
            format='json'
        )

        # Получение статус-кода
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Получение содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )

    def test_inactive_user_cannot_update_sale_without_activation(self):
        """Неактивные пользователи не могут изменять объекты Sale."""

        # Отключение пользователя
        self.user_test.is_active = False
        self.user_test.save()

        # PATCH-запрос на изменение объекта
        response = self.client.patch(
            self.sale_update_url,
            self.sale_update_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Получение статус-кода
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Получение содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'Пользователь неактивен', 'code': 'user_inactive'}
        )

    def test_user_cannot_update_sale_from_retail_to_factory_with_supplier(self):
        """Пользователи не могут обновлять объекты Sale с <розничная сеть> на <завод> без удаления поставщика."""

        # Данные для обновления объекта Sale
        self.sale_update_test_data = {
            'title': 'Розничная сеть тестовый',
            'unit': 'Завод',
            'supplier': self.sale_factory_1.pk,
            'product': self.product_1.pk,
            'contact': self.contact_1.pk,
            'sale_user': 'test@test.com',
            'debt': 0.00
        }

        # PATCH-запрос на изменение объекта
        response = self.client.patch(
            self.sale_update_url,
            self.sale_update_test_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Получение статус-кода
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Получение содержимого ответа
        self.assertEqual(
            response.json(),
            {'supplier': ['Звено не может ссылаться на такой же тип звена.'],
             'supplier_factory': ['Звено "Завод" не может ссылаться на другие звенья.']}
        )

    def test_user_cannot_update_sales_another_user(self):
        """Активные пользователи не могут изменять детальную информацию объектов модели Sale чужих
        пользователей."""

        # PATCH-запрос на обновление объекта модели тестового пользователя вторым пользователем
        response = self.client.patch(
            self.sale_update_url,
            self.sale_update_data,
            headers=self.headers_user_2,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
        )

    def test_user_cannot_update_sales_field_debt(self):
        """Активные пользователи при изменении объекта Sale не могут изменить свою задолженность."""

        # Данные для обновления объекта Sale
        self.sale_update_test_data = {
            'title': 'Розничная сеть тестовый',
            'unit': 'Розничная сеть',
            'supplier': self.sale_factory_1.pk,
            'product': self.product_1.pk,
            'contact': self.contact_1.pk,
            'sale_user': 'test@test.com',
            'debt': 2000.00
        }

        # PATCH-запрос на изменение объекта
        response = self.client.patch(
            self.sale_update_url,
            self.sale_update_test_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Получение статус-кода
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Проверка задолженности
        self.assertNotEqual(
            self.sale_update_test_data.get('debt'),
            response.json().get('debt')
        )


class SaleDeleteTestCase(SaleModelTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Получение маршрутов
        self.sale_delete_url = f'/sales/delete/{self.sale_retail_1.pk}/'

    def test_user_can_delete_sale_correctly(self):
        """Активные пользователи могут удалять свои объекты модели Sale корректно."""

        # Количество объектов модели Sale до удаления
        self.assertTrue(
            Sale.objects.count() == 6
        )

        # DELETE-запрос на удаление объекта модели тестового пользователя
        response = self.client.delete(
            self.sale_delete_url,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        # Количество объектов модели Sale после удаления
        self.assertTrue(
            Sale.objects.count() == 5
        )

    def test_user_cannot_delete_sales_another_user(self):
        """Активные пользователи не могут удалять объекты модели Sale чужих пользователей."""

        # DELETE-запрос на удаление объекта модели тестового пользователя вторым пользователем
        response = self.client.delete(
            self.sale_delete_url,
            headers=self.headers_user_2,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'У вас недостаточно прав для выполнения данного действия.'}
        )

    def test_inactive_user_cannot_delete_sale_without_activation(self):
        """Неактивные пользователи не могут удалять объекты Sale."""

        # Отключение пользователя
        self.user_test.is_active = False
        self.user_test.save()

        # DELETE-запрос на удаление объекта
        response = self.client.delete(
            self.sale_delete_url,
            headers=self.headers_user_1,
            format='json'
        )

        # Получение статус-кода
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Получение содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'Пользователь неактивен', 'code': 'user_inactive'}
        )

    def test_user_cannot_delete_sales_without_authentication(self):
        """Неавторизованные пользователи не могут удалять объекты модели Sale."""

        # DELETE-запрос на удаление объекта модели тестового пользователя
        response = self.client.delete(
            self.sale_delete_url,
            headers=None,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # Проверка содержимого ответа
        self.assertEqual(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )
