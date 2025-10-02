# Pytest - Быстрый старт

## Установка

```bash
# Установка pytest
pip install pytest

# Или установка всех зависимостей из requirements.txt
pip install -r requirements.txt
```

## Запуск тестов

```bash
# Запустить все тесты в текущей директории
pytest

# Запустить конкретный файл
pytest test_basics.py

# Запустить с подробным выводом
pytest -v

# Запустить с выводом print
pytest -s

# Запустить конкретный тест
pytest test_basics.py::test_function_name

# Запустить тесты в классе
pytest test_basics.py::TestClassName

# Запустить только медленные тесты
pytest -m slow

# Запустить все кроме медленных тестов
pytest -m "not slow"

# Запустить с покрытием кода
pytest --cov=. --cov-report=html

# Остановиться на первой ошибке
pytest -x

# Запустить в параллель (4 процесса)
pytest -n 4
```

## Структура простого теста

```python
# test_example.py

def add(a, b):
    return a + b

def test_add():
    """Простой тест функции сложения"""
    assert add(2, 3) == 5
    assert add(0, 0) == 0
    assert add(-1, 1) == 0
```

## Запуск примеров из этой папки

```bash
# 1. Установите зависимости
pip install -r requirements.txt

# 2. Запустите все тесты
pytest

# 3. Запустите с покрытием кода
pytest --cov=. --cov-report=html

# 4. Откройте отчет о покрытии (создается файл htmlcov/index.html)
# В Linux/Mac:
open htmlcov/index.html
# В Windows:
start htmlcov/index.html
```

## Полезные команды

```bash
# Показать доступные фикстуры
pytest --fixtures

# Показать доступные маркеры
pytest --markers

# Запустить только упавшие тесты из предыдущего запуска
pytest --lf

# Показать 10 самых медленных тестов
pytest --durations=10

# Запустить с HTML отчетом
pytest --html=report.html --self-contained-html
```

## Следующие шаги

1. Прочитайте [README.md](README.md) для подробного руководства
2. Изучите примеры в файлах:
   - `test_basics.py` - базовые примеры
   - `test_advanced.py` - продвинутые техники
   - `test_fixtures_demo.py` - работа с фикстурами
3. Экспериментируйте с кодом!

## Дополнительные ресурсы

- [Официальная документация pytest](https://docs.pytest.org/)
- [Список плагинов pytest](https://docs.pytest.org/en/latest/reference/plugin_list.html)
- [Real Python: Pytest Tutorial](https://realpython.com/pytest-python-testing/)

