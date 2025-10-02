"""
🟢 СПИСКИ (Lists) - Вопросы и задачи для собеседований

Основные темы:
- Методы списков
- List comprehensions
- Срезы (slicing)
- Копирование списков
- Производительность операций
"""


# ============================================================================
# ТЕОРЕТИЧЕСКИЕ ВОПРОСЫ
# ============================================================================

"""
Q1: В чем разница между list.append() и list.extend()?
A: 
- append() добавляет элемент целиком (в том числе список как один элемент)
- extend() добавляет каждый элемент из итерируемого объекта

Q2: Что такое list comprehension и когда его использовать?
A: Компактный способ создания списков. Используется для трансформации данных.
Синтаксис: [expression for item in iterable if condition]

Q3: В чем разница между list.copy() и list[:] и deepcopy?
A:
- list.copy() и list[:] создают поверхностную копию (shallow copy)
- deepcopy создает глубокую копию (копирует вложенные объекты)

Q4: Какая сложность операций со списками?
A:
- Доступ по индексу: O(1)
- Поиск элемента: O(n)
- Добавление в конец: O(1) амортизированно
- Вставка в начало/середину: O(n)
- Удаление: O(n)

Q5: Что такое отрицательные индексы?
A: Индексация с конца списка. -1 - последний элемент, -2 - предпоследний и т.д.
"""


# ============================================================================
# ЗАДАЧА 1: Удалить дубликаты из списка, сохранив порядок
# ============================================================================

def remove_duplicates_preserve_order(lst):
    """
    🟢 Junior level
    Удаляет дубликаты, сохраняя порядок первого появления
    
    >>> remove_duplicates_preserve_order([1, 2, 2, 3, 1, 4])
    [1, 2, 3, 4]
    """
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def remove_duplicates_dict_fromkeys(lst):
    """
    Альтернативное решение через dict.fromkeys (Python 3.7+)
    """
    return list(dict.fromkeys(lst))


# ============================================================================
# ЗАДАЧА 2: Развернуть вложенный список (flatten)
# ============================================================================

def flatten_list(nested_list):
    """
    🟡 Middle level
    Разворачивает вложенный список любой глубины
    
    >>> flatten_list([1, [2, 3], [4, [5, 6]], 7])
    [1, 2, 3, 4, 5, 6, 7]
    """
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result


def flatten_list_iterative(nested_list):
    """
    Итеративное решение через стек
    """
    stack = list(reversed(nested_list))
    result = []
    
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            stack.extend(reversed(item))
        else:
            result.append(item)
    
    return result


# ============================================================================
# ЗАДАЧА 3: Найти пересечение двух списков
# ============================================================================

def list_intersection(list1, list2):
    """
    🟢 Junior level
    Находит общие элементы в двух списках
    
    >>> list_intersection([1, 2, 3, 4], [3, 4, 5, 6])
    [3, 4]
    """
    return list(set(list1) & set(list2))


def list_intersection_preserve_order(list1, list2):
    """
    С сохранением порядка из первого списка
    """
    set2 = set(list2)
    return [x for x in list1 if x in set2]


# ============================================================================
# ЗАДАЧА 4: Разбить список на чанки (chunks)
# ============================================================================

