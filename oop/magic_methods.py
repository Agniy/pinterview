"""
🟡 МАГИЧЕСКИЕ МЕТОДЫ - Вопросы и задачи для собеседований

Основные темы:
- __init__, __new__, __del__
- __str__, __repr__
- __eq__, __lt__, __gt__ и др.
- __len__, __getitem__, __setitem__
- __call__, __enter__, __exit__
- __add__, __sub__ и др. операторы
"""


# ============================================================================
# ТЕОРЕТИЧЕСКИЕ ВОПРОСЫ
# ============================================================================

"""
Q1: Что такое магические методы (dunder methods)?
A: Специальные методы с двойными подчеркиваниями (__method__),
определяющие поведение объектов в различных ситуациях.

Q2: В чем разница между __str__ и __repr__?
A:
- __str__ - читаемое для пользователя строковое представление
- __repr__ - однозначное представление для разработчика (должно быть воссоздаваемым)

Q3: Какие магические методы для сравнения?
A: __eq__, __ne__, __lt__, __le__, __gt__, __ge__

Q4: Что такое __call__?
A: Позволяет вызывать экземпляр класса как функцию

Q5: Зачем нужен __enter__ и __exit__?
A: Для реализации протокола контекстного менеджера (with statement)
"""


# ============================================================================
# ЗАДАЧА 1: Базовые методы представления
# ============================================================================

class Book:
    """
    🟢 Junior level
    Класс с __str__ и __repr__
    """
    
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
    
    def __str__(self):
        """Для пользователя"""
        return f'"{self.title}" by {self.author}'
    
    def __repr__(self):
        """Для разработчика"""
        return f"Book('{self.title}', '{self.author}', {self.pages})"


def demo_book():
    book = Book("1984", "George Orwell", 328)
    
    print(f"str(book): {str(book)}")
    print(f"repr(book): {repr(book)}")


# ============================================================================
# ЗАДАЧА 2: Методы сравнения
# ============================================================================

from functools import total_ordering

@total_ordering
class Person:
    """
    🟡 Middle level
    Класс с операторами сравнения (используя @total_ordering)
    """
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __eq__(self, other):
        """Равенство"""
        if not isinstance(other, Person):
            return NotImplemented
        return self.age == other.age
    
    def __lt__(self, other):
        """Меньше (остальные операторы генерируются автоматически)"""
        if not isinstance(other, Person):
            return NotImplemented
        return self.age < other.age
    
    def __str__(self):
        return f"{self.name} ({self.age})"


def demo_comparison():
    alice = Person("Alice", 30)
    bob = Person("Bob", 25)
    charlie = Person("Charlie", 30)
    
    print(f"{alice} == {charlie}: {alice == charlie}")
    print(f"{alice} > {bob}: {alice > bob}")
    print(f"{bob} < {alice}: {bob < alice}")
    
    people = [alice, bob, charlie]
    print(f"Отсортированные: {sorted(people, key=lambda p: p.age)}")


# ============================================================================
# ЗАДАЧА 3: Арифметические операторы
# ============================================================================

class Vector:
    """
    🟡 Middle level
    Вектор с арифметическими операторами
    """
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        """Сложение векторов"""
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        """Вычитание векторов"""
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        """Умножение на скаляр"""
        return Vector(self.x * scalar, self.y * scalar)
    
    def __abs__(self):
        """Длина вектора"""
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"


def demo_vector():
    v1 = Vector(2, 3)
    v2 = Vector(1, 1)
    
    print(f"v1 = {v1}")
    print(f"v2 = {v2}")
    print(f"v1 + v2 = {v1 + v2}")
    print(f"v1 - v2 = {v1 - v2}")
    print(f"v1 * 3 = {v1 * 3}")
    print(f"|v1| = {abs(v1):.2f}")


# ============================================================================
# ЗАДАЧА 4: Контейнерные методы
# ============================================================================

class CustomList:
    """
    🟡 Middle level
    Кастомный список с методами контейнера
    """
    
    def __init__(self, items=None):
        self.items = items if items is not None else []
    
    def __len__(self):
        """len(obj)"""
        return len(self.items)
    
    def __getitem__(self, index):
        """obj[index]"""
        return self.items[index]
    
    def __setitem__(self, index, value):
        """obj[index] = value"""
        self.items[index] = value
    
    def __delitem__(self, index):
        """del obj[index]"""
        del self.items[index]
    
    def __contains__(self, item):
        """item in obj"""
        return item in self.items
    
    def __iter__(self):
        """for item in obj"""
        return iter(self.items)
    
    def __reversed__(self):
        """reversed(obj)"""
        return reversed(self.items)
    
    def append(self, item):
        self.items.append(item)
    
    def __str__(self):
        return f"CustomList({self.items})"


