# Create your tests here.
from rest_framework import status

from contacts.models import Contact
from users.tests import UserModelTestCase


# Create your tests here.
class ContactModelTestCase(UserModelTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Создание объекта Contact
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

        # Данные для создания Contact
        self.contact_create_data = {
            'email': 'another@test.com',
            'country': 'Россия',
            'city': 'Воронеж',
            'street': 'Воронежская',
            'number': '2',
            'contact_user': 'another@test.com'
        }

        # Данные для обновления Contact
        self.contact_update_data = {
            'email': 'test@test.com',
            'country': 'Россия',
            'city': 'Воронеж',
            'street': 'Воронежская',
            'number': '5',
            'contact_user': 'test@test.com'
        }

    def tearDown(self) -> None:
        return super().tearDown()


class ContactTestCase(ContactModelTestCase):
    def setUp(self) -> None:
        super().setUp()

        # Получение маршрутов
        self.contact_create_url = '/contacts/'
        self.contact_list_url = '/contacts/'
        self.contact_detail_url = f'/contacts/{self.contact_1.pk}/'
        self.contact_update_url = f'/contacts/{self.contact_1.pk}/'
        self.contact_delete_url = f'/contacts/{self.contact_1.pk}/'

    def test_user_cannot_create_contacts_without_authentication(self):
        """Неавторизованные пользователи не могут создавать объекты Contacts."""

        # POST-запрос на создание объекта Contact
        response = self.client.post(
            self.contact_create_url,
            self.contact_create_data,
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

    def test_inactive_user_cannot_create_contacts_without_activation(self):
        """Неактивные пользователи не могут создавать объекты Contacts."""

        # Отключение пользователя
        self.inactive_user.is_active = False
        self.inactive_user.save()

        # POST-запрос на создание объекта Contact
        response = self.client.post(
            self.contact_create_url,
            self.contact_create_data,
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

    def test_user_can_create_contacts_correctly(self):
        """Активные пользователи могут создавать объекты модели Contacts корректно."""

        # Количество контактов до создания
        self.assertTrue(
            Contact.objects.count() == 2
        )

        # POST-запрос на создание контакта
        response = self.client.post(
            self.contact_create_url,
            self.contact_create_data,
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
            Contact.objects.count() == 3
        )

    def test_user_can_get_contacts_correctly(self):
        """Активные пользователи могут получать информацию об объектах модели Contacts корректно."""

        # GET-запрос на получение всех контактов
        response = self.client.get(
            self.contact_list_url,
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
            Contact.objects.count() == 2
        )

    def test_user_cannot_get_contacts_without_authentication(self):
        """Неавторизованные пользователи не могут получать информацию об объектах модели Contacts."""

        # GET-запрос на получение всех модулей
        response = self.client.get(
            self.contact_list_url,
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

    def test_inactive_user_cannot_get_contacts_without_activation(self):
        """Неактивные пользователи не могут получить информацию об объектах Contacts."""

        # Отключение пользователя
        self.inactive_user.is_active = False
        self.inactive_user.save()

        # GET-запрос на создание объекта Contact
        response = self.client.get(
            self.contact_list_url,
            self.contact_create_data,
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

    def test_user_can_get_detail_contacts_correctly_owner(self):
        """Активные пользователи могут получать детальную информацию об объектах модели Contacts, чьими
        владельцами они являются."""

        # GET-запрос на получение конкретного контакта
        response = self.client.get(
            self.contact_detail_url,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Проверка на пользователя объекта Contacts
        self.assertEqual(
            response.json().get('email'),
            self.user_test.email
        )

    def test_user_cannot_get_detail_contacts_without_authentication(self):
        """Неавторизованные пользователи не могут получать детальную информацию об объекте модели Contacts."""

        # GET-запрос на получение конкретного контакта
        response = self.client.get(
            self.contact_detail_url,
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

    def test_inactive_user_cannot_get_detail_contacts_without_activation(self):
        """Неактивные пользователи не могут получить информацию об объекте Contacts."""

        # Отключение пользователя
        self.inactive_user.is_active = False
        self.inactive_user.save()

        # GET-запрос на создание объекта Contact
        response = self.client.get(
            self.contact_detail_url,
            self.contact_create_data,
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

    def test_user_cannot_detail_contacts_not_owner(self):
        """Активные пользователи не могут получать детальную информацию об объекте модели Contacts, чьими
        владельцами они не являются."""

        # GET-запрос на получение модуля тестового пользователя вторым пользователем
        response = self.client.get(
            self.contact_detail_url,
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

    def test_user_cannot_update_contacts_without_authentication(self):
        """Неавторизованные пользователи не могут изменять детальную информацию объектов модели Contacts."""

        # PATCH-запрос на обновление объекта модели Contacts тестового пользователя
        response = self.client.patch(
            self.contact_update_url,
            self.contact_update_data,
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

    def test_inactive_user_cannot_update_contacts_without_activation(self):
        """Неактивные пользователи не могут изменить информацию об объекте Contacts."""

        # Получение объекта модели Contact, созданного неактивным пользователем
        self.contact_update_2_url = f'/contacts/{self.contact_2.pk}/'

        # Отключение пользователя
        self.inactive_user.is_active = False
        self.inactive_user.save()

        # PATCH-запрос на создание объекта Contact
        response = self.client.patch(
            self.contact_update_2_url,
            self.contact_update_data,
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

    def test_user_cannot_update_contacts_another_user(self):
        """Активные пользователи не могут изменять детальную информацию объектов модели Contacts чужих
        пользователей."""

        # PATCH-запрос на обновление объекта модели тестового пользователя вторым пользователем
        response = self.client.patch(
            self.contact_update_url,
            self.contact_update_data,
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

    def test_user_can_update_contacts_correctly(self):
        """Активные пользователи могут изменять детальную информацию объектов модели Contacts корректно."""

        # Получение названия города до изменения
        self.assertEqual(
            self.contact_1.city,
            'СПб'
        )

        # PATCH-запрос на обновление объекта модели тестового пользователя
        response = self.client.patch(
            self.contact_update_url,
            self.contact_update_data,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Получение названия города после изменения
        self.assertEqual(
            response.json().get('city'),
            'Воронеж'
        )

    def test_user_cannot_delete_contacts_without_authentication(self):
        """Неавторизованные пользователи не могут удалять объекты модели Contacts."""

        # DELETE-запрос на удаление объекта модели тестового пользователя
        response = self.client.delete(
            self.contact_delete_url,
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

    def test_inactive_user_cannot_delete_contacts_without_activation(self):
        """Неактивные пользователи не могут удалять информацию об объекте Contacts."""

        # Получение объекта модели Contact, созданного неактивным пользователем
        self.contact_update_2_url = f'/contacts/{self.contact_2.pk}/'

        # Отключение пользователя
        self.inactive_user.is_active = False
        self.inactive_user.save()

        # DELETE-запрос на создание объекта Contact
        response = self.client.delete(
            self.contact_delete_url,
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

    def test_user_cannot_delete_contacts_another_user(self):
        """Активные пользователи не могут удалять объекты модели Contacts чужих пользователей."""

        # DELETE-запрос на удаление объекта модели тестового пользователя вторым пользователем
        response = self.client.delete(
            self.contact_delete_url,
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

    def test_user_can_delete_contacts_correctly(self):
        """Авторизованные пользователи могут удалять объекты модели Contacts корректно."""

        # Количество объектов модели Contact до удаления
        self.assertTrue(
            Contact.objects.count() == 2
        )

        # DELETE-запрос на удаление объекта модели тестового пользователя
        response = self.client.delete(
            self.contact_delete_url,
            headers=self.headers_user_1,
            format='json'
        )

        # Проверка статус кода
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        # Количество объектов модели Contact после удаления
        self.assertTrue(
            Contact.objects.count() == 1
        )