def split_into_chunks(lst, chunk_size):
    """
    🟡 Middle level
    Разбивает список на части заданного размера
    
    >>> split_into_chunks([1, 2, 3, 4, 5, 6, 7], 3)
    [[1, 2, 3], [4, 5, 6], [7]]
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def split_into_n_parts(lst, n):
    """
    Разбивает список на n примерно равных частей
    """
    k, m = divmod(len(lst), n)
    return [lst[i*k + min(i, m):(i+1)*k + min(i+1, m)] for i in range(n)]


# ============================================================================
# ЗАДАЧА 5: Ротация списка
# ============================================================================

def rotate_list(lst, k):
    """
    🟢 Junior level
    Сдвигает элементы списка на k позиций вправо
    
    >>> rotate_list([1, 2, 3, 4, 5], 2)
    [4, 5, 1, 2, 3]
    """
    if not lst:
        return lst
    k = k % len(lst)  # Обрабатываем случай k > len(lst)
    return lst[-k:] + lst[:-k]


# ============================================================================
# ЗАДАЧА 6: Найти второй максимум
# ============================================================================

def find_second_max(lst):
    """
    🟢 Junior level
    Находит второй по величине элемент
    
    >>> find_second_max([1, 5, 3, 9, 2, 9, 7])
    7
    """
    if len(lst) < 2:
        return None
    
    # Убираем дубликаты и сортируем
    unique_sorted = sorted(set(lst), reverse=True)
    return unique_sorted[1] if len(unique_sorted) > 1 else None


def find_second_max_optimized(lst):
    """
    Оптимизированное решение за O(n)
    """
    if len(lst) < 2:
        return None
    
    first = second = float('-inf')
    
    for num in lst:
        if num > first:
            second = first
            first = num
        elif num > second and num != first:
            second = num
    
    return second if second != float('-inf') else None


# ============================================================================
# ЗАДАЧА 7: Переместить все нули в конец
# ============================================================================

def move_zeros_to_end(lst):
    """
    🟡 Middle level
    Перемещает все нули в конец, сохраняя порядок остальных элементов
    
    >>> move_zeros_to_end([0, 1, 0, 3, 12])
    [1, 3, 12, 0, 0]
    """
    # Решение 1: создание нового списка
    non_zeros = [x for x in lst if x != 0]
    zeros = [x for x in lst if x == 0]
    return non_zeros + zeros


def move_zeros_to_end_inplace(lst):
    """
    In-place решение (модифицирует исходный список)
    """
    insert_pos = 0
    
    # Перемещаем все ненулевые элементы вперед
    for i in range(len(lst)):
        if lst[i] != 0:
            lst[insert_pos] = lst[i]
            insert_pos += 1
    
    # Заполняем остаток нулями
    for i in range(insert_pos, len(lst)):
        lst[i] = 0
    
    return lst


# ============================================================================
# ЗАДАЧА 8: Найти подмассив с максимальной суммой (Kadane's algorithm)
# ============================================================================

def max_subarray_sum(lst):
    """
    🔴 Senior level
    Находит максимальную сумму непрерывного подмассива
    
    >>> max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    6  # [4, -1, 2, 1]
    """
    if not lst:
        return 0
    
    max_sum = current_sum = lst[0]
    
    for num in lst[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    
    return max_sum


def max_subarray_with_indices(lst):
    """
    Возвращает также индексы подмассива
    """
    if not lst:
        return 0, 0, 0
    
    max_sum = current_sum = lst[0]
    start = end = temp_start = 0
    
    for i in range(1, len(lst)):
        if lst[i] > current_sum + lst[i]:
            current_sum = lst[i]
            temp_start = i
        else:
            current_sum += lst[i]
        
        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start
            end = i
    
    return max_sum, start, end


# ============================================================================
# ЗАДАЧА 9: List Comprehension - практические примеры
# ============================================================================

def list_comprehension_examples():
    """
    🟢 Junior level
    Примеры использования list comprehensions
    """
    
    # Квадраты чисел
    squares = [x**2 for x in range(10)]
    print(f"Squares: {squares}")
    
    # Четные числа
    evens = [x for x in range(20) if x % 2 == 0]
    print(f"Evens: {evens}")
    
    # Вложенные списки - декартово произведение
    pairs = [(x, y) for x in range(3) for y in range(3)]
    print(f"Pairs: {pairs}")
    
    # Условное преобразование
    transformed = [x if x % 2 == 0 else -x for x in range(10)]
    print(f"Transformed: {transformed}")
    
    # Развернуть матрицу
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flattened = [num for row in matrix for num in row]
    print(f"Flattened matrix: {flattened}")


# ============================================================================
# ЗАДАЧА 10: Слияние отсортированных списков
# ============================================================================

def merge_sorted_lists(list1, list2):
    """
    🟡 Middle level
    Объединяет два отсортированных списка в один отсортированный
    
    >>> merge_sorted_lists([1, 3, 5], [2, 4, 6])
    [1, 2, 3, 4, 5, 6]
    """
    result = []
    i = j = 0
    
    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            result.append(list1[i])
            i += 1
        else:
            result.append(list2[j])
            j += 1
    
    # Добавляем оставшиеся элементы
    result.extend(list1[i:])
    result.extend(list2[j:])
    
    return result


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("СПИСКИ - Примеры и тесты")
    print("=" * 60)
    
    # Тест 1: Удаление дубликатов
    print("\n1. Удаление дубликатов:")
    test_list = [1, 2, 2, 3, 1, 4, 4, 5]
    print(f"   Исходный: {test_list}")
    print(f"   Результат: {remove_duplicates_preserve_order(test_list)}")
    
    # Тест 2: Разворачивание вложенного списка
    print("\n2. Разворачивание списка:")
    nested = [1, [2, 3], [4, [5, 6]], 7]
    print(f"   Исходный: {nested}")
    print(f"   Результат: {flatten_list(nested)}")
    
    # Тест 3: Ротация списка
    print("\n3. Ротация списка:")
    test_list = [1, 2, 3, 4, 5]
    print(f"   Исходный: {test_list}")
    print(f"   Ротация на 2: {rotate_list(test_list, 2)}")
    
    # Тест 4: Второй максимум
    print("\n4. Второй максимум:")
    test_list = [1, 5, 3, 9, 2, 9, 7]
    print(f"   Список: {test_list}")
    print(f"   Второй максимум: {find_second_max_optimized(test_list)}")
    
    # Тест 5: Максимальная сумма подмассива
    print("\n5. Максимальная сумма подмассива:")
    test_list = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(f"   Список: {test_list}")
    max_sum, start, end = max_subarray_with_indices(test_list)
    print(f"   Макс сумма: {max_sum}, подмассив: {test_list[start:end+1]}")
    
    # Тест 6: List comprehensions
    print("\n6. List Comprehension примеры:")
    list_comprehension_examples()
    
    print("\n" + "=" * 60)

