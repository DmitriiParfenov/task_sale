# Create your tests here.
from rest_framework import status

from products.models import Product
from users.tests import UserModelTestCase


# Create your tests here.
class ProductModelTestCase(UserModelTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Создание объекта Product
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

        # Данные для создания Product
        self.product_create_data = {
            'title': 'Intel Core i5',
            'model': 'Процессоры',
            'release': '2023-12-29',
            'product_user': 'test@test.com',
        }

        # Данные для обновления Product
        self.product_update_data = {
            'title': 'Intel Core i9',
            'model': 'Процессоры',
            'release': '2024-12-29',
            'product_user': 'test@test.com',
        }

    def tearDown(self) -> None:
        return super().tearDown()


class ProductTestCase(ProductModelTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Получение маршрутов
        self.product_create_url = '/products/'
        self.product_list_url = '/products/'
        self.product_detail_url = f'/products/{self.product_1.pk}/'
        self.product_update_url = f'/products/{self.product_1.pk}/'
        self.product_delete_url = f'/products/{self.product_1.pk}/'

    def test_user_cannot_create_product_without_authentication(self):
        """Неавторизованные пользователи не могут создавать объекты Product."""

        # POST-запрос на создание объекта Product
        response = self.client.post(
            self.product_create_url,
            self.product_create_data,
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

    def test_inactive_user_cannot_create_product_without_activation(self):
        """Неактивные пользователи не могут создавать объекты Product."""

        # Отключение пользователя
        self.inactive_user.is_active = False
        self.inactive_user.save()

        # POST-запрос на создание объекта Product
        response = self.client.post(
            self.product_create_url,
            self.product_create_data,
            headers=self.headers_user_inactive,
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

    def test_user_can_create_products_correctly(self):
        """Активные пользователи могут создавать объекты модели Product корректно."""

        # Количество продуктов до создания
        self.assertTrue(
            Product.objects.count() == 2
        )

        # POST-запрос на создание продукта
        response = self.client.post(
            self.product_create_url,
            self.product_create_data,
            headers=self.headers_user_inactive,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Количество контактов после создания
        self.assertTrue(
            Product.objects.count() == 3
        )

    def test_user_can_get_product_correctly(self):
        """Активные пользователи могут получать информацию об объектах модели Product корректно."""

        # GET-запрос на получение всех продуктов
        response = self.client.get(
            self.product_list_url,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Проверка количества объектов в содержании ответа
        self.assertTrue(
            len(response.json()) == 2
        )

        # Проверка количества объектов в базе данных
        self.assertTrue(
            Product.objects.count() == 2
        )

    def test_user_cannot_get_products_without_authentication(self):
        """Неавторизованные пользователи не могут получать информацию об объектах модели Product."""

        # GET-запрос на получение всех продуктов
        response = self.client.get(
            self.product_list_url,
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

    def test_inactive_user_cannot_get_products_without_activation(self):
        """Неактивные пользователи не могут получить информацию об объектах Product."""

        # Отключение пользователя
        self.inactive_user.is_active = False
        self.inactive_user.save()

        # GET-запрос на создание объекта Product
        response = self.client.get(
            self.product_list_url,
            self.product_create_data,
            headers=self.headers_user_inactive,
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

    def test_user_can_get_detail_products_correctly_owner(self):
        """Активные пользователи могут получать детальную информацию об объектах модели Product, чьими
        владельцами они являются."""

        # GET-запрос на получение конкретного продукта
        response = self.client.get(
            self.product_detail_url,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Проверка на пользователя объекта Product
        self.assertEqual(
            response.json().get('product_user'),
            self.user_test.email
        )

    def test_user_cannot_get_detail_products_without_authentication(self):
        """Неавторизованные пользователи не могут получать детальную информацию об объекте модели Product."""

        # GET-запрос на получение конкретного продукта
        response = self.client.get(
            self.product_detail_url,
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

    def test_inactive_user_cannot_get_detail_products_without_activation(self):
        """Неактивные пользователи не могут получить информацию об объекте Product."""

        # Отключение пользователя
        self.inactive_user.is_active = False
        self.inactive_user.save()

        # GET-запрос на создание объекта Product
        response = self.client.get(
            self.product_detail_url,
            self.product_create_data,
            headers=self.headers_user_inactive,
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

    def test_user_cannot_detail_products_not_owner(self):
        """Активные пользователи не могут получать детальную информацию об объекте модели Product, чьими
        владельцами они не являются."""

        # GET-запрос на получение продукта тестового пользователя вторым пользователем
        response = self.client.get(
            self.product_detail_url,
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

    def test_user_cannot_update_products_without_authentication(self):
        """Неавторизованные пользователи не могут изменять детальную информацию объектов модели Product."""

        # PATCH-запрос на обновление объекта модели Product тестового пользователя
        response = self.client.patch(
            self.product_update_url,
            self.product_update_data,
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

    def test_inactive_user_cannot_update_products_without_activation(self):
        """Неактивные пользователи не могут изменить информацию об объекте Product."""

        # Получение объекта модели Product, созданного неактивным пользователем
        self.product_update_2_url = f'/contacts/{self.product_2.pk}/'

        # Отключение пользователя
        self.inactive_user.is_active = False
        self.inactive_user.save()

        # PATCH-запрос на создание объекта Contact
        response = self.client.patch(
            self.product_update_2_url,
            self.product_update_data,
            headers=self.headers_user_inactive,
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

    def test_user_cannot_update_products_another_user(self):
        """Активные пользователи не могут изменять детальную информацию объектов модели Product чужих
        пользователей."""

        # PATCH-запрос на обновление объекта модели тестового пользователя вторым пользователем
        response = self.client.patch(
            self.product_update_url,
            self.product_update_data,
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

    def test_user_can_update_products_correctly(self):
        """Активные пользователи могут изменять детальную информацию объектов модели Product корректно."""

        # Получение названия города до изменения
        self.assertEqual(
            self.product_1.model,
            'Яблоки'
        )

        # PATCH-запрос на обновление объекта модели тестового пользователя
        response = self.client.patch(
            self.product_update_url,
            self.product_update_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Получение модели после изменения
        self.assertEqual(
            response.json().get('model'),
            'Процессоры'
        )

    def test_user_cannot_delete_products_without_authentication(self):
        """Неавторизованные пользователи не могут удалять объекты модели Product."""

        # DELETE-запрос на удаление объекта модели тестового пользователя
        response = self.client.delete(
            self.product_delete_url,
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

    def test_inactive_user_cannot_delete_products_without_activation(self):
        """Неактивные пользователи не могут удалять информацию об объекте Product."""

        # Получение объекта модели Product, созданного неактивным пользователем
        self.product_update_2_url = f'/contacts/{self.product_2.pk}/'

        # Отключение пользователя
        self.inactive_user.is_active = False
        self.inactive_user.save()

        # DELETE-запрос на создание объекта Product
        response = self.client.delete(
            self.product_delete_url,
            headers=self.headers_user_inactive,
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

    def test_user_cannot_delete_products_another_user(self):
        """Активные пользователи не могут удалять объекты модели Product чужих пользователей."""

        # DELETE-запрос на удаление объекта модели тестового пользователя вторым пользователем
        response = self.client.delete(
            self.product_delete_url,
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

    def test_user_can_delete_products_correctly(self):
        """Авторизованные пользователи могут удалять объекты модели Product корректно."""

        # Количество объектов модели Product до удаления
        self.assertTrue(
            Product.objects.count() == 2
        )

        # DELETE-запрос на удаление объекта модели тестового пользователя
        response = self.client.delete(
            self.product_delete_url,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        # Количество объектов модели Product после удаления
        self.assertTrue(
            Product.objects.count() == 1
        )
