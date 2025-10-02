"""
🟢 КОРТЕЖИ (Tuples) - Вопросы и задачи для собеседований

Основные темы:
- Неизменяемость (immutability)
- Named tuples
- Распаковка (unpacking)
- Сравнение с list
"""

from collections import namedtuple
from typing import NamedTuple


# ============================================================================
# ТЕОРЕТИЧЕСКИЕ ВОПРОСЫ
# ============================================================================

"""
Q1: В чем разница между tuple и list?
A:
- tuple неизменяемый (immutable), list изменяемый (mutable)
- tuple быстрее, занимает меньше памяти
- tuple можно использовать как ключ словаря
- tuple гарантирует, что данные не изменятся

Q2: Почему tuple неизменяемый, но может содержать изменяемые объекты?
A: Неизменяемость означает, что нельзя изменить идентичность объектов в tuple,
но содержимое изменяемых объектов можно менять.

Q3: Как создать tuple с одним элементом?
A: Нужна запятая: (element,) не (element)

Q4: Что такое named tuple?
A: Tuple с именованными полями, доступными как атрибуты.
Создается через collections.namedtuple или typing.NamedTuple

Q5: Что такое tuple unpacking?
A: Присваивание элементов tuple переменным: a, b, c = (1, 2, 3)

Q6: Можно ли изменить tuple?
A: Нет, но можно создать новый tuple с изменениями
"""


# ============================================================================
# ЗАДАЧА 1: Основы работы с tuple
# ============================================================================

def tuple_basics():
    """
    🟢 Junior level
    Демонстрация основных операций с кортежами
    """
    
    # Создание
    t1 = (1, 2, 3)
    t2 = 1, 2, 3  # Скобки опциональны
    t3 = (1,)  # Один элемент - обязательна запятая
    empty = ()
    
    print(f"Tuple: {t1}")
    print(f"Без скобок: {t2}")
    print(f"Один элемент: {t3}")
    print(f"Пустой: {empty}")
    
    # Индексация и срезы
    print(f"\nПервый элемент: {t1[0]}")
    print(f"Последний: {t1[-1]}")
    print(f"Срез [1:]: {t1[1:]}")
    
    # Конкатенация
    t4 = t1 + (4, 5)
    print(f"\nКонкатенация: {t1} + (4, 5) = {t4}")
    
    # Повторение
    t5 = t1 * 2
    print(f"Повторение: {t1} * 2 = {t5}")
    
    # Методы
    t6 = (1, 2, 2, 3, 2)
    print(f"\nКоличество 2: {t6.count(2)}")
    print(f"Индекс первой 2: {t6.index(2)}")


# ============================================================================
# ЗАДАЧА 2: Tuple unpacking
# ============================================================================

def unpacking_examples():
    """
    🟢 Junior level
    Примеры распаковки кортежей
    """
    
    # Базовая распаковка
    coordinates = (10, 20)
    x, y = coordinates
    print(f"Координаты: x={x}, y={y}")
    
    # Обмен значений
    a, b = 5, 10
    a, b = b, a
    print(f"После обмена: a={a}, b={b}")
    
    # Распаковка с *
    first, *middle, last = (1, 2, 3, 4, 5)
    print(f"first={first}, middle={middle}, last={last}")
    
    # Игнорирование значений
    name, _, age = ("Alice", "ignored", 30)
    print(f"name={name}, age={age}")
    
    # Вложенная распаковка
    person = ("Alice", (30, "Engineer"))
    name, (age, job) = person
    print(f"name={name}, age={age}, job={job}")


# ============================================================================
# ЗАДАЧА 3: Named Tuples
# ============================================================================

def namedtuple_examples():
    """
    🟡 Middle level
    Примеры использования named tuples
    """
    
    # Создание через collections.namedtuple
    Point = namedtuple('Point', ['x', 'y'])
    p1 = Point(10, 20)
    print(f"Point: {p1}")
    print(f"Доступ: p1.x={p1.x}, p1.y={p1.y}")
    print(f"По индексу: p1[0]={p1[0]}")
    
    # Создание из словаря
    Person = namedtuple('Person', ['name', 'age', 'city'])
    data = {'name': 'Alice', 'age': 30, 'city': 'NYC'}
    alice = Person(**data)
    print(f"\nPerson: {alice}")
    
    # _fields, _asdict(), _replace()
    print(f"Поля: {alice._fields}")
    print(f"Как словарь: {alice._asdict()}")
    alice_new = alice._replace(age=31)
    print(f"После замены: {alice_new}")


