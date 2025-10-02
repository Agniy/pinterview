"""
Тесты для базовых примеров

Демонстрирует основные возможности pytest:
- Простые assertions
- Тестирование исключений
- Параметризация тестов
- Группировка тестов в классы
"""

import pytest
from .basics import (
    Calculator, User, ShoppingCart,
    validate_password, is_palindrome,
    fibonacci, factorial
)


# ============= Тесты калькулятора =============

class TestCalculator:
    """Группа тестов для класса Calculator"""
    
    def test_add(self):
        """Тест сложения"""
        calc = Calculator()
        assert calc.add(2, 3) == 5
        assert calc.add(-1, 1) == 0
        assert calc.add(0, 0) == 0
    
    def test_subtract(self):
        """Тест вычитания"""
        calc = Calculator()
        assert calc.subtract(5, 3) == 2
        assert calc.subtract(0, 5) == -5
        assert calc.subtract(10, 10) == 0
    
    def test_multiply(self):
        """Тест умножения"""
        calc = Calculator()
        assert calc.multiply(3, 4) == 12
        assert calc.multiply(0, 100) == 0
        assert calc.multiply(-2, 5) == -10
    
    def test_divide(self):
        """Тест деления"""
        calc = Calculator()
        assert calc.divide(10, 2) == 5
        assert calc.divide(9, 3) == 3
        assert calc.divide(7, 2) == 3.5
    
    def test_divide_by_zero(self):
        """Тест деления на ноль - должно выбрасываться исключение"""
        calc = Calculator()
        with pytest.raises(ValueError, match="Деление на ноль"):
            calc.divide(10, 0)
    
    def test_power(self):
        """Тест возведения в степень"""
        calc = Calculator()
        assert calc.power(2, 3) == 8
        assert calc.power(5, 0) == 1
        assert calc.power(10, 2) == 100


# ============= Тесты пользователя =============

class TestUser:
    """Группа тестов для класса User"""
    
    def test_create_user(self):
        """Тест создания пользователя"""
        user = User("john_doe", "john@example.com", age=25)
        assert user.username == "john_doe"
        assert user.email == "john@example.com"
        assert user.age == 25
    
    def test_user_without_age(self):
        """Тест создания пользователя без возраста"""
        user = User("jane", "jane@example.com")
        assert user.username == "jane"
        assert user.age is None
    
    def test_empty_username(self):
        """Тест создания пользователя с пустым username"""
        with pytest.raises(ValueError, match="Username не может быть пустым"):
            User("", "test@example.com")
    
    def test_invalid_email(self):
        """Тест создания пользователя с некорректным email"""
        with pytest.raises(ValueError, match="Некорректный email"):
            User("test", "invalid-email")
    
    def test_negative_age(self):
        """Тест создания пользователя с отрицательным возрастом"""
        with pytest.raises(ValueError, match="Возраст не может быть отрицательным"):
            User("test", "test@example.com", age=-5)
    
    def test_user_activation(self):
        """Тест активации/деактивации пользователя"""
        user = User("test", "test@example.com")
        assert user.is_active() is True
        
        user.deactivate()
        assert user.is_active() is False
        
        user.activate()
        assert user.is_active() is True
    
    def test_get_info(self):
        """Тест получения информации о пользователе"""
        user = User("john", "john@example.com", age=30)
        info = user.get_info()
        assert "john" in info
        assert "john@example.com" in info
        assert "30" in info


# ============= Тесты корзины покупок =============

class TestShoppingCart:
    """Группа тестов для класса ShoppingCart"""
    
    def test_empty_cart(self):
        """Тест пустой корзины"""
        cart = ShoppingCart()
        assert cart.is_empty() is True
        assert cart.get_total_items() == 0
    
    def test_add_item(self):
        """Тест добавления товара"""
        cart = ShoppingCart()
        cart.add_item("Apple", 3)
        assert cart.is_empty() is False
        assert cart.get_total_items() == 3
    
    def test_add_multiple_items(self):
        """Тест добавления нескольких товаров"""
        cart = ShoppingCart()
        cart.add_item("Apple", 3)
        cart.add_item("Banana", 2)
        cart.add_item("Orange", 5)
        assert cart.get_total_items() == 10
    
    def test_remove_item(self):
        """Тест удаления товара"""
        cart = ShoppingCart()
        cart.add_item("Apple", 3)
        cart.add_item("Banana", 2)
        
        cart.remove_item("Apple")
        assert cart.get_total_items() == 2
    
    def test_clear_cart(self):
        """Тест очистки корзины"""
        cart = ShoppingCart()
        cart.add_item("Apple", 3)
        cart.add_item("Banana", 2)
        
        cart.clear()
        assert cart.is_empty() is True
    
    def test_add_item_with_zero_quantity(self):
        """Тест добавления товара с нулевым количеством"""
        cart = ShoppingCart()
        with pytest.raises(ValueError, match="Количество должно быть положительным"):
            cart.add_item("Apple", 0)


