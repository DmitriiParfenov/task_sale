from rest_framework import serializers


class SupplierValidator:
    """Валидирует поля <unit> и <supplier>. Если звено ссылает на аналогичный тип звена, то возбудится исключение.
    Поле <unit> типа <Завод> не может иметь поставщика, в ином случае возбудится исключение. Поля <unit>, тип которых
    отличны от <Завод> должны иметь поставщика, в ином случае возбудится исключение. Иерархичная структура данных должна
    иметь не больше 3 уровней вложенности, иначе возбудится исключение."""

    def __init__(self, unit, supplier):
        self.unit = unit
        self.supplier = supplier

    def __call__(self, value):
        error = {}
        counter = 0
        unit = value.get(self.unit)
        supplier = value.get(self.supplier)
        if supplier and unit == supplier.unit:
            error['supplier'] = 'Звено не может ссылаться на такой же тип звена.'
        if unit == 'Завод' and supplier:
            error['supplier_factory'] = 'Звено "Завод" не может ссылаться на другие звенья.'
        if unit != 'Завод' and not supplier:
            error['supplier_empty'] = 'Выберете поставщика.'
        while supplier:
            supplier = supplier.supplier
            counter += 1
        if counter >= 3:
            error['count_supplier'] = 'Уровень вложенности не должен превышать 3.'
        if error:
            raise serializers.ValidationError(error)


class ProductValidator:
    """Валидирует поля <product_user> и <sale_user>. Пользователь при создании объекта модели Sale не может ссылаться
    на объекты модели Product, чьими владельцами он не является."""

    def __init__(self, product_user, sale_user):
        self.product = product_user
        self.sale = sale_user

    def __call__(self, value):
        errors = {}
        product = value.get('product')
        sale_user = value.get('sale_user')
        if product.product_user != sale_user:
            errors['wrong_owner'] = 'Нельзя добавлять продукты чужих пользователей'
        if errors:
            raise serializers.ValidationError(errors)


class ContactValidator:
    """Валидирует поля <contact> и <sale_user>. Пользователь при создании объекта модели Sale не может ссылаться
    на объекты модели Contact, чьими владельцами он не является."""

    def __init__(self, contact, sale_user):
        self.product = contact
        self.sale = sale_user

    def __call__(self, value):
        errors = {}
        contact = value.get('contact')
        sale_user = value.get('sale_user')
        if contact.contact_user != sale_user:
            errors['wrong_owner'] = 'Нельзя добавлять контакты чужих пользователей'
        if errors:
            raise serializers.ValidationError(errors)
