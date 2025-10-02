"""
🔴 ИТЕРАТОРЫ И ИТЕРИРУЕМЫЕ ОБЪЕКТЫ - Вопросы и задачи для собеседований

Основные темы:
- Протокол итератора
- __iter__ и __next__
- StopIteration
- itertools
"""

import itertools


# ============================================================================
# ТЕОРЕТИЧЕСКИЕ ВОПРОСЫ
# ============================================================================

"""
Q1: В чем разница между итератором и итерируемым объектом?
A:
- Итерируемый (iterable): объект с методом __iter__(), возвращающим итератор
- Итератор (iterator): объект с методом __next__() и __iter__() (возвращает self)

Q2: Что такое протокол итератора?
A: Реализация методов __iter__() и __next__()

Q3: Что такое StopIteration?
A: Исключение, которое итератор выбрасывает при исчерпании элементов

Q4: Можно ли итератор использовать повторно?
A: Нет, итератор одноразовый. Нужно создать новый.
"""


# ============================================================================
# ЗАДАЧА 1: Простой итератор
# ============================================================================

class CountUp:
    """
    🟡 Middle level
    Итератор, считающий от start до end
    """
    
    def __init__(self, start, end):
        self.current = start
        self.end = end
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current > self.end:
            raise StopIteration
        
        value = self.current
        self.current += 1
        return value


def demo_count_up():
    print("Итератор CountUp:")
    for num in CountUp(1, 5):
        print(num, end=' ')
    print()


# ============================================================================
# ЗАДАЧА 2: Итератор Фибоначчи
# ============================================================================

class FibonacciIterator:
    """
    🟡 Middle level
    Бесконечный итератор чисел Фибоначчи
    """
    
    def __init__(self):
        self.a, self.b = 0, 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        value = self.a
        self.a, self.b = self.b, self.a + self.b
        return value


def demo_fibonacci():
    print("\nИтератор Фибоначчи (первые 10):")
    fib = FibonacciIterator()
    for _ in range(10):
        print(next(fib), end=' ')
    print()


# ============================================================================
# ЗАДАЧА 3: Итератор с ограничением
# ============================================================================

class LimitedFibonacci:
    """
    🟡 Middle level
    Итератор Фибоначчи с ограничением
    """
    
    def __init__(self, max_value):
        self.max_value = max_value
        self.a, self.b = 0, 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.a > self.max_value:
            raise StopIteration
        
        value = self.a
        self.a, self.b = self.b, self.a + self.b
        return value


def demo_limited_fib():
    print("\nФибоначчи до 100:")
    print(list(LimitedFibonacci(100)))


# ============================================================================
# ЗАДАЧА 4: Реверсивный итератор
# ============================================================================

class ReverseIterator:
    """
    🟡 Middle level
    Итератор для обратного обхода последовательности
    """
    
    def __init__(self, data):
        self.data = data
        self.index = len(data)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index == 0:
            raise StopIteration
        
        self.index -= 1
        return self.data[self.index]


def demo_reverse():
    print("\nОбратный итератор:")
    for char in ReverseIterator("hello"):
        print(char, end=' ')
    print()


# ============================================================================
# ЗАДАЧА 5: Итератор по батчам
# ============================================================================

class BatchIterator:
    """
    🟡 Middle level
    Разбивает последовательность на батчи
    """
    
    def __init__(self, data, batch_size):
        self.data = data
        self.batch_size = batch_size
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration
        
        batch = self.data[self.index:self.index + self.batch_size]
        self.index += self.batch_size
        return batch


def demo_batch():
    print("\nИтератор по батчам:")
    data = list(range(10))
    for batch in BatchIterator(data, 3):
        print(batch)


# ============================================================================
# ЗАДАЧА 6: Iterable класс (не iterator)
# ============================================================================

class NumberRange:
    """
    🟡 Middle level
    Итерируемый класс (можно использовать многократно)
    """
    
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def __iter__(self):
        # Возвращаем новый итератор каждый раз
        return NumberRangeIterator(self.start, self.end)


class NumberRangeIterator:
    """Итератор для NumberRange"""
    
    def __init__(self, start, end):
        self.current = start
        self.end = end
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current > self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value


def demo_iterable():
    print("\nIterable класс (многократное использование):")
    nr = NumberRange(1, 5)
    
    print("Первый проход:", list(nr))
    print("Второй проход:", list(nr))


# ============================================================================
# ЗАДАЧА 7: itertools примеры
# ============================================================================

