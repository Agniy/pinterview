"""
🟢 BINARY SEARCH (Бинарный поиск)

Временная сложность:
- Лучший случай: O(1) - элемент найден в середине
- Средний случай: O(log n)
- Худший случай: O(log n)

Пространственная сложность: 
- Итеративная версия: O(1)
- Рекурсивная версия: O(log n) - глубина стека вызовов

Особенности:
- Работает только на отсортированных данных
- Очень эффективен для больших массивов
- Основа многих других алгоритмов
- Классический пример алгоритма "разделяй и властвуй"
"""


def binary_search(arr, target):
    """
    🟢 Junior level
    Бинарный поиск (итеративная версия)
    
    Принцип работы:
    1. Находим середину массива
    2. Сравниваем с искомым элементом
    3. Если равен - возвращаем индекс
    4. Если меньше - ищем в левой половине
    5. Если больше - ищем в правой половине
    6. Повторяем до нахождения или исчерпания поиска
    
    Args:
        arr: отсортированный массив для поиска
        target: искомый элемент
        
    Returns:
        индекс элемента или -1 если не найден
        
    >>> binary_search([1, 3, 5, 7, 9, 11], 7)
    3
    >>> binary_search([1, 3, 5, 7, 9, 11], 6)
    -1
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


def binary_search_recursive(arr, target, left=0, right=None):
    """
    🟡 Middle level
    Бинарный поиск (рекурсивная версия)
    """
    if right is None:
        right = len(arr) - 1
    
    # Базовый случай
    if left > right:
        return -1
    
    mid = (left + right) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)


# ============================================================================
# ПОШАГОВОЕ ИСПОЛНЕНИЕ
# ============================================================================

def binary_search_with_steps(arr, target):
    """
    Версия с выводом пошагового исполнения
    """
    print(f"Ищем элемент {target} в отсортированном массиве {arr}")
    print("=" * 60)
    
    left, right = 0, len(arr) - 1
    step = 0
    
    while left <= right:
        step += 1
        mid = (left + right) // 2
        
        print(f"Шаг {step}:")
        print(f"  Границы поиска: left={left}, right={right}")
        print(f"  Средний элемент: arr[{mid}]={arr[mid]}")
        print(f"  Сравниваем {arr[mid]} с {target}")
        
        if arr[mid] == target:
            print(f"  ✓ Найден! Элемент {target} находится на позиции {mid}")
            return mid
        elif arr[mid] < target:
            print(f"  {arr[mid]} < {target}, ищем в правой половине")
            left = mid + 1
        else:
            print(f"  {arr[mid]} > {target}, ищем в левой половине")
            right = mid - 1
        
        print(f"  Новые границы: left={left}, right={right}")
        if left <= right:
            print(f"  Область поиска: {arr[left:right+1]}")
        print()
    
    print(f"✗ Элемент {target} не найден в массиве")
    return -1


# ============================================================================
# РАСШИРЕННЫЕ ВЕРСИИ
# ============================================================================

def find_first_occurrence(arr, target):
    """
    🟡 Middle level
    Находит первое вхождение элемента в отсортированном массиве с дубликатами
    
    >>> find_first_occurrence([1, 2, 2, 2, 3, 4], 2)
    1
    """
    left, right = 0, len(arr) - 1
    result = -1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            result = mid
            right = mid - 1  # Продолжаем искать в левой части
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result


def find_last_occurrence(arr, target):
    """
    Находит последнее вхождение элемента
    
    >>> find_last_occurrence([1, 2, 2, 2, 3, 4], 2)
    3
    """
    left, right = 0, len(arr) - 1
    result = -1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            result = mid
            left = mid + 1  # Продолжаем искать в правой части
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result


def find_closest_element(arr, target):
    """
    Находит элемент, ближайший к целевому
    
    >>> find_closest_element([1, 3, 7, 10, 15], 8)
    7
    """
    left, right = 0, len(arr) - 1
    
    while left < right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return arr[mid]
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    
    # Проверяем ближайший элемент
    if left > 0 and abs(arr[left - 1] - target) < abs(arr[left] - target):
        return arr[left - 1]
    return arr[left]


def count_occurrences(arr, target):
    """
    Подсчитывает количество вхождений элемента
    
    >>> count_occurrences([1, 2, 2, 2, 3, 4], 2)
    3
    """
    first = find_first_occurrence(arr, target)
    if first == -1:
        return 0
    
    last = find_last_occurrence(arr, target)
    return last - first + 1


# ============================================================================
# ПОИСК В РОТИРОВАННОМ МАССИВЕ
# ============================================================================

def search_rotated_array(arr, target):
    """
    🔴 Senior level
    Поиск в отсортированном ротированном массиве
    
    >>> search_rotated_array([4, 5, 6, 7, 0, 1, 2], 0)
    4
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        
        # Определяем, какая половина отсортирована
        if arr[left] <= arr[mid]:
            # Левая половина отсортирована
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            # Правая половина отсортирована
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1