class PersonTyped(NamedTuple):
    """
    🟡 Middle level
    Typed NamedTuple (Python 3.6+) с аннотациями типов
    """
    name: str
    age: int
    city: str = "Unknown"  # Значение по умолчанию
    
    def greet(self):
        return f"Hello, I'm {self.name} from {self.city}"


def typed_namedtuple_example():
    """
    Пример использования typed NamedTuple
    """
    bob = PersonTyped("Bob", 25, "LA")
    print(f"\nTyped NamedTuple: {bob}")
    print(f"Метод: {bob.greet()}")
    
    # С дефолтным значением
    charlie = PersonTyped("Charlie", 28)
    print(f"С дефолтом: {charlie}")


# ============================================================================
# ЗАДАЧА 4: Tuple как ключ словаря
# ============================================================================

def tuple_as_dict_key():
    """
    🟢 Junior level
    Использование tuple как ключа словаря
    """
    
    # Координаты -> значение
    grid = {
        (0, 0): "origin",
        (1, 0): "right",
        (0, 1): "up",
        (1, 1): "diagonal"
    }
    
    print("Grid:")
    for coords, value in grid.items():
        print(f"  {coords}: {value}")
    
    # Доступ
    print(f"\nЗначение в (1, 1): {grid[(1, 1)]}")


# ============================================================================
# ЗАДАЧА 5: Сортировка кортежей
# ============================================================================

def sort_tuples():
    """
    🟡 Middle level
    Сортировка списка кортежей
    """
    
    students = [
        ("Alice", 25, 85),
        ("Bob", 22, 90),
        ("Charlie", 25, 80),
        ("David", 22, 95)
    ]
    
    print("Исходный список:")
    for s in students:
        print(f"  {s}")
    
    # Сортировка по возрасту (второй элемент)
    by_age = sorted(students, key=lambda x: x[1])
    print("\nПо возрасту:")
    for s in by_age:
        print(f"  {s}")
    
    # Сортировка по оценке (третий элемент, по убыванию)
    by_score = sorted(students, key=lambda x: x[2], reverse=True)
    print("\nПо оценке (убывание):")
    for s in by_score:
        print(f"  {s}")
    
    # Сортировка по возрасту, затем по оценке
    by_age_score = sorted(students, key=lambda x: (x[1], -x[2]))
    print("\nПо возрасту, потом оценке:")
    for s in by_age_score:
        print(f"  {s}")


# ============================================================================
# ЗАДАЧА 6: Поиск дубликатов в списке кортежей
# ============================================================================

def find_duplicate_tuples(tuples_list):
    """
    🟢 Junior level
    Находит дублирующиеся кортежи
    
    >>> find_duplicate_tuples([(1, 2), (3, 4), (1, 2), (5, 6), (3, 4)])
    [(1, 2), (3, 4)]
    """
    seen = set()
    duplicates = set()
    
    for t in tuples_list:
        if t in seen:
            duplicates.add(t)
        else:
            seen.add(t)
    
    return list(duplicates)


# ============================================================================
# ЗАДАЧА 7: Zip и enumerate с кортежами
# ============================================================================

def zip_enumerate_examples():
    """
    🟢 Junior level
    Примеры zip и enumerate, которые возвращают кортежи
    """
    
    # zip - объединяет несколько последовательностей
    names = ["Alice", "Bob", "Charlie"]
    ages = [25, 30, 35]
    cities = ["NYC", "LA", "SF"]
    
    print("Zip пример:")
    for name, age, city in zip(names, ages, cities):
        print(f"  {name}, {age}, {city}")
    
    # Создание словаря из двух списков
    person_dict = dict(zip(names, ages))
    print(f"\nСловарь: {person_dict}")
    
    # enumerate - добавляет индексы
    print("\nEnumerate пример:")
    for index, name in enumerate(names, start=1):
        print(f"  {index}. {name}")
    
    # Распаковка enumerate
    print("\nРаспаковка enumerate:")
    for i, (name, age) in enumerate(zip(names, ages), start=1):
        print(f"  {i}. {name} - {age} years")


# ============================================================================
# ЗАДАЧА 8: Кортежи и производительность
# ============================================================================