def demo_custom_list():
    cl = CustomList([1, 2, 3, 4, 5])
    
    print(f"Список: {cl}")
    print(f"Длина: {len(cl)}")
    print(f"cl[2] = {cl[2]}")
    print(f"3 in cl: {3 in cl}")
    
    print("Итерация:")
    for item in cl:
        print(item, end=' ')
    print()


# ============================================================================
# ЗАДАЧА 5: __call__ - вызываемые объекты
# ============================================================================

class Multiplier:
    """
    🟡 Middle level
    Вызываемый объект для умножения
    """
    
    def __init__(self, factor):
        self.factor = factor
    
    def __call__(self, x):
        """Делает экземпляр вызываемым"""
        return x * self.factor


class Counter:
    """
    🟡 Middle level
    Счетчик вызовов
    """
    
    def __init__(self):
        self.count = 0
    
    def __call__(self):
        self.count += 1
        return self.count


def demo_callable():
    # Multiplier
    double = Multiplier(2)
    triple = Multiplier(3)
    
    print(f"double(5) = {double(5)}")
    print(f"triple(5) = {triple(5)}")
    
    # Counter
    counter = Counter()
    print(f"Вызов 1: {counter()}")
    print(f"Вызов 2: {counter()}")
    print(f"Вызов 3: {counter()}")


# ============================================================================
# ЗАДАЧА 6: Контекстный менеджер
# ============================================================================

class FileManager:
    """
    🔴 Senior level
    Контекстный менеджер для работы с файлами
    """
    
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        """Вход в контекст"""
        print(f"Открытие файла {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Выход из контекста"""
        print(f"Закрытие файла {self.filename}")
        if self.file:
            self.file.close()
        
        # Возвращаем False, чтобы исключение пробросилось дальше
        return False


class Timer:
    """
    🟡 Middle level
    Контекстный менеджер для измерения времени
    """
    
    def __enter__(self):
        import time
        self.start = time.time()
        return self
    
    def __exit__(self, *args):
        import time
        self.end = time.time()
        self.elapsed = self.end - self.start
        print(f"Время выполнения: {self.elapsed:.4f}с")
        return False


def demo_context_manager():
    # Timer
    print("Использование Timer:")
    with Timer() as timer:
        import time
        time.sleep(0.1)
        sum([i**2 for i in range(1000)])


# ============================================================================
# ЗАДАЧА 7: Атрибуты динамически
# ============================================================================

class DynamicAttributes:
    """
    🔴 Senior level
    Класс с динамическими атрибутами
    """
    
    def __init__(self):
        self._attributes = {}
    
    def __getattr__(self, name):
        """Вызывается, когда атрибут не найден"""
        if name in self._attributes:
            return self._attributes[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
    
    def __setattr__(self, name, value):
        """Вызывается при установке атрибута"""
        if name.startswith('_'):
            # Для приватных атрибутов используем обычное поведение
            super().__setattr__(name, value)
        else:
            self._attributes[name] = value
    
    def __delattr__(self, name):
        """Вызывается при удалении атрибута"""
        if name in self._attributes:
            del self._attributes[name]
        else:
            raise AttributeError(name)


def demo_dynamic_attrs():
    obj = DynamicAttributes()
    
    obj.name = "Alice"
    obj.age = 30
    
    print(f"name: {obj.name}")
    print(f"age: {obj.age}")
    
    del obj.age
    try:
        print(obj.age)
    except AttributeError as e:
        print(f"Ошибка: {e}")


# ============================================================================
# ЗАДАЧА 8: Дескрипторный класс
# ============================================================================

class ValidatedString:
    """
    🔴 Senior level
    Дескриптор для валидации строк
    """
    
    def __init__(self, min_length=0, max_length=100):
        self.min_length = min_length
        self.max_length = max_length
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, '')
    
    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} должно быть строкой")
        if len(value) < self.min_length:
            raise ValueError(f"{self.name} слишком короткое")
        if len(value) > self.max_length:
            raise ValueError(f"{self.name} слишком длинное")
        obj.__dict__[self.name] = value


class User:
    """Пользователь с валидацией"""
    
    username = ValidatedString(min_length=3, max_length=20)
    email = ValidatedString(min_length=5, max_length=100)
    
    def __init__(self, username, email):
        self.username = username
        self.email = email