# ============= Параметризованные тесты =============

@pytest.mark.parametrize("text, expected", [
    ("radar", True),
    ("level", True),
    ("hello", False),
    ("A man a plan a canal Panama", True),
    ("race car", True),
    ("Python", False),
    ("", True),  # Пустая строка - палиндром
])
def test_palindrome(text, expected):
    """Параметризованный тест проверки палиндромов"""
    assert is_palindrome(text) == expected


@pytest.mark.parametrize("n, expected", [
    (0, 0),
    (1, 1),
    (2, 1),
    (3, 2),
    (4, 3),
    (5, 5),
    (6, 8),
    (7, 13),
    (10, 55),
])
def test_fibonacci(n, expected):
    """Параметризованный тест чисел Фибоначчи"""
    assert fibonacci(n) == expected


def test_fibonacci_negative():
    """Тест Фибоначчи с отрицательным числом"""
    with pytest.raises(ValueError):
        fibonacci(-1)


@pytest.mark.parametrize("n, expected", [
    (0, 1),
    (1, 1),
    (2, 2),
    (3, 6),
    (4, 24),
    (5, 120),
    (6, 720),
])
def test_factorial(n, expected):
    """Параметризованный тест факториала"""
    assert factorial(n) == expected


def test_factorial_negative():
    """Тест факториала с отрицательным числом"""
    with pytest.raises(ValueError):
        factorial(-1)


# ============= Тесты валидации пароля =============

class TestPasswordValidation:
    """Группа тестов для валидации пароля"""
    
    def test_valid_password(self):
        """Тест валидного пароля"""
        is_valid, message = validate_password("SecurePass123!")
        assert is_valid is True
    
    def test_too_short_password(self):
        """Тест слишком короткого пароля"""
        is_valid, message = validate_password("Short1!")
        assert is_valid is False
        assert "8 символов" in message
    
    def test_no_uppercase(self):
        """Тест пароля без заглавных букв"""
        is_valid, message = validate_password("password123!")
        assert is_valid is False
        assert "заглавную букву" in message
    
    def test_no_digit(self):
        """Тест пароля без цифр"""
        is_valid, message = validate_password("SecurePass!")
        assert is_valid is False
        assert "цифру" in message
    
    def test_no_special_char(self):
        """Тест пароля без специальных символов"""
        is_valid, message = validate_password("SecurePass123")
        assert is_valid is False
        assert "специальный символ" in message
    
    @pytest.mark.parametrize("password", [
        "ValidPass1!",
        "Str0ng#Pass",
        "MyP@ssw0rd",
        "Test1234!@#$",
    ])
    def test_multiple_valid_passwords(self, password):
        """Параметризованный тест валидных паролей"""
        is_valid, message = validate_password(password)
        assert is_valid is True


# ============= Демонстрация различных assertions =============

def test_various_assertions():
    """Демонстрация различных типов проверок"""
    
    # Числовые сравнения
    assert 5 > 3
    assert 10 >= 10
    assert 2 < 5
    assert 3 <= 3
    
    # Строки
    assert "hello" == "hello"
    assert "world" in "hello world"
    assert "python".startswith("py")
    assert "test".endswith("st")
    
    # Списки
    assert [1, 2, 3] == [1, 2, 3]
    assert 2 in [1, 2, 3]
    assert len([1, 2, 3]) == 3
    
    # Словари
    assert {'a': 1, 'b': 2} == {'b': 2, 'a': 1}
    assert 'a' in {'a': 1, 'b': 2}
    
    # Типы
    assert isinstance(5, int)
    assert isinstance("test", str)
    assert isinstance([1, 2], list)
    
    # None
    value = None
    assert value is None
    
    # Boolean
    assert True
    assert not False
    
    # Приблизительное сравнение для float
    assert 0.1 + 0.2 == pytest.approx(0.3)
    assert 3.14159 == pytest.approx(3.14, abs=0.01)


# ============= Использование маркеров =============

@pytest.mark.slow
def test_slow_operation():
    """Пример медленного теста (помечен маркером @pytest.mark.slow)"""
    import time
    time.sleep(0.1)  # Имитация медленной операции
    assert True


@pytest.mark.skip(reason="Функция еще не реализована")
def test_future_feature():
    """Тест, который пропускается"""
    pass


@pytest.mark.skipif(True, reason="Пример условного пропуска")
def test_conditional_skip():
    """Тест с условным пропуском"""
    pass

