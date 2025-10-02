"""
🟡 ДЕКОРАТОРЫ (Decorators) - Вопросы и задачи для собеседований

Основные темы:
- Функции высшего порядка
- Замыкания
- Декораторы функций
- Декораторы с параметрами
- Декораторы классов
- functools.wraps
"""

import time
import functools
from typing import Callable


# ============================================================================
# ТЕОРЕТИЧЕСКИЕ ВОПРОСЫ
# ============================================================================

"""
Q1: Что такое декоратор?
A: Функция, которая принимает функцию и возвращает новую функцию,
расширяя/изменяя поведение исходной функции без её модификации.

Q2: Что такое замыкание (closure)?
A: Функция, которая запоминает значения из окружающей области видимости,
даже после завершения внешней функции.

Q3: Зачем нужен functools.wraps?
A: Сохраняет метаданные (имя, docstring и т.д.) оригинальной функции
при создании декоратора.

Q4: Можно ли применить несколько декораторов к одной функции?
A: Да, они применяются снизу вверх:
@decorator1
@decorator2
def func(): ...
эквивалентно: decorator1(decorator2(func))

Q5: Что такое декоратор с параметрами?
A: Функция, которая принимает параметры и возвращает декоратор.
"""


# ============================================================================
# ЗАДАЧА 1: Простой декоратор - таймер
# ============================================================================

def timer(func):
    """
    🟢 Junior level
    Декоратор для измерения времени выполнения функции
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} выполнилась за {end - start:.4f}с")
        return result
    return wrapper


@timer
def slow_function():
    """Медленная функция для тестирования"""
    time.sleep(0.1)
    return "Done"


# ============================================================================
# ЗАДАЧА 2: Декоратор с логированием
# ============================================================================

def logger(func):
    """
    🟢 Junior level
    Логирует вызовы функции с аргументами
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Вызов {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"{func.__name__} вернула {result!r}")
        return result
    return wrapper


@logger
def add(a, b):
    """Складывает два числа"""
    return a + b


# ============================================================================
# ЗАДАЧА 3: Декоратор для подсчета вызовов
# ============================================================================

def count_calls(func):
    """
    🟡 Middle level
    Подсчитывает количество вызовов функции
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1
        print(f"Вызов #{wrapper.call_count} функции {func.__name__}")
        return func(*args, **kwargs)
    
    wrapper.call_count = 0
    return wrapper


@count_calls
def say_hello():
    return "Hello!"


# ============================================================================
# ЗАДАЧА 4: Декоратор с параметрами - повторитель
# ============================================================================

def repeat(times=2):
    """
    🟡 Middle level
    Декоратор с параметром - повторяет выполнение функции
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for i in range(times):
                print(f"Вызов {i+1}/{times}")
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


@repeat(times=3)
def greet(name):
    print(f"Hello, {name}!")


# ============================================================================
# ЗАДАЧА 5: Кеширующий декоратор (Memoization)
# ============================================================================

def memoize(func):
    """
    🔴 Senior level
    Кеширует результаты функции
    """
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        else:
            print(f"Возврат из кеша для {args}")
        return cache[args]
    
    wrapper.cache = cache
    wrapper.cache_clear = lambda: cache.clear()
    return wrapper


@memoize
def fibonacci(n):
    """Вычисляет число Фибоначчи"""
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


# Альтернатива - встроенный lru_cache
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci_lru(n):
    """Фибоначчи с встроенным кешем"""
    if n < 2:
        return n
    return fibonacci_lru(n-1) + fibonacci_lru(n-2)


# ============================================================================
# ЗАДАЧА 6: Декоратор для проверки типов
# ============================================================================

def type_check(*expected_types):
    """
    🟡 Middle level
    Проверяет типы аргументов функции
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Проверяем позиционные аргументы
            for arg, expected_type in zip(args, expected_types):
                if not isinstance(arg, expected_type):
                    raise TypeError(
                        f"Ожидался {expected_type.__name__}, "
                        f"получен {type(arg).__name__}"
                    )
            return func(*args, **kwargs)
        return wrapper
    return decorator


@type_check(int, int)
def multiply(a, b):
    return a * b


# ============================================================================
# ЗАДАЧА 7: Декоратор для повторных попыток
# ============================================================================

def retry(max_attempts=3, delay=1):
    """
    🔴 Senior level
    Повторяет вызов функции при ошибке
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Попытка {attempt + 1} провалилась: {e}")
                    print(f"Повтор через {delay}с...")
                    time.sleep(delay)
        return wrapper
    return decorator


