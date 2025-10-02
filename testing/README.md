# Testing - Тестирование в Python

Эта папка содержит материалы по различным аспектам тестирования в Python.

## 📚 Содержание

### [pytest/](pytest/)
Полное руководство по pytest - самому популярному фреймворку для тестирования в Python.

**Что включает:**
- 📖 Подробное руководство по pytest
- 💡 Базовые и продвинутые примеры
- 🔧 Работа с фикстурами
- 🎯 Параметризация тестов
- 🔨 Моки и патчи
- ⚡ Асинхронное тестирование
- 📊 Покрытие кода

**Файлы:**
- `README.md` - полное руководство по pytest
- `QUICK_START.md` - быстрый старт
- `basics.py` + `test_basics.py` - базовые примеры
- `advanced_examples.py` + `test_advanced.py` - продвинутые примеры
- `test_fixtures_demo.py` - демонстрация фикстур
- `conftest.py` - общие фикстуры
- `pytest.ini` - конфигурация pytest
- `requirements.txt` - зависимости

## 🚀 Быстрый старт

```bash
# Перейти в папку pytest
cd testing/pytest

# Установить зависимости
pip install -r requirements.txt

# Запустить все тесты
pytest

# Запустить с покрытием кода
pytest --cov=. --cov-report=html
```

## 📖 Типы тестирования

### 1. **Unit Testing (Модульное тестирование)**
Тестирование отдельных компонентов кода в изоляции.

```python
def test_calculator_add():
    calc = Calculator()
    assert calc.add(2, 3) == 5
```

### 2. **Integration Testing (Интеграционное тестирование)**
Тестирование взаимодействия между компонентами.

```python
def test_database_and_cache_integration(db, cache):
    db.insert('users', user_data)
    cache.set('user:1', user_data)
    assert db.select('users')[0] == cache.get('user:1')
```

### 3. **Functional Testing (Функциональное тестирование)**
Тестирование функциональности системы с точки зрения пользователя.

### 4. **End-to-End Testing (E2E тестирование)**
Тестирование всей системы от начала до конца.

## 🎯 Лучшие практики тестирования

### 1. **Следуйте AAA паттерну**
```python
def test_example():
    # Arrange (Подготовка)
    user = User("John")
    
    # Act (Действие)
    result = user.get_name()
    
    # Assert (Проверка)
    assert result == "John"
```

### 2. **Один тест - одна проверка**
```python
# ✅ Хорошо
def test_user_name():
    assert user.name == "John"

def test_user_age():
    assert user.age == 30

# ❌ Плохо - слишком много проверок в одном тесте
def test_user():
    assert user.name == "John"
    assert user.age == 30
    assert user.email == "john@example.com"
    # ... еще 10 проверок
```

### 3. **Используйте описательные имена**
```python
# ✅ Хорошо
def test_user_cannot_login_with_invalid_password():
    pass

# ❌ Плохо
def test_login():
    pass
```

### 4. **Изолируйте тесты**
Каждый тест должен быть независимым и не полагаться на результаты других тестов.

### 5. **Используйте фикстуры для повторяющегося кода**
```python
@pytest.fixture
def user():
    return User("John", age=30)

def test_user_name(user):
    assert user.name == "John"
```

### 6. **Тестируйте граничные случаи**
```python
@pytest.mark.parametrize("value", [0, -1, 1, 999, 1000, 1001])
def test_validate_number(value):
    # Тестируем граничные значения
    pass
```

## 🔧 Полезные инструменты

### Фреймворки для тестирования:
- **pytest** ⭐ - Рекомендуется (самый популярный)
- **unittest** - Встроенный в Python
- **nose2** - Альтернатива pytest
- **doctest** - Тесты в docstrings

### Инструменты для покрытия кода:
- **coverage.py** - Измерение покрытия кода
- **pytest-cov** - Плагин pytest для покрытия

### Моки и патчи:
- **unittest.mock** - Встроенный модуль для моков
- **pytest-mock** - Плагин pytest для моков
- **responses** - Мокирование HTTP запросов
- **freezegun** - Заморозка времени

