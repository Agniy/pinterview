"""
🟢 СЛОВАРИ (Dictionaries) - Вопросы и задачи для собеседований

Основные темы:
- Методы словарей
- Dict comprehensions
- defaultdict, Counter, OrderedDict
- Хеширование и производительность
"""

from collections import defaultdict, Counter, OrderedDict


# ============================================================================
# ТЕОРЕТИЧЕСКИЕ ВОПРОСЫ
# ============================================================================

"""
Q1: Как работает словарь в Python? Какая сложность операций?
A: Словарь реализован как хеш-таблица
- Доступ/вставка/удаление: O(1) в среднем, O(n) в худшем случае
- Поиск ключа: O(1)

Q2: Какие типы данных могут быть ключами словаря?
A: Только неизменяемые (hashable) типы:
- int, float, str, tuple (если содержит hashable элементы), frozenset
- Нельзя: list, dict, set

Q3: В чем разница между dict.get() и dict[key]?
A:
- dict[key] вызывает KeyError, если ключа нет
- dict.get(key, default) возвращает default (None по умолчанию)

Q4: Что такое dict comprehension?
A: {key_expr: value_expr for item in iterable if condition}

Q5: Гарантирован ли порядок в dict?
A: С Python 3.7+ порядок вставки гарантирован

Q6: В чем разница между dict.items(), dict.keys(), dict.values()?
A: Возвращают view объекты (динамические представления):
- items() - пары (ключ, значение)
- keys() - только ключи
- values() - только значения
"""


# ============================================================================
# ЗАДАЧА 1: Слияние словарей
# ============================================================================

def merge_dicts_method1(dict1, dict2):
    """
    🟢 Junior level
    Слияние словарей (dict2 перезаписывает dict1)
    
    >>> merge_dicts_method1({'a': 1, 'b': 2}, {'b': 3, 'c': 4})
    {'a': 1, 'b': 3, 'c': 4}
    """
    result = dict1.copy()
    result.update(dict2)
    return result


def merge_dicts_operator(dict1, dict2):
    """
    Python 3.9+ - оператор |
    """
    return dict1 | dict2


def merge_dicts_unpacking(dict1, dict2):
    """
    Python 3.5+ - распаковка
    """
    return {**dict1, **dict2}


# ============================================================================
# ЗАДАЧА 2: Инвертировать словарь (поменять ключи и значения)
# ============================================================================

def invert_dict(d):
    """
    🟢 Junior level
    Инвертирует словарь (значения становятся ключами)
    
    >>> invert_dict({'a': 1, 'b': 2, 'c': 3})
    {1: 'a', 2: 'b', 3: 'c'}
    """
    return {v: k for k, v in d.items()}


def invert_dict_with_duplicates(d):
    """
    🟡 Middle level
    Если несколько ключей имеют одно значение, группирует их в список
    
    >>> invert_dict_with_duplicates({'a': 1, 'b': 2, 'c': 1})
    {1: ['a', 'c'], 2: ['b']}
    """
    result = defaultdict(list)
    for key, value in d.items():
        result[value].append(key)
    return dict(result)


# ============================================================================
# ЗАДАЧА 3: Группировка элементов
# ============================================================================

def group_by_length(words):
    """
    🟡 Middle level
    Группирует слова по длине
    
    >>> group_by_length(['apple', 'bat', 'car', 'elephant', 'dog'])
    {5: ['apple'], 3: ['bat', 'car', 'dog'], 8: ['elephant']}
    """
    result = defaultdict(list)
    for word in words:
        result[len(word)].append(word)
    return dict(result)


def group_by_key(items, key_func):
    """
    Универсальная группировка по функции
    
    >>> students = [{'name': 'Alice', 'grade': 'A'}, {'name': 'Bob', 'grade': 'B'}, 
    ...             {'name': 'Charlie', 'grade': 'A'}]
    >>> group_by_key(students, lambda x: x['grade'])
    """
    result = defaultdict(list)
    for item in items:
        key = key_func(item)
        result[key].append(item)
    return dict(result)


# ============================================================================
# ЗАДАЧА 4: Подсчет частоты элементов
# ============================================================================

