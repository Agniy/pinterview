"""
🟢 МНОЖЕСТВА (Sets) - Вопросы и задачи для собеседований

Основные темы:
- Операции над множествами
- Set comprehensions
- frozenset
- Производительность
"""


# ============================================================================
# ТЕОРЕТИЧЕСКИЕ ВОПРОСЫ
# ============================================================================

"""
Q1: Что такое set и когда его использовать?
A: Set - неупорядоченная коллекция уникальных элементов
Использование:
- Удаление дубликатов
- Проверка принадлежности (O(1))
- Математические операции (объединение, пересечение и т.д.)

Q2: Какая сложность основных операций?
A:
- Добавление/удаление: O(1)
- Проверка принадлежности: O(1)
- Объединение/пересечение: O(min(len(s1), len(s2)))

Q3: В чем разница между set и frozenset?
A:
- set - изменяемый (mutable)
- frozenset - неизменяемый (immutable), можно использовать как ключ dict

Q4: Какие операции над множествами есть в Python?
A:
- Объединение: | или union()
- Пересечение: & или intersection()
- Разность: - или difference()
- Симметрическая разность: ^ или symmetric_difference()
- Подмножество: <= или issubset()
- Надмножество: >= или issuperset()

Q5: Почему set не поддерживает индексацию?
A: Set - неупорядоченная коллекция, порядок элементов не гарантирован
"""


# ============================================================================
# ЗАДАЧА 1: Операции над множествами
# ============================================================================

def set_operations_demo():
    """
    🟢 Junior level
    Демонстрация основных операций над множествами
    """
    set1 = {1, 2, 3, 4, 5}
    set2 = {4, 5, 6, 7, 8}
    
    print("Set1:", set1)
    print("Set2:", set2)
    
    # Объединение
    union = set1 | set2  # или set1.union(set2)
    print(f"Объединение (|): {union}")
    
    # Пересечение
    intersection = set1 & set2  # или set1.intersection(set2)
    print(f"Пересечение (&): {intersection}")
    
    # Разность
    difference = set1 - set2  # или set1.difference(set2)
    print(f"Разность (-): {difference}")
    
    # Симметрическая разность
    sym_diff = set1 ^ set2  # или set1.symmetric_difference(set2)
    print(f"Симметрическая разность (^): {sym_diff}")
    
    # Проверки
    print(f"\n{1, 2} подмножество set1: {{1, 2}} <= set1 = {{1, 2} <= set1}")
    print(f"set1 и set2 не пересекаются: {set1.isdisjoint(set2)}")


# ============================================================================
# ЗАДАЧА 2: Найти все уникальные элементы в списке
# ============================================================================

def get_unique_elements(lst):
    """
    🟢 Junior level
    Возвращает уникальные элементы из списка
    
    >>> get_unique_elements([1, 2, 2, 3, 4, 3, 5])
    {1, 2, 3, 4, 5}
    """
    return set(lst)


def get_unique_preserve_order(lst):
    """
    С сохранением порядка первого появления (через dict)
    """
    return list(dict.fromkeys(lst))


# ============================================================================
# ЗАДАЧА 3: Проверка анаграмм
# ============================================================================

def are_anagrams(str1, str2):
    """
    🟢 Junior level
    Проверяет, являются ли строки анаграммами
    
    >>> are_anagrams("listen", "silent")
    True
    >>> are_anagrams("hello", "world")
    False
    """
    # Удаляем пробелы и приводим к нижнему регистру
    str1 = str1.replace(" ", "").lower()
    str2 = str2.replace(" ", "").lower()
    
    # Сравниваем отсортированные символы
    return sorted(str1) == sorted(str2)


def are_anagrams_using_counter(str1, str2):
    """
    Альтернативное решение через Counter
    """
    from collections import Counter
    str1 = str1.replace(" ", "").lower()
    str2 = str2.replace(" ", "").lower()
    return Counter(str1) == Counter(str2)


# ============================================================================
# ЗАДАЧА 4: Найти общие элементы в N списках
# ============================================================================