def demo_descriptor():
    try:
        user = User("alice123", "alice@example.com")
        print(f"User: {user.username}, {user.email}")
        
        user.username = "ab"  # Слишком короткое
    except ValueError as e:
        print(f"Ошибка: {e}")


# ============================================================================
# ЗАДАЧА 9: Метаклассы через __init_subclass__
# ============================================================================

class PluginBase:
    """
    🔴 Senior level
    Базовый класс с автоматической регистрацией подклассов
    """
    
    plugins = {}
    
    def __init_subclass__(cls, plugin_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if plugin_name:
            cls.plugins[plugin_name] = cls


class ImagePlugin(PluginBase, plugin_name='image'):
    def process(self):
        return "Processing image"


class VideoPlugin(PluginBase, plugin_name='video'):
    def process(self):
        return "Processing video"


def demo_init_subclass():
    print("Зарегистрированные плагины:")
    for name, plugin_class in PluginBase.plugins.items():
        plugin = plugin_class()
        print(f"  {name}: {plugin.process()}")


# ============================================================================
# ЗАДАЧА 10: Полная реализация числового типа
# ============================================================================

class Fraction:
    """
    🔴 Senior level
    Дробь с полным набором операторов
    """
    
    def __init__(self, numerator, denominator):
        if denominator == 0:
            raise ValueError("Знаменатель не может быть 0")
        
        # Упрощаем дробь
        from math import gcd
        g = gcd(abs(numerator), abs(denominator))
        self.numerator = numerator // g
        self.denominator = denominator // g
        
        # Знак всегда в числителе
        if self.denominator < 0:
            self.numerator = -self.numerator
            self.denominator = -self.denominator
    
    def __add__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        return Fraction(
            self.numerator * other.denominator + other.numerator * self.denominator,
            self.denominator * other.denominator
        )
    
    def __sub__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        return Fraction(
            self.numerator * other.denominator - other.numerator * self.denominator,
            self.denominator * other.denominator
        )
    
    def __mul__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        return Fraction(
            self.numerator * other.numerator,
            self.denominator * other.denominator
        )
    
    def __truediv__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        return Fraction(
            self.numerator * other.denominator,
            self.denominator * other.numerator
        )
    
    def __eq__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        return (self.numerator == other.numerator and 
                self.denominator == other.denominator)
    
    def __float__(self):
        return self.numerator / self.denominator
    
    def __str__(self):
        return f"{self.numerator}/{self.denominator}"
    
    def __repr__(self):
        return f"Fraction({self.numerator}, {self.denominator})"


def demo_fraction():
    f1 = Fraction(1, 2)
    f2 = Fraction(1, 3)
    
    print(f"f1 = {f1}")
    print(f"f2 = {f2}")
    print(f"f1 + f2 = {f1 + f2}")
    print(f"f1 - f2 = {f1 - f2}")
    print(f"f1 * f2 = {f1 * f2}")
    print(f"f1 / f2 = {f1 / f2}")
    print(f"float(f1) = {float(f1)}")


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("МАГИЧЕСКИЕ МЕТОДЫ - Примеры и тесты")
    print("=" * 60)
    
    # Тест 1: __str__ и __repr__
    print("\n1. __str__ и __repr__:")
    demo_book()
    
    # Тест 2: Операторы сравнения
    print("\n2. Операторы сравнения:")
    demo_comparison()
    
    # Тест 3: Арифметические операторы
    print("\n3. Арифметические операторы (Vector):")
    demo_vector()
    
    # Тест 4: Контейнерные методы
    print("\n4. Контейнерные методы:")
    demo_custom_list()
    
    # Тест 5: __call__
    print("\n5. __call__ (вызываемые объекты):")
    demo_callable()
    
    # Тест 6: Контекстный менеджер
    print("\n6. Контекстный менеджер:")
    demo_context_manager()
    
    # Тест 7: Динамические атрибуты
    print("\n7. Динамические атрибуты:")
    demo_dynamic_attrs()
    
    # Тест 8: Дескрипторы
    print("\n8. Дескрипторы для валидации:")
    demo_descriptor()
    
    # Тест 9: __init_subclass__
    print("\n9. __init_subclass__ (регистрация плагинов):")
    demo_init_subclass()
    
    # Тест 10: Полная реализация числового типа
    print("\n10. Fraction (полная реализация):")
    demo_fraction()
    
    print("\n" + "=" * 60)