def count_frequency_manual(items):
    """
    🟢 Junior level
    Подсчитывает частоту элементов (ручная реализация)
    
    >>> count_frequency_manual(['a', 'b', 'a', 'c', 'b', 'a'])
    {'a': 3, 'b': 2, 'c': 1}
    """
    freq = {}
    for item in items:
        freq[item] = freq.get(item, 0) + 1
    return freq


def count_frequency_counter(items):
    """
    Используя Counter из collections
    """
    return dict(Counter(items))


def most_common_elements(items, n=3):
    """
    Находит n самых частых элементов
    
    >>> most_common_elements(['a', 'b', 'a', 'c', 'b', 'a'], 2)
    [('a', 3), ('b', 2)]
    """
    return Counter(items).most_common(n)


# ============================================================================
# ЗАДАЧА 5: Вложенные словари - получение значения по пути
# ============================================================================

def get_nested_value(data, path, default=None):
    """
    🟡 Middle level
    Получает значение из вложенного словаря по пути
    
    >>> data = {'a': {'b': {'c': 42}}}
    >>> get_nested_value(data, ['a', 'b', 'c'])
    42
    >>> get_nested_value(data, ['a', 'x', 'y'], default='not found')
    'not found'
    """
    current = data
    for key in path:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current


def set_nested_value(data, path, value):
    """
    Устанавливает значение в вложенном словаре
    
    >>> data = {}
    >>> set_nested_value(data, ['a', 'b', 'c'], 42)
    >>> data
    {'a': {'b': {'c': 42}}}
    """
    current = data
    for key in path[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    current[path[-1]] = value


# ============================================================================
# ЗАДАЧА 6: Объединение словарей с суммированием значений
# ============================================================================

def merge_with_sum(dict1, dict2):
    """
    🟡 Middle level
    Объединяет словари, суммируя значения для общих ключей
    
    >>> merge_with_sum({'a': 1, 'b': 2}, {'b': 3, 'c': 4})
    {'a': 1, 'b': 5, 'c': 4}
    """
    result = dict1.copy()
    for key, value in dict2.items():
        result[key] = result.get(key, 0) + value
    return result


def merge_dicts_custom(dict1, dict2, merge_func):
    """
    Обобщенное слияние с пользовательской функцией
    """
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result:
            result[key] = merge_func(result[key], value)
        else:
            result[key] = value
    return result


# ============================================================================
# ЗАДАЧА 7: Фильтрация словаря
# ============================================================================

def filter_dict_by_value(d, predicate):
    """
    🟢 Junior level
    Фильтрует словарь по условию на значения
    
    >>> filter_dict_by_value({'a': 1, 'b': 2, 'c': 3, 'd': 4}, lambda x: x > 2)
    {'c': 3, 'd': 4}
    """
    return {k: v for k, v in d.items() if predicate(v)}


def filter_dict_by_key(d, predicate):
    """
    Фильтрует по ключам
    """
    return {k: v for k, v in d.items() if predicate(k)}


# ============================================================================
# ЗАДАЧА 8: Проверка изоморфности строк
# ============================================================================

def is_isomorphic(s1, s2):
    """
    🟡 Middle level
    Проверяет, являются ли строки изоморфными
    (можно ли заменить символы одной на другую 1-к-1)
    
    >>> is_isomorphic("egg", "add")
    True
    >>> is_isomorphic("foo", "bar")
    False
    """
    if len(s1) != len(s2):
        return False
    
    mapping1 = {}
    mapping2 = {}
    
    for c1, c2 in zip(s1, s2):
        if c1 in mapping1:
            if mapping1[c1] != c2:
                return False
        else:
            mapping1[c1] = c2
        
        if c2 in mapping2:
            if mapping2[c2] != c1:
                return False
        else:
            mapping2[c2] = c1
    
    return True


# ============================================================================
# ЗАДАЧА 9: LRU Cache (простая реализация)
# ============================================================================

class LRUCache:
    """
    🔴 Senior level
    Least Recently Used Cache - кеш с вытеснением давно не использованных элементов
    """
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key):
        """
        Получить значение, переместив его в конец (как недавно использованное)
        """
        if key not in self.cache:
            return -1
        
        # Перемещаем в конец
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        """
        Добавить/обновить значение
        """
        if key in self.cache:
            # Обновляем и перемещаем в конец
            self.cache.move_to_end(key)
        else:
            # Если кеш полон, удаляем самый старый элемент
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
        
        self.cache[key] = value


