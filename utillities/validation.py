import re

class Validator:
    @staticmethod
    def validate_name(name: str) -> bool:
        """
        Проверяет корректность имени, фамилии, отчества.
        Допускаются только буквы русского или латинского алфавита, дефис и пробел.
        """
        if not name:
            return False
        pattern = r"^[A-Za-zА-Яа-яЁё\- ]{2,50}$"
        return bool(re.match(pattern, name.strip()))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """
        Проверяет корректность номера телефона.
        +7XXXXXXXXXX
        """
        if not phone:
            return False
        pattern = r"^(\+?\d{1,3})?[ -]?\(?\d{3,5}\)?[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}$"
        return bool(re.match(pattern, phone.strip()))

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Проверяет корректность корпоративной почты.
        """
        if not email:
            return False
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        return bool(re.match(pattern, email.strip()))

    @staticmethod
    def validate_class_id(class_id) -> bool:
        """
        Проверяет, что class_id — целое положительное число.
        """
        try:
            return int(class_id) > 0
        except (TypeError, ValueError):
            return False

    @staticmethod
    def validate_locker_id(locker_id) -> bool:
        """
        Проверяет, что id_locker — целое положительное число.
        """
        try:
            return int(locker_id) > 0
        except (TypeError, ValueError):
            return False

    @staticmethod
    def validate_student_data(data: dict) -> dict:
        """
        Комплексная проверка всех полей студента.
        Возвращает словарь с ошибками, если есть.
        """
        errors = {}

        if not Validator.validate_name(data.get("first_name", "")):
            errors["first_name"] = "Некорректное имя"
        if not Validator.validate_name(data.get("last_name", "")):
            errors["last_name"] = "Некорректная фамилия"
        if data.get("middle_name") and not Validator.validate_name(data["middle_name"]):
            errors["middle_name"] = "Некорректное отчество"
        if data.get("phone_number") and not Validator.validate_phone(data["phone_number"]):
            errors["phone_number"] = "Некорректный номер телефона"
        if data.get("corp_email") and not Validator.validate_email(data["corp_email"]):
            errors["corp_email"] = "Некорректный адрес электронной почты"
        if not Validator.validate_class_id(data.get("class_id", 0)):
            errors["class_id"] = "Некорректный идентификатор класса"
        if not Validator.validate_locker_id(data.get("id_locker", 0)):
            errors["id_locker"] = "Некорректный номер шкафчика"

        return errors