@retry(max_attempts=3, delay=0.5)
def unstable_function():
    """Функция, которая может упасть"""
    import random
    if random.random() < 0.7:
        raise ValueError("Случайная ошибка!")
    return "Успех!"


# ============================================================================
# ЗАДАЧА 8: Декоратор-синглтон
# ============================================================================

def singleton(cls):
    """
    🔴 Senior level
    Декоратор класса для реализации паттерна Singleton
    """
    instances = {}
    
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance


@singleton
class Database:
    """Класс базы данных - должен быть только один экземпляр"""
    
    def __init__(self):
        print("Инициализация базы данных")
        self.connection = "Connected"


# ============================================================================
# ЗАДАЧА 9: Декоратор для валидации
# ============================================================================

def validate_range(min_val, max_val):
    """
    🟡 Middle level
    Проверяет, что результат функции в допустимом диапазоне
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if not (min_val <= result <= max_val):
                raise ValueError(
                    f"Результат {result} вне диапазона [{min_val}, {max_val}]"
                )
            return result
        return wrapper
    return decorator


@validate_range(0, 100)
def calculate_percentage(part, whole):
    return (part / whole) * 100


# ============================================================================
# ЗАДАЧА 10: Декоратор для rate limiting
# ============================================================================

def rate_limit(max_calls, time_window):
    """
    🔴 Senior level
    Ограничивает количество вызовов функции за промежуток времени
    """
    def decorator(func):
        calls = []
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            
            # Удаляем старые вызовы
            calls[:] = [c for c in calls if now - c < time_window]
            
            if len(calls) >= max_calls:
                raise Exception(
                    f"Превышен лимит: {max_calls} вызовов за {time_window}с"
                )
            
            calls.append(now)
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


@rate_limit(max_calls=3, time_window=5)
def api_call():
    return "API ответ"


# ============================================================================
# ЗАДАЧА 11: Декоратор для депрекации
# ============================================================================

import warnings

def deprecated(reason):
    """
    🟡 Middle level
    Помечает функцию как устаревшую
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"{func.__name__} устарела. {reason}",
                category=DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator


@deprecated("Используйте new_function() вместо этого")
def old_function():
    return "Старая функция"


# ============================================================================
# ЗАДАЧА 12: Комбинирование декораторов
# ============================================================================

@timer
@logger
@count_calls
def complex_function(x, y):
    """Функция с несколькими декораторами"""
    time.sleep(0.1)
    return x + y


# ============================================================================
# ЗАДАЧА 13: Класс как декоратор
# ============================================================================

class CallCounter:
    """
    🟡 Middle level
    Декоратор-класс для подсчета вызовов
    """
    
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Вызов #{self.count}")
        return self.func(*args, **kwargs)


@CallCounter
def test_function():
    return "Test"


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("ДЕКОРАТОРЫ - Примеры и тесты")
    print("=" * 60)
    
    # Тест 1: Таймер
    print("\n1. Декоратор-таймер:")
    slow_function()
    
    # Тест 2: Логгер
    print("\n2. Декоратор-логгер:")
    add(5, 3)
    
    # Тест 3: Счетчик вызовов
    print("\n3. Счетчик вызовов:")
    say_hello()
    say_hello()
    say_hello()
    
    # Тест 4: Повторитель
    print("\n4. Декоратор с параметрами (повтор):")
    greet("Alice")
    
    # Тест 5: Мемоизация
    print("\n5. Кеширование (Memoization):")
    print(f"fibonacci(10) = {fibonacci(10)}")
    print(f"fibonacci(10) снова = {fibonacci(10)}")
    
    # Тест 6: Проверка типов
    print("\n6. Проверка типов:")
    print(f"multiply(5, 3) = {multiply(5, 3)}")
    try:
        multiply("5", 3)
    except TypeError as e:
        print(f"Ошибка: {e}")
    
    # Тест 7: Синглтон
    print("\n7. Singleton:")
    db1 = Database()
    db2 = Database()
    print(f"db1 is db2: {db1 is db2}")
    
    # Тест 8: Валидация
    print("\n8. Валидация диапазона:")
    print(f"50 из 100 = {calculate_percentage(50, 100)}%")
    try:
        calculate_percentage(150, 100)
    except ValueError as e:
        print(f"Ошибка: {e}")
    
    # Тест 9: Комбинирование
    print("\n9. Комбинирование декораторов:")
    complex_function(10, 20)
    
    # Тест 10: Класс-декоратор
    print("\n10. Класс как декоратор:")
    test_function()
    test_function()
    
    print("\n" + "=" * 60)