def find_common_elements(*lists):
    """
    🟡 Middle level
    Находит элементы, присутствующие во всех списках
    
    >>> find_common_elements([1, 2, 3], [2, 3, 4], [2, 3, 5])
    {2, 3}
    """
    if not lists:
        return set()
    
    # Начинаем с первого множества
    common = set(lists[0])
    
    # Пересекаем с остальными
    for lst in lists[1:]:
        common &= set(lst)
    
    return common


def find_common_elements_functional(*lists):
    """
    Функциональный подход
    """
    if not lists:
        return set()
    
    from functools import reduce
    return reduce(lambda a, b: a & b, map(set, lists))


# ============================================================================
# ЗАДАЧА 5: Найти все элементы, встречающиеся только один раз
# ============================================================================

def find_unique_once(lst):
    """
    🟡 Middle level
    Находит элементы, встречающиеся ровно один раз
    
    >>> find_unique_once([1, 2, 2, 3, 4, 4, 5])
    {1, 3, 5}
    """
    from collections import Counter
    counts = Counter(lst)
    return {item for item, count in counts.items() if count == 1}


# ============================================================================
# ЗАДАЧА 6: Группировка анаграмм
# ============================================================================

def group_anagrams(words):
    """
    🟡 Middle level
    Группирует слова-анаграммы вместе
    
    >>> group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
    """
    from collections import defaultdict
    
    groups = defaultdict(list)
    
    for word in words:
        # Используем отсортированное слово как ключ
        key = ''.join(sorted(word))
        groups[key].append(word)
    
    return list(groups.values())


# ============================================================================
# ЗАДАЧА 7: Проверка, содержит ли список дубликаты
# ============================================================================

def has_duplicates(lst):
    """
    🟢 Junior level
    Проверяет наличие дубликатов в списке
    
    >>> has_duplicates([1, 2, 3, 4])
    False
    >>> has_duplicates([1, 2, 2, 3])
    True
    """
    return len(lst) != len(set(lst))


def find_duplicates(lst):
    """
    Возвращает все дублирующиеся элементы
    """
    seen = set()
    duplicates = set()
    
    for item in lst:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    
    return duplicates


# ============================================================================
# ЗАДАЧА 8: Найти пропущенные числа в диапазоне
# ============================================================================

def find_missing_numbers(nums, start, end):
    """
    🟡 Middle level
    Находит пропущенные числа в диапазоне
    
    >>> find_missing_numbers([1, 2, 4, 6], 1, 6)
    {3, 5}
    """
    full_range = set(range(start, end + 1))
    present = set(nums)
    return full_range - present


# ============================================================================
# ЗАДАЧА 9: Подмножества (Power Set)
# ============================================================================

def generate_all_subsets(s):
    """
    🔴 Senior level
    Генерирует все возможные подмножества множества
    
    >>> sorted(generate_all_subsets({1, 2, 3}))
    [set(), {1}, {1, 2}, {1, 2, 3}, {1, 3}, {2}, {2, 3}, {3}]
    """
    s = list(s)
    n = len(s)
    result = []
    
    # Используем битовые маски для генерации подмножеств
    for i in range(2**n):
        subset = set()
        for j in range(n):
            # Проверяем, установлен ли j-й бит
            if i & (1 << j):
                subset.add(s[j])
        result.append(subset)
    
    return result


def generate_subsets_recursive(s):
    """
    Рекурсивное решение
    """
    s = list(s)
    
    def backtrack(index, current):
        if index == len(s):
            result.append(set(current))
            return
        
        # Не включаем текущий элемент
        backtrack(index + 1, current)
        
        # Включаем текущий элемент
        backtrack(index + 1, current + [s[index]])
    
    result = []
    backtrack(0, [])
    return result


# ============================================================================
# ЗАДАЧА 10: Longest Consecutive Sequence
# ============================================================================