def compare_performance():
    """
    🟡 Middle level
    Сравнение производительности tuple vs list
    """
    import sys
    import timeit
    
    # Размер в памяти
    t = tuple(range(1000))
    l = list(range(1000))
    
    print(f"Размер tuple: {sys.getsizeof(t)} байт")
    print(f"Размер list: {sys.getsizeof(l)} байт")
    print(f"Разница: {sys.getsizeof(l) - sys.getsizeof(t)} байт")
    
    # Скорость создания
    tuple_time = timeit.timeit('tuple(range(1000))', number=100000)
    list_time = timeit.timeit('list(range(1000))', number=100000)
    
    print(f"\nВремя создания tuple: {tuple_time:.4f}s")
    print(f"Время создания list: {list_time:.4f}s")
    print(f"Tuple быстрее в {list_time/tuple_time:.2f} раз")


# ============================================================================
# ЗАДАЧА 9: Возврат нескольких значений из функции
# ============================================================================

def get_statistics(numbers):
    """
    🟢 Junior level
    Возвращает несколько статистик (tuple используется неявно)
    
    >>> get_statistics([1, 2, 3, 4, 5])
    (5, 15, 3.0, 1, 5)
    """
    count = len(numbers)
    total = sum(numbers)
    average = total / count if count > 0 else 0
    minimum = min(numbers) if numbers else None
    maximum = max(numbers) if numbers else None
    
    return count, total, average, minimum, maximum


def use_statistics():
    """
    Использование функции с tuple unpacking
    """
    data = [10, 20, 30, 40, 50]
    count, total, avg, min_val, max_val = get_statistics(data)
    
    print(f"Данные: {data}")
    print(f"Количество: {count}")
    print(f"Сумма: {total}")
    print(f"Среднее: {avg}")
    print(f"Мин: {min_val}, Макс: {max_val}")


# ============================================================================
# ЗАДАЧА 10: Tuple vs List - когда что использовать
# ============================================================================

def when_to_use():
    """
    🟡 Middle level
    Рекомендации по использованию tuple vs list
    """
    
    print("TUPLE - используйте когда:")
    print("  - Данные не должны изменяться (координаты, константы)")
    print("  - Нужен ключ для словаря")
    print("  - Возвращаете несколько значений из функции")
    print("  - Важна производительность и память")
    print("  - Данные имеют фиксированную структуру")
    
    print("\nLIST - используйте когда:")
    print("  - Данные будут изменяться")
    print("  - Количество элементов переменное")
    print("  - Нужны методы изменения (append, remove, sort, etc.)")
    print("  - Все элементы одного типа (однородная коллекция)")
    
    # Примеры
    print("\n--- Примеры ---")
    
    # Tuple - структура (RGB цвет)
    color = (255, 128, 0)  # RGB
    print(f"Цвет (tuple): {color}")
    
    # List - коллекция
    shopping_list = ["milk", "eggs", "bread"]
    shopping_list.append("cheese")
    print(f"Список покупок (list): {shopping_list}")


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("КОРТЕЖИ - Примеры и тесты")
    print("=" * 60)
    
    # Тест 1: Основы
    print("\n1. Основы работы с tuple:")
    tuple_basics()
    
    # Тест 2: Распаковка
    print("\n" + "=" * 60)
    print("2. Tuple unpacking:")
    unpacking_examples()
    
    # Тест 3: Named tuples
    print("\n" + "=" * 60)
    print("3. Named Tuples:")
    namedtuple_examples()
    typed_namedtuple_example()
    
    # Тест 4: Tuple как ключ
    print("\n" + "=" * 60)
    print("4. Tuple как ключ словаря:")
    tuple_as_dict_key()
    
    # Тест 5: Сортировка
    print("\n" + "=" * 60)
    print("5. Сортировка кортежей:")
    sort_tuples()
    
    # Тест 6: Zip и enumerate
    print("\n" + "=" * 60)
    print("6. Zip и enumerate:")
    zip_enumerate_examples()
    
    # Тест 7: Возврат значений
    print("\n" + "=" * 60)
    print("7. Возврат нескольких значений:")
    use_statistics()
    
    # Тест 8: Производительность
    print("\n" + "=" * 60)
    print("8. Сравнение производительности:")
    compare_performance()
    
    # Тест 9: Когда использовать
    print("\n" + "=" * 60)
    print("9. Tuple vs List - рекомендации:")
    when_to_use()
    
    print("\n" + "=" * 60)