# ============================================================================
# ПОИСК В 2D МАТРИЦЕ
# ============================================================================

def search_2d_matrix(matrix, target):
    """
    🟡 Middle level
    Поиск в отсортированной 2D матрице
    
    >>> matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    >>> search_2d_matrix(matrix, 3)
    True
    """
    if not matrix or not matrix[0]:
        return False
    
    rows, cols = len(matrix), len(matrix[0])
    left, right = 0, rows * cols - 1
    
    while left <= right:
        mid = (left + right) // 2
        mid_value = matrix[mid // cols][mid % cols]
        
        if mid_value == target:
            return True
        elif mid_value < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return False


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

def demonstrate_binary_search():
    """
    Демонстрация работы алгоритма
    """
    print("=" * 60)
    print("BINARY SEARCH - Демонстрация")
    print("=" * 60)
    
    # Тест 1: Элемент найден
    test_arr1 = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    target1 = 11
    print(f"\nТест 1: Ищем {target1} в {test_arr1}")
    result1 = binary_search(test_arr1, target1)
    print(f"Результат: индекс {result1}")
    
    # Тест 2: Элемент не найден
    test_arr2 = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    target2 = 8
    print(f"\nТест 2: Ищем {target2} в {test_arr2}")
    result2 = binary_search(test_arr2, target2)
    print(f"Результат: {result2} (не найден)")
    
    # Тест 3: Первый элемент
    test_arr3 = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    target3 = 1
    print(f"\nТест 3: Ищем {target3} в {test_arr3}")
    result3 = binary_search(test_arr3, target3)
    print(f"Результат: индекс {result3}")
    
    # Тест 4: Последний элемент
    test_arr4 = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    target4 = 19
    print(f"\nТест 4: Ищем {target4} в {test_arr4}")
    result4 = binary_search(test_arr4, target4)
    print(f"Результат: индекс {result4}")
    
    # Пошаговое исполнение
    print("\n" + "=" * 60)
    print("ПОШАГОВОЕ ИСПОЛНЕНИЕ")
    print("=" * 60)
    binary_search_with_steps([1, 3, 5, 7, 9, 11, 13], 7)
    
    # Поиск вхождений с дубликатами
    print("\n" + "=" * 60)
    print("ПОИСК В МАССИВЕ С ДУБЛИКАТАМИ")
    print("=" * 60)
    
    test_arr5 = [1, 2, 2, 2, 3, 4, 5, 6, 7, 8]
    target5 = 2
    print(f"Массив с дубликатами: {test_arr5}")
    print(f"Ищем все вхождения {target5}:")
    print(f"Первое вхождение: индекс {find_first_occurrence(test_arr5, target5)}")
    print(f"Последнее вхождение: индекс {find_last_occurrence(test_arr5, target5)}")
    print(f"Количество вхождений: {count_occurrences(test_arr5, target5)}")
    
    # Поиск ближайшего элемента
    test_arr6 = [1, 3, 7, 10, 15, 20, 25]
    target6 = 8
    print(f"\nБлижайший к {target6} в {test_arr6}: {find_closest_element(test_arr6, target6)}")


# ============================================================================
# АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ
# ============================================================================

def performance_analysis():
    """
    Анализ производительности
    """
    import time
    import random
    
    print("\n" + "=" * 60)
    print("АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ")
    print("=" * 60)
    
    sizes = [1000, 10000, 100000, 1000000]
    
    print("Размер\tЛинейный\tБинарный\tУскорение")
    print("-" * 50)
    
    for size in sizes:
        # Создаем отсортированный массив
        arr = sorted([random.randint(1, size * 2) for _ in range(size)])
        target = random.choice(arr)
        
        # Линейный поиск
        start = time.time()
        linear_search([i for i in range(size)], size - 1)
        linear_time = time.time() - start
        
        # Бинарный поиск
        start = time.time()
        binary_search([i for i in range(size)], size - 1)
        binary_time = time.time() - start
        
        speedup = linear_time / binary_time if binary_time > 0 else 0
        
        print(f"{size}\t{linear_time*1000:.3f}ms\t\t{binary_time*1000:.3f}ms\t\t{speedup:.1f}x")


# ============================================================================
# ПРАКТИЧЕСКИЕ ПРИМЕНЕНИЯ
# ============================================================================

def practical_applications():
    """
    Практические применения бинарного поиска
    """
    print("\n" + "=" * 60)
    print("ПРАКТИЧЕСКИЕ ПРИМЕНЕНИЯ")
    print("=" * 60)
    
    print("1. Поиск в базах данных:")
    print("   - Индексы в SQL")
    print("   - Поиск по первичному ключу")
    
    print("\n2. Поиск в файлах:")
    print("   - Поиск в больших отсортированных файлах")
    print("   - Поиск в логах по времени")
    
    print("\n3. Математические задачи:")
    print("   - Поиск корня уравнения")
    print("   - Поиск оптимального значения")
    
    print("\n4. Алгоритмы сортировки:")
    print("   - Основа для многих алгоритмов")
    print("   - Merge Sort, Quick Sort")
    
    print("\n5. Структуры данных:")
    print("   - Основа для B-деревьев")
    print("   - Skip lists")
    
    print("\n6. Оптимизация:")
    print("   - Поиск минимального/максимального значения")
    print("   - Бинарный поиск по ответу")


# ============================================================================
# ОБЩИЕ ОШИБКИ И ЛОВУШКИ
# ============================================================================

def common_mistakes():
    """
    Общие ошибки при реализации бинарного поиска
    """
    print("\n" + "=" * 60)
    print("ОБЩИЕ ОШИБКИ И ЛОВУШКИ")
    print("=" * 60)
    
    print("1. Неправильное условие цикла:")
    print("   ❌ while left < right:")
    print("   ✅ while left <= right:")
    
    print("\n2. Неправильное вычисление середины:")
    print("   ❌ mid = (left + right) / 2  # Может вызвать переполнение")
    print("   ✅ mid = left + (right - left) // 2")
    
    print("\n3. Неправильные границы:")
    print("   ❌ right = mid")
    print("   ✅ right = mid - 1")
    
    print("\n4. Поиск в неотсортированном массиве:")
    print("   ❌ Бинарный поиск работает только на отсортированных данных!")
    
    print("\n5. Ошибки в индексации:")
    print("   ❌ Забыть проверить границы массива")
    print("   ✅ Всегда проверять 0 <= index < len(arr)")


# ============================================================================
# ВАРИАНТЫ РЕАЛИЗАЦИИ
# ============================================================================

def implementation_variants():
    """
    Различные варианты реализации
    """
    print("\n" + "=" * 60)
    print("ВАРИАНТЫ РЕАЛИЗАЦИИ")
    print("=" * 60)
    
    print("1. Итеративная vs Рекурсивная:")
    print("   - Итеративная: O(1) памяти, быстрее")
    print("   - Рекурсивная: O(log n) памяти, проще для понимания")
    
    print("\n2. Поиск первого/последнего вхождения:")
    print("   - Модификация для работы с дубликатами")
    print("   - Важно для подсчета количества")
    
    print("\n3. Поиск в специальных структурах:")
    print("   - Ротированные массивы")
    print("   - 2D матрицы")
    print("   - Неполные массивы")


if __name__ == "__main__":
    demonstrate_binary_search()
    performance_analysis()
    practical_applications()
    common_mistakes()
    implementation_variants()
