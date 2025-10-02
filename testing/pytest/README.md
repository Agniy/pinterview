# Pytest - Полное руководство по тестированию в Python

## Содержание
1. [Введение](#введение)
2. [Установка](#установка)
3. [Основы](#основы)
4. [Именование тестов](#именование-тестов)
5. [Запуск тестов](#запуск-тестов)
6. [Assertions (Утверждения)](#assertions-утверждения)
7. [Фикстуры (Fixtures)](#фикстуры-fixtures)
8. [Параметризация тестов](#параметризация-тестов)
9. [Маркеры (Markers)](#маркеры-markers)
10. [Исключения](#исключения)
11. [Моки и патчи](#моки-и-патчи)
12. [Лучшие практики](#лучшие-практики)

---

## Введение

**Pytest** — это мощный и популярный фреймворк для тестирования в Python. Он предоставляет простой синтаксис, богатую функциональность и множество плагинов.

### Преимущества pytest:
- ✅ Простой и понятный синтаксис
- ✅ Автоматическое обнаружение тестов
- ✅ Детальные отчеты об ошибках
- ✅ Фикстуры для управления состоянием
- ✅ Параметризация тестов
- ✅ Богатая экосистема плагинов

---

## Установка

```bash
# Установка pytest
pip install pytest

# Установка с дополнительными плагинами
pip install pytest pytest-cov pytest-mock pytest-asyncio
```

---

## Основы

### Простой тест

```python
# test_simple.py
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
```

### Структура теста

```python
def test_example():
    # 1. Arrange (Подготовка)
    x = 5
    y = 10
    
    # 2. Act (Действие)
    result = x + y
    
    # 3. Assert (Проверка)
    assert result == 15
```

---

## Именование тестов

### Правила именования:
1. Файлы с тестами должны начинаться с `test_` или заканчиваться `_test.py`
2. Функции тестов должны начинаться с `test_`
3. Классы тестов должны начинаться с `Test` (без `__init__`)

```python
# ✅ Правильно
test_user.py
user_test.py

def test_user_creation():
    pass

class TestUser:
    def test_login(self):
        pass

# ❌ Неправильно
user.py
def check_user():
    pass
```

---

## Запуск тестов

```bash
# Запустить все тесты в текущей директории
pytest

# Запустить конкретный файл
pytest test_basics.py

# Запустить конкретный тест
pytest test_basics.py::test_function_name

# Запустить тесты в классе
pytest test_basics.py::TestClass

# Запустить с подробным выводом
pytest -v

# Запустить с выводом print
pytest -s

# Запустить с покрытием кода
pytest --cov=.

# Остановиться на первой ошибке
pytest -x

# Запустить только последние упавшие тесты
pytest --lf

# Запустить в параллель (требует pytest-xdist)
pytest -n auto
```

---

## Assertions (Утверждения)

Pytest использует стандартный `assert` Python с улучшенными сообщениями об ошибках.

```python
def test_assertions():
    # Сравнение значений
    assert 1 + 1 == 2
    
    # Проверка на True/False
    assert True
    assert not False
    
    
    # Проверка вхождения
    assert 'hello' in 'hello world'
    
    # Проверка типов
    assert isinstance([], list)
    
    # Сравнение коллекций
    assert [1, 2, 3] == [1, 2, 3]
    assert {'a': 1} == {'a': 1}
    
    # Приблизительное сравнение для float
    from pytest import approx
    assert 0.1 + 0.2 == approx(0.3)
    
    # С пользовательским сообщением
    x = 5
    assert x > 10, f"Значение {x} должно быть больше 10"
```

---

## Фикстуры (Fixtures)

Фикстуры — это функции, которые выполняются перед тестами для подготовки данных или окружения.

### Базовые фикстуры

```python
import pytest

@pytest.fixture
def sample_data():
    """Фикстура с тестовыми данными"""
    return [1, 2, 3, 4, 5]

def test_sum(sample_data):
    assert sum(sample_data) == 15

def test_length(sample_data):
    assert len(sample_data) == 5
```

### Фикстуры с setup/teardown

```python
import pytest

@pytest.fixture
def database_connection():
    # Setup - выполняется перед тестом
    print("\nПодключение к базе данных")
    db = {"connected": True}
    
    yield db  # Передаем объект в тест
    
    # Teardown - выполняется после теста
    print("\nЗакрытие соединения с базой данных")
    db["connected"] = False
```

### Scope фикстур

```python
@pytest.fixture(scope="function")  # По умолчанию - для каждого теста
def function_scope():
    return "function"

@pytest.fixture(scope="class")  # Один раз для класса
def class_scope():
    return "class"

@pytest.fixture(scope="module")  # Один раз для модуля
def module_scope():
    return "module"

@pytest.fixture(scope="session")  # Один раз для всей сессии
def session_scope():
    return "session"
```

### Автоиспользуемые фикстуры

```python
@pytest.fixture(autouse=True)
def reset_state():
    """Автоматически выполняется перед каждым тестом"""
    print("\nСброс состояния")
```

---

## Параметризация тестов

Параметризация позволяет запускать один тест с разными входными данными.

```python
import pytest

@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_addition(a, b, expected):
    assert a + b == expected

@pytest.mark.parametrize("value", [1, 2, 3, 4, 5])
def test_is_positive(value):
    assert value > 0

# Комбинированная параметризация
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [3, 4])
def test_multiply(x, y):
    # Создаст 4 теста: (1,3), (1,4), (2,3), (2,4)
    assert x * y > 0
```

---

## Маркеры (Markers)

Маркеры позволяют помечать и фильтровать тесты.

```python
import pytest

@pytest.mark.slow
def test_slow_operation():
    """Медленный тест"""
    pass

@pytest.mark.skip(reason="Еще не реализовано")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="Не работает на Windows")
def test_unix_only():
    pass

@pytest.mark.xfail(reason="Известная ошибка")
def test_known_bug():
    assert False

# Запуск только помеченных тестов
# pytest -m slow
# pytest -m "not slow"
```

---

## Исключения

Проверка, что код выбрасывает исключения.

```python
import pytest

def divide(a, b):
    if b == 0:
        raise ValueError("Деление на ноль!")
    return a / b

def test_division_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
    
    # С проверкой сообщения
    with pytest.raises(ValueError, match="Деление на ноль"):
        divide(10, 0)
    
    # С получением информации об исключении
    with pytest.raises(ValueError) as exc_info:
        divide(10, 0)
    assert "ноль" in str(exc_info.value)
```

---

## Моки и патчи

Использование `unittest.mock` и `pytest-mock` для создания заглушек.

```python
from unittest.mock import Mock, patch, MagicMock
import pytest

def test_mock_example():
    # Создание мок-объекта
    mock_obj = Mock()
    mock_obj.method.return_value = 42
    
    assert mock_obj.method() == 42
    mock_obj.method.assert_called_once()

def fetch_data_from_api():
    # Реальный API запрос
    import requests
    response = requests.get("https://api.example.com/data")
    return response.json()

@patch('requests.get')
def test_api_call(mock_get):
    # Настройка мока
    mock_response = Mock()
    mock_response.json.return_value = {'data': 'test'}
    mock_get.return_value = mock_response
    
    # Тестирование
    result = fetch_data_from_api()
    assert result == {'data': 'test'}
    mock_get.assert_called_once_with("https://api.example.com/data")
```

---

## Лучшие практики

### 1. Один assert на тест (когда возможно)
```python
# ✅ Хорошо
def test_user_name():
    user = User("John")
    assert user.name == "John"

def test_user_age():
    user = User("John", age=30)
    assert user.age == 30

# ⚠️ Приемлемо для связанных проверок
def test_user_creation():
    user = User("John", age=30)
    assert user.name == "John"
    assert user.age == 30
```

### 2. Используйте описательные имена
```python
# ✅ Хорошо
def test_user_cannot_login_with_wrong_password():
    pass

# ❌ Плохо
def test_login():
    pass
```

### 3. Следуйте паттерну AAA
```python
def test_shopping_cart():
    # Arrange (Подготовка)
    cart = ShoppingCart()
    item = Item("Book", 10.0)
    
    # Act (Действие)
    cart.add_item(item)
    
    # Assert (Проверка)
    assert cart.total() == 10.0
```

### 4. Изолируйте тесты
```python
# Каждый тест должен быть независимым
# Не полагайтесь на порядок выполнения тестов
```

### 5. Используйте фикстуры для повторяющегося кода
```python
@pytest.fixture
def user():
    return User("John", age=30)

def test_user_name(user):
    assert user.name == "John"

def test_user_age(user):
    assert user.age == 30
```

### 6. Настройте pytest.ini или pyproject.toml
```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
markers =
    slow: медленные тесты
    integration: интеграционные тесты
    unit: юнит-тесты
```

---

## Структура проекта

```
project/
├── src/
│   ├── __init__.py
│   └── calculator.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Общие фикстуры
│   ├── test_calculator.py
│   └── integration/
│       └── test_integration.py
├── pytest.ini
└── requirements.txt
```

---

## Полезные команды

```bash
# Показать доступные фикстуры
pytest --fixtures

# Показать доступные маркеры
pytest --markers

# Сгенерировать HTML отчет (требует pytest-html)
pytest --html=report.html

# Запустить с профилированием (требует pytest-profiling)
pytest --profile

# Запустить только упавшие тесты из предыдущего запуска
pytest --lf

# Запустить упавшие тесты первыми
pytest --ff

# Показать самые медленные тесты
pytest --durations=10
```

---

## Полезные плагины

- `pytest-cov` — покрытие кода
- `pytest-mock` — улучшенные моки
- `pytest-asyncio` — тестирование асинхронного кода
- `pytest-xdist` — параллельное выполнение тестов
- `pytest-html` — HTML отчеты
- `pytest-timeout` — таймауты для тестов
- `pytest-django` — тестирование Django приложений
- `pytest-flask` — тестирование Flask приложений

---

## Примеры использования

См. файлы в этой директории:
- `basics.py` и `test_basics.py` — базовые примеры
- `advanced_examples.py` и `test_advanced.py` — продвинутые техники
- `fixtures_example.py` и `test_fixtures.py` — работа с фикстурами
- `conftest.py` — общие фикстуры для всех тестов