### Для веб-приложений:
- **pytest-django** - Тестирование Django
- **pytest-flask** - Тестирование Flask
- **selenium** - E2E тестирование браузера
- **playwright** - Современная альтернатива Selenium

### Генерация тестовых данных:
- **faker** - Генерация фейковых данных
- **factory_boy** - Фабрики для создания тестовых объектов
- **hypothesis** - Property-based тестирование

## 📊 Метрики качества тестов

### Покрытие кода (Code Coverage)
```bash
# Запустить с покрытием
pytest --cov=. --cov-report=html

# Минимальное покрытие: 80%+ рекомендуется
# 100% покрытия не всегда необходимо
```

### Скорость выполнения тестов
```bash
# Показать самые медленные тесты
pytest --durations=10

# Параллельное выполнение
pytest -n auto
```

## 🎓 Рекомендуемый порядок изучения

1. **Начните с pytest/QUICK_START.md** - быстрый старт
2. **Изучите pytest/README.md** - полное руководство
3. **Практикуйтесь с примерами:**
   - `test_basics.py` - базовые тесты
   - `test_advanced.py` - продвинутые техники
   - `test_fixtures_demo.py` - работа с фикстурами
4. **Пишите свои тесты** для существующего кода

## 📚 Дополнительные ресурсы

### Документация:
- [Pytest Documentation](https://docs.pytest.org/)
- [Python Testing Guide](https://docs.python.org/3/library/unittest.html)
- [Testing Best Practices](https://realpython.com/python-testing/)

### Книги:
- "Python Testing with pytest" by Brian Okken
- "Test-Driven Development with Python" by Harry Percival

### Статьи:
- [Real Python - Testing](https://realpython.com/python-testing/)
- [The Hitchhiker's Guide to Python - Testing](https://docs.python-guide.org/writing/tests/)

## 🎯 Основные концепции

### Test-Driven Development (TDD)
1. **Red** - Напишите тест, который падает
2. **Green** - Напишите минимальный код, чтобы тест прошел
3. **Refactor** - Улучшите код

### Behavior-Driven Development (BDD)
Описание тестов на понятном языке:
```gherkin
Given a user with name "John"
When the user logs in
Then the user should see the dashboard
```

### Property-Based Testing
Тестирование с автоматической генерацией данных:
```python
from hypothesis import given, strategies as st

@given(st.integers(), st.integers())
def test_add_commutative(a, b):
    assert add(a, b) == add(b, a)
```

## 🚦 CI/CD Integration

### GitHub Actions
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          pip install -r requirements.txt
          pytest --cov=. --cov-report=xml
```

## ⚡ Производительность

### Советы по ускорению тестов:
1. Используйте параллельное выполнение (`pytest-xdist`)
2. Используйте правильный scope для фикстур
3. Мокируйте медленные операции (API, БД)
4. Разделяйте быстрые и медленные тесты

```bash
# Запустить только быстрые тесты
pytest -m "not slow"
```

## 🎨 Стиль кода в тестах

```python
# ✅ Хорошо - читаемый и понятный тест
def test_user_registration_with_valid_data():
    """
    Проверяет успешную регистрацию пользователя
    с корректными данными
    """
    # Arrange
    user_data = {
        'username': 'john_doe',
        'email': 'john@example.com',
        'password': 'SecurePass123!'
    }
    
    # Act
    result = register_user(user_data)
    
    # Assert
    assert result.success is True
    assert result.user_id is not None

# ❌ Плохо - неясно что тестируется
def test1():
    assert register_user({'username': 'a', 'email': 'b', 'password': 'c'})
```

---

## 📝 Заметки

- Тесты - это инвестиция в качество кода
- Хорошие тесты служат документацией
- Тесты помогают в рефакторинге
- 100% покрытие != 100% качество
- Пишите тесты, которые легко читать и поддерживать

---

**Удачи в тестировании! 🚀**