def longest_consecutive(nums):
    """
    🔴 Senior level
    Находит длину самой длинной последовательности последовательных чисел
    
    >>> longest_consecutive([100, 4, 200, 1, 3, 2])
    4  # [1, 2, 3, 4]
    """
    if not nums:
        return 0
    
    num_set = set(nums)
    max_length = 0
    
    for num in num_set:
        # Проверяем, начало ли это последовательности
        if num - 1 not in num_set:
            current_num = num
            current_length = 1
            
            # Считаем длину последовательности
            while current_num + 1 in num_set:
                current_num += 1
                current_length += 1
            
            max_length = max(max_length, current_length)
    
    return max_length


# ============================================================================
# ЗАДАЧА 11: Set Comprehension примеры
# ============================================================================

def set_comprehension_examples():
    """
    🟢 Junior level
    Примеры set comprehensions
    """
    
    # Квадраты четных чисел
    even_squares = {x**2 for x in range(10) if x % 2 == 0}
    print(f"Квадраты четных: {even_squares}")
    
    # Уникальные длины слов
    words = ["hello", "world", "hi", "python", "code"]
    lengths = {len(word) for word in words}
    print(f"Уникальные длины: {lengths}")
    
    # Первые буквы (уникальные)
    first_letters = {word[0] for word in words}
    print(f"Первые буквы: {first_letters}")


# ============================================================================
# ЗАДАЧА 12: Frozenset примеры
# ============================================================================

def frozenset_examples():
    """
    🟡 Middle level
    Примеры использования frozenset
    """
    
    # Frozenset как ключ словаря
    set_dict = {
        frozenset([1, 2, 3]): "Group A",
        frozenset([4, 5, 6]): "Group B"
    }
    print(f"Словарь с frozenset ключами: {set_dict}")
    
    # Frozenset в множестве
    set_of_sets = {
        frozenset([1, 2]),
        frozenset([3, 4]),
        frozenset([1, 2])  # Дубликат не добавится
    }
    print(f"Множество frozenset'ов: {set_of_sets}")
    
    # Операции как с обычным set
    fs1 = frozenset([1, 2, 3])
    fs2 = frozenset([2, 3, 4])
    print(f"Пересечение: {fs1 & fs2}")


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("МНОЖЕСТВА - Примеры и тесты")
    print("=" * 60)
    
    # Тест 1: Базовые операции
    print("\n1. Базовые операции над множествами:")
    set_operations_demo()
    
    # Тест 2: Проверка анаграмм
    print("\n2. Проверка анаграмм:")
    print(f"   'listen' и 'silent': {are_anagrams('listen', 'silent')}")
    print(f"   'hello' и 'world': {are_anagrams('hello', 'world')}")
    
    # Тест 3: Общие элементы
    print("\n3. Общие элементы в списках:")
    lists = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]]
    print(f"   Списки: {lists}")
    print(f"   Общие: {find_common_elements(*lists)}")
    
    # Тест 4: Группировка анаграмм
    print("\n4. Группировка анаграмм:")
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    print(f"   Слова: {words}")
    print(f"   Группы: {group_anagrams(words)}")
    
    # Тест 5: Поиск дубликатов
    print("\n5. Поиск дубликатов:")
    test_list = [1, 2, 3, 2, 4, 5, 3, 6]
    print(f"   Список: {test_list}")
    print(f"   Есть дубликаты: {has_duplicates(test_list)}")
    print(f"   Дубликаты: {find_duplicates(test_list)}")
    
    # Тест 6: Пропущенные числа
    print("\n6. Пропущенные числа:")
    nums = [1, 2, 4, 6, 7, 10]
    print(f"   Числа: {nums}")
    print(f"   Пропущены (1-10): {sorted(find_missing_numbers(nums, 1, 10))}")
    
    # Тест 7: Самая длинная последовательность
    print("\n7. Longest Consecutive Sequence:")
    nums = [100, 4, 200, 1, 3, 2]
    print(f"   Числа: {nums}")
    print(f"   Длина последовательности: {longest_consecutive(nums)}")
    
    # Тест 8: Set comprehensions
    print("\n8. Set Comprehension примеры:")
    set_comprehension_examples()
    
    # Тест 9: Frozenset
    print("\n9. Frozenset примеры:")
    frozenset_examples()
    
    print("\n" + "=" * 60)