def demo_itertools():
    """
    🟡 Middle level
    Примеры использования itertools
    """
    
    print("\nitertools примеры:")
    
    # count - бесконечный счетчик
    print("\ncount (первые 5):")
    for i, val in enumerate(itertools.count(10, 2)):
        if i >= 5:
            break
        print(val, end=' ')
    print()
    
    # cycle - циклическое повторение
    print("\ncycle (первые 10):")
    for i, val in enumerate(itertools.cycle(['A', 'B', 'C'])):
        if i >= 10:
            break
        print(val, end=' ')
    print()
    
    # repeat - повторение элемента
    print("\nrepeat (3 раза):")
    print(list(itertools.repeat('Python', 3)))
    
    # chain - объединение последовательностей
    print("\nchain:")
    print(list(itertools.chain([1, 2, 3], ['a', 'b', 'c'])))
    
    # islice - срез итератора
    print("\nislice (элементы 2-5):")
    print(list(itertools.islice(range(10), 2, 6)))
    
    # groupby - группировка
    print("\ngroupby:")
    data = [('a', 1), ('a', 2), ('b', 3), ('b', 4), ('c', 5)]
    for key, group in itertools.groupby(data, lambda x: x[0]):
        print(f"  {key}: {list(group)}")
    
    # combinations - комбинации
    print("\ncombinations:")
    print(list(itertools.combinations([1, 2, 3], 2)))
    
    # permutations - перестановки
    print("\npermutations:")
    print(list(itertools.permutations([1, 2, 3], 2)))
    
    # product - декартово произведение
    print("\nproduct:")
    print(list(itertools.product([1, 2], ['a', 'b'])))
    
    # accumulate - накопление
    print("\naccumulate (кумулятивная сумма):")
    print(list(itertools.accumulate([1, 2, 3, 4, 5])))
    
    # filterfalse - обратная фильтрация
    print("\nfilterfalse (нечетные):")
    print(list(itertools.filterfalse(lambda x: x % 2 == 0, range(10))))


# ============================================================================
# ЗАДАЧА 8: Кастомный enumerate
# ============================================================================

class MyEnumerate:
    """
    🟡 Middle level
    Собственная реализация enumerate
    """
    
    def __init__(self, iterable, start=0):
        self.iterator = iter(iterable)
        self.count = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        value = next(self.iterator)
        result = (self.count, value)
        self.count += 1
        return result


def demo_my_enumerate():
    print("\nКастомный enumerate:")
    for i, char in MyEnumerate("hello", start=1):
        print(f"{i}: {char}")


# ============================================================================
# ЗАДАЧА 9: Кастомный zip
# ============================================================================

class MyZip:
    """
    🔴 Senior level
    Собственная реализация zip
    """
    
    def __init__(self, *iterables):
        self.iterators = [iter(it) for it in iterables]
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if not self.iterators:
            raise StopIteration
        
        values = []
        for iterator in self.iterators:
            try:
                values.append(next(iterator))
            except StopIteration:
                raise StopIteration
        
        return tuple(values)


def demo_my_zip():
    print("\nКастомный zip:")
    for item in MyZip([1, 2, 3], ['a', 'b', 'c'], [10, 20, 30]):
        print(item)


# ============================================================================
# ЗАДАЧА 10: Бесконечный цикличный итератор
# ============================================================================

class CyclicIterator:
    """
    🟡 Middle level
    Циклический итератор
    """
    
    def __init__(self, data):
        self.data = data
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if not self.data:
            raise StopIteration
        
        value = self.data[self.index]
        self.index = (self.index + 1) % len(self.data)
        return value


def demo_cyclic():
    print("\nЦиклический итератор (первые 10):")
    cyclic = CyclicIterator(['A', 'B', 'C'])
    for _ in range(10):
        print(next(cyclic), end=' ')
    print()


# ============================================================================
# ЗАДАЧА 11: Ленивое вычисление с итераторами
# ============================================================================

class LazyFileReader:
    """
    🔴 Senior level
    Ленивое чтение файла построчно
    """
    
    def __init__(self, filename):
        self.filename = filename
        self.file = None
    
    def __iter__(self):
        self.file = open(self.filename, 'r', encoding='utf-8')
        return self
    
    def __next__(self):
        line = self.file.readline()
        if not line:
            self.file.close()
            raise StopIteration
        return line.strip()


# ============================================================================
# ЗАДАЧА 12: Фильтрующий итератор
# ============================================================================

class FilterIterator:
    """
    🟡 Middle level
    Итератор с фильтрацией
    """
    
    def __init__(self, iterable, predicate):
        self.iterator = iter(iterable)
        self.predicate = predicate
    
    def __iter__(self):
        return self
    
    def __next__(self):
        while True:
            value = next(self.iterator)
            if self.predicate(value):
                return value


def demo_filter():
    print("\nФильтрующий итератор (четные числа):")
    even = FilterIterator(range(10), lambda x: x % 2 == 0)
    print(list(even))


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("ИТЕРАТОРЫ - Примеры и тесты")
    print("=" * 60)
    
    # Тест 1: Простой итератор
    demo_count_up()
    
    # Тест 2: Фибоначчи
    demo_fibonacci()
    demo_limited_fib()
    
    # Тест 3: Реверсивный итератор
    demo_reverse()
    
    # Тест 4: Батчи
    demo_batch()
    
    # Тест 5: Iterable vs Iterator
    demo_iterable()
    
    # Тест 6: itertools
    demo_itertools()
    
    # Тест 7: Кастомный enumerate
    demo_my_enumerate()
    
    # Тест 8: Кастомный zip
    demo_my_zip()
    
    # Тест 9: Циклический итератор
    demo_cyclic()
    
    # Тест 10: Фильтрующий итератор
    demo_filter()
    
    print("\n" + "=" * 60)

