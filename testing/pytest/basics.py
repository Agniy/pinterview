"""
Базовые примеры функций для тестирования с pytest
"""


class Calculator:
    """Простой калькулятор для демонстрации тестирования"""
    
    def add(self, a, b):
        """Сложение двух чисел"""
        return a + b
    
    def subtract(self, a, b):
        """Вычитание двух чисел"""
        return a - b
    
    def multiply(self, a, b):
        """Умножение двух чисел"""
        return a * b
    
    def divide(self, a, b):
        """Деление двух чисел"""
        if b == 0:
            raise ValueError("Деление на ноль невозможно!")
        return a / b
    
    def power(self, base, exponent):
        """Возведение в степень"""
        return base ** exponent


class User:
    """Класс пользователя для демонстрации"""
    
    def __init__(self, username, email, age=None):
        if not username:
            raise ValueError("Username не может быть пустым")
        if not email or '@' not in email:
            raise ValueError("Некорректный email")
        if age is not None and age < 0:
            raise ValueError("Возраст не может быть отрицательным")
        
        self.username = username
        self.email = email
        self.age = age
        self._is_active = True
    
    def activate(self):
        """Активировать пользователя"""
        self._is_active = True
    
    def deactivate(self):
        """Деактивировать пользователя"""
        self._is_active = False
    
    def is_active(self):
        """Проверить, активен ли пользователь"""
        return self._is_active
    
    def get_info(self):
        """Получить информацию о пользователе"""
        info = f"User: {self.username} ({self.email})"
        if self.age:
            info += f", Age: {self.age}"
        return info


class ShoppingCart:
    """Корзина покупок"""
    
    def __init__(self):
        self.items = []
    
    def add_item(self, item, quantity=1):
        """Добавить товар в корзину"""
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным")
        self.items.append({
            'name': item,
            'quantity': quantity
        })
    
    def remove_item(self, item):
        """Удалить товар из корзины"""
        self.items = [i for i in self.items if i['name'] != item]
    
    def get_total_items(self):
        """Получить общее количество товаров"""
        return sum(item['quantity'] for item in self.items)
    
    def is_empty(self):
        """Проверить, пуста ли корзина"""
        return len(self.items) == 0
    
    def clear(self):
        """Очистить корзину"""
        self.items = []


def validate_password(password):
    """
    Валидация пароля
    
    Правила:
    - Минимум 8 символов
    - Хотя бы одна заглавная буква
    - Хотя бы одна цифра
    - Хотя бы один специальный символ
    """
    if len(password) < 8:
        return False, "Пароль должен содержать минимум 8 символов"
    
    if not any(c.isupper() for c in password):
        return False, "Пароль должен содержать хотя бы одну заглавную букву"
    
    if not any(c.isdigit() for c in password):
        return False, "Пароль должен содержать хотя бы одну цифру"
    
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(c in special_chars for c in password):
        return False, "Пароль должен содержать хотя бы один специальный символ"
    
    return True, "Пароль валиден"


def is_palindrome(text):
    """Проверка, является ли строка палиндромом"""
    cleaned = ''.join(c.lower() for c in text if c.isalnum())
    return cleaned == cleaned[::-1]


def fibonacci(n):
    """Вычислить n-ое число Фибоначчи"""
    if n < 0:
        raise ValueError("n должно быть неотрицательным")
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def factorial(n):
    """Вычислить факториал числа"""
    if n < 0:
        raise ValueError("Факториал определен только для неотрицательных чисел")
    if n == 0 or n == 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