# ============================================================================
# ЗАДАЧА 10: Словарь по умолчанию с функцией
# ============================================================================

class DefaultDict:
    """
    🟡 Middle level
    Собственная реализация defaultdict
    """
    
    def __init__(self, default_factory):
        self.default_factory = default_factory
        self.data = {}
    
    def __getitem__(self, key):
        if key not in self.data:
            self.data[key] = self.default_factory()
        return self.data[key]
    
    def __setitem__(self, key, value):
        self.data[key] = value


# ============================================================================
# Dict Comprehension примеры
# ============================================================================

def dict_comprehension_examples():
    """
    🟢 Junior level
    Примеры dict comprehensions
    """
    
    # Квадраты чисел
    squares = {x: x**2 for x in range(1, 6)}
    print(f"Squares: {squares}")
    
    # Инвертирование
    original = {'a': 1, 'b': 2, 'c': 3}
    inverted = {v: k for k, v in original.items()}
    print(f"Inverted: {inverted}")
    
    # Фильтрация
    filtered = {k: v for k, v in squares.items() if v > 10}
    print(f"Filtered: {filtered}")
    
    # Из двух списков
    keys = ['name', 'age', 'city']
    values = ['Alice', 30, 'NYC']
    person = {k: v for k, v in zip(keys, values)}
    print(f"Person: {person}")


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("СЛОВАРИ - Примеры и тесты")
    print("=" * 60)
    
    # Тест 1: Инвертирование словаря
    print("\n1. Инвертирование словаря:")
    d = {'a': 1, 'b': 2, 'c': 1, 'd': 3}
    print(f"   Исходный: {d}")
    print(f"   Инвертированный (простой): {invert_dict({'a': 1, 'b': 2})}")
    print(f"   С дубликатами: {invert_dict_with_duplicates(d)}")
    
    # Тест 2: Группировка
    print("\n2. Группировка слов по длине:")
    words = ['apple', 'bat', 'car', 'elephant', 'dog', 'cat']
    print(f"   Слова: {words}")
    print(f"   Группы: {group_by_length(words)}")
    
    # Тест 3: Подсчет частоты
    print("\n3. Подсчет частоты:")
    items = ['a', 'b', 'a', 'c', 'b', 'a', 'd', 'b']
    print(f"   Элементы: {items}")
    print(f"   Частота: {count_frequency_counter(items)}")
    print(f"   Топ-2: {most_common_elements(items, 2)}")
    
    # Тест 4: Вложенные словари
    print("\n4. Работа с вложенными словарями:")
    data = {'user': {'profile': {'name': 'Alice', 'age': 30}}}
    print(f"   Данные: {data}")
    print(f"   Получить name: {get_nested_value(data, ['user', 'profile', 'name'])}")
    print(f"   Несуществующий путь: {get_nested_value(data, ['user', 'x'], 'N/A')}")
    
    # Тест 5: Слияние с суммированием
    print("\n5. Слияние словарей с суммой:")
    d1 = {'a': 1, 'b': 2, 'c': 3}
    d2 = {'b': 3, 'c': 4, 'd': 5}
    print(f"   Dict1: {d1}")
    print(f"   Dict2: {d2}")
    print(f"   Результат: {merge_with_sum(d1, d2)}")
    
    # Тест 6: LRU Cache
    print("\n6. LRU Cache:")
    cache = LRUCache(2)
    cache.put(1, 'one')
    cache.put(2, 'two')
    print(f"   get(1): {cache.get(1)}")
    cache.put(3, 'three')  # Вытеснит ключ 2
    print(f"   get(2) после добавления 3: {cache.get(2)}")  # -1
    print(f"   get(3): {cache.get(3)}")
    
    # Тест 7: Dict comprehensions
    print("\n7. Dict Comprehension примеры:")
    dict_comprehension_examples()
    
    print("\n" + "=" * 60)

