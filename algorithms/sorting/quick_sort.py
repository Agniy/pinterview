"""
🟡 QUICK SORT (Быстрая сортировка)

Временная сложность:
- Лучший случай: O(n log n) - когда pivot делит массив пополам
- Средний случай: O(n log n)
- Худший случай: O(n²) - когда pivot всегда минимальный или максимальный

Пространственная сложность: O(log n) - глубина рекурсии

Стабильность: Нет (может изменить порядок равных элементов)

Особенности:
- Алгоритм "разделяй и властвуй"
- In-place сортировка
- Один из самых быстрых алгоритмов на практике
- Выбор pivot критичен для производительности
"""


def quick_sort(arr):
    """
    🟡 Middle level
    Быстрая сортировка - разделяй и властвуй с pivot
    
    Принцип работы:
    1. Выбираем элемент pivot
    2. Разделяем массив на элементы меньше и больше pivot
    3. Рекурсивно сортируем части
    4. Объединяем результаты
    
    Args:
        arr: список для сортировки
        
    Returns:
        отсортированный список
        
    >>> quick_sort([10, 7, 8, 9, 1, 5])
    [1, 5, 7, 8, 9, 10]
    """
    arr = arr.copy()
    _quick_sort_helper(arr, 0, len(arr) - 1)
    return arr


def _quick_sort_helper(arr, low, high):
    """
    Рекурсивная функция быстрой сортировки
    """
    if low < high:
        # Находим позицию pivot после разделения
        pi = partition(arr, low, high)
        
        # Рекурсивно сортируем элементы до и после pivot
        _quick_sort_helper(arr, low, pi - 1)
        _quick_sort_helper(arr, pi + 1, high)


def partition(arr, low, high):
    """
    Разделение массива по pivot (схема Lomuto)
    """
    # Выбираем последний элемент как pivot
    pivot = arr[high]
    
    # Индекс меньшего элемента (правильная позиция pivot)
    i = low - 1
    
    for j in range(low, high):
        # Если текущий элемент меньше или равен pivot
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    # Ставим pivot в правильную позицию
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# ============================================================================
# ПОШАГОВОЕ ИСПОЛНЕНИЕ
# ============================================================================

def quick_sort_with_steps(arr, low=0, high=None, level=0):
    """
    Версия с выводом пошагового исполнения
    """
    if high is None:
        high = len(arr) - 1
    
    indent = "  " * level
    print(f"{indent}quick_sort(arr={arr}, low={low}, high={high})")
    
    if low < high:
        print(f"{indent}Разделяем массив {arr[low:high+1]}")
        
        # Разделяем
        pi = partition_with_steps(arr, low, high, level + 1)
        print(f"{indent}Pivot {arr[pi]} в позиции {pi}")
        print(f"{indent}Массив после разделения: {arr}")
        
        # Рекурсивно сортируем
        print(f"{indent}Сортируем левую часть {arr[low:pi]}")
        quick_sort_with_steps(arr, low, pi - 1, level + 1)
        
        print(f"{indent}Сортируем правую часть {arr[pi+1:high+1]}")
        quick_sort_with_steps(arr, pi + 1, high, level + 1)
    else:
        print(f"{indent}Базовый случай: {arr[low:high+1]}")


def partition_with_steps(arr, low, high, level=0):
    """
    Разделение с выводом шагов
    """
    indent = "  " * level
    pivot = arr[high]
    print(f"{indent}Pivot = {pivot}")
    
    i = low - 1
    print(f"{indent}i = {i} (индекс для элементов <= pivot)")
    
    for j in range(low, high):
        print(f"{indent}j={j}, arr[{j}]={arr[j]} vs pivot={pivot}")
        if arr[j] <= pivot:
            i += 1
            print(f"{indent}  arr[{j}] <= pivot, увеличиваем i до {i}")
            if i != j:
                print(f"{indent}  Меняем arr[{i}]={arr[i]} и arr[{j}]={arr[j]}")
                arr[i], arr[j] = arr[j], arr[i]
                print(f"{indent}  Массив: {arr}")
            else:
                print(f"{indent}  Элемент уже на месте")
        else:
            print(f"{indent}  arr[{j}] > pivot, пропускаем")
    
    # Ставим pivot в правильную позицию
    i += 1
    print(f"{indent}Ставим pivot в позицию {i}")
    if i != high:
        print(f"{indent}Меняем arr[{i}]={arr[i]} и arr[{high}]={arr[high]}")
        arr[i], arr[high] = arr[high], arr[i]
        print(f"{indent}Финальный массив: {arr}")
    
    return i


# ============================================================================
# РАЗНЫЕ СТРАТЕГИИ ВЫБОРА PIVOT
# ============================================================================

def quick_sort_first_pivot(arr):
    """
    Quick Sort с выбором первого элемента как pivot
    """
    arr = arr.copy()
    _quick_sort_first_helper(arr, 0, len(arr) - 1)
    return arr


def _quick_sort_first_helper(arr, low, high):
    if low < high:
        # Выбираем первый элемент как pivot
        pivot = arr[low]
        i = low + 1
        j = high
        
        while i <= j:
            while i <= j and arr[i] <= pivot:
                i += 1
            while i <= j and arr[j] >= pivot:
                j -= 1
            if i < j:
                arr[i], arr[j] = arr[j], arr[i]
        
        # Ставим pivot в правильную позицию
        arr[low], arr[j] = arr[j], arr[low]
        
        _quick_sort_first_helper(arr, low, j - 1)
        _quick_sort_first_helper(arr, j + 1, high)


def quick_sort_middle_pivot(arr):
    """
    Quick Sort с выбором среднего элемента как pivot
    """
    arr = arr.copy()
    _quick_sort_middle_helper(arr, 0, len(arr) - 1)
    return arr


def _quick_sort_middle_helper(arr, low, high):
    if low < high:
        # Выбираем средний элемент как pivot
        mid = (low + high) // 2
        arr[mid], arr[high] = arr[high], arr[mid]  # Перемещаем в конец
        
        pi = partition(arr, low, high)
        _quick_sort_middle_helper(arr, low, pi - 1)
        _quick_sort_middle_helper(arr, pi + 1, high)


def quick_sort_random_pivot(arr):
    """
    Quick Sort с выбором случайного элемента как pivot
    """
    import random
    arr = arr.copy()
    _quick_sort_random_helper(arr, 0, len(arr) - 1)
    return arr


def _quick_sort_random_helper(arr, low, high):
    if low < high:
        # Выбираем случайный элемент как pivot
        pivot_idx = random.randint(low, high)
        arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
        
        pi = partition(arr, low, high)
        _quick_sort_random_helper(arr, low, pi - 1)
        _quick_sort_random_helper(arr, pi + 1, high)


# ============================================================================
# КОМПАКТНАЯ ВЕРСИЯ
# ============================================================================

def quick_sort_compact(arr):
    """
    🟡 Middle level
    Компактная версия Quick Sort (не in-place)
    """
    if len(arr) <= 1:
        return arr
    
    # Выбираем pivot
    pivot = arr[len(arr) // 2]
    
    # Разделяем на три части
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    # Рекурсивно сортируем и объединяем
    return quick_sort_compact(left) + middle + quick_sort_compact(right)


# ============================================================================
# ОПТИМИЗИРОВАННАЯ ВЕРСИЯ
# ============================================================================

def quick_sort_optimized(arr):
    """
    Оптимизированная версия с переходом на Insertion Sort для малых массивов
    """
    arr = arr.copy()
    _quick_sort_optimized_helper(arr, 0, len(arr) - 1)
    return arr


def _quick_sort_optimized_helper(arr, low, high):
    # Для малых массивов используем Insertion Sort
    if high - low < 10:
        insertion_sort_section(arr, low, high)
        return
    
    if low < high:
        # Выбираем медиану из трех как pivot
        mid = (low + high) // 2
        if arr[low] > arr[mid]:
            arr[low], arr[mid] = arr[mid], arr[low]
        if arr[mid] > arr[high]:
            arr[mid], arr[high] = arr[high], arr[mid]
        if arr[low] > arr[mid]:
            arr[low], arr[mid] = arr[mid], arr[low]
        
        # Перемещаем медиану в конец
        arr[mid], arr[high] = arr[high], arr[mid]
        
        pi = partition(arr, low, high)
        _quick_sort_optimized_helper(arr, low, pi - 1)
        _quick_sort_optimized_helper(arr, pi + 1, high)


def insertion_sort_section(arr, low, high):
    """
    Insertion Sort для части массива
    """
    for i in range(low + 1, high + 1):
        key = arr[i]
        j = i - 1
        while j >= low and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

def demonstrate_quick_sort():
    """
    Демонстрация работы алгоритма
    """
    print("=" * 60)
    print("QUICK SORT - Демонстрация")
    print("=" * 60)
    
    # Тест 1: Простой массив
    test_arr1 = [10, 7, 8, 9, 1, 5]
    print(f"\nТест 1: {test_arr1}")
    result1 = quick_sort(test_arr1)
    print(f"Результат: {result1}")
    
    # Тест 2: Уже отсортированный массив
    test_arr2 = [1, 2, 3, 4, 5]
    print(f"\nТест 2 (уже отсортирован): {test_arr2}")
    result2 = quick_sort(test_arr2)
    print(f"Результат: {result2}")
    
    # Тест 3: Обратно отсортированный массив
    test_arr3 = [5, 4, 3, 2, 1]
    print(f"\nТест 3 (обратный порядок): {test_arr3}")
    result3 = quick_sort(test_arr3)
    print(f"Результат: {result3}")
    
    # Тест 4: Массив с дубликатами
    test_arr4 = [3, 1, 4, 1, 5, 9, 2, 6, 5]
    print(f"\nТест 4 (с дубликатами): {test_arr4}")
    result4 = quick_sort(test_arr4)
    print(f"Результат: {result4}")
    
    # Пошаговое исполнение
    print("\n" + "=" * 60)
    print("ПОШАГОВОЕ ИСПОЛНЕНИЕ на примере [5, 2, 8, 1, 9]")
    print("=" * 60)
    test_arr = [5, 2, 8, 1, 9]
    quick_sort_with_steps(test_arr.copy())
    
    # Сравнение стратегий выбора pivot
    print("\n" + "=" * 60)
    print("СРАВНЕНИЕ СТРАТЕГИЙ ВЫБОРА PIVOT")
    print("=" * 60)
    
    test_arr = [64, 34, 25, 12, 22, 11, 90]
    print(f"Исходный массив: {test_arr}")
    print(f"Последний элемент: {quick_sort(test_arr)}")
    print(f"Первый элемент: {quick_sort_first_pivot(test_arr)}")
    print(f"Средний элемент: {quick_sort_middle_pivot(test_arr)}")
    print(f"Случайный элемент: {quick_sort_random_pivot(test_arr)}")
    print(f"Компактная версия: {quick_sort_compact(test_arr)}")
    print(f"Оптимизированная: {quick_sort_optimized(test_arr)}")


# ============================================================================
# АНАЛИЗ СЛОЖНОСТИ
# ============================================================================

def analyze_complexity():
    """
    Детальный анализ сложности
    """
    print("\n" + "=" * 60)
    print("АНАЛИЗ СЛОЖНОСТИ QUICK SORT")
    print("=" * 60)
    
    print("Временная сложность:")
    print("- Лучший случай: O(n log n) - pivot делит массив пополам")
    print("- Средний случай: O(n log n)")
    print("- Худший случай: O(n²) - pivot всегда минимальный/максимальный")
    print()
    print("Пространственная сложность:")
    print("- O(log n) - глубина рекурсии")
    print("- Худший случай: O(n) - при неудачном выборе pivot")
    print()
    print("Факторы, влияющие на производительность:")
    print("- Стратегия выбора pivot")
    print("- Распределение данных")
    print("- Размер массива")
    print()
    print("Преимущества:")
    print("- В среднем быстрее Merge Sort")
    print("- In-place алгоритм")
    print("- Кэш-эффективный")
    print()
    print("Недостатки:")
    print("- Нестабильный")
    print("- Худший случай O(n²)")
    print("- Чувствителен к выбору pivot")


# ============================================================================
# ПРОБЛЕМА ХУДШЕГО СЛУЧАЯ
# ============================================================================

def demonstrate_worst_case():
    """
    Демонстрация худшего случая
    """
    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ ХУДШЕГО СЛУЧАЯ")
    print("=" * 60)
    
    # Уже отсортированный массив с выбором первого элемента
    worst_arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"Уже отсортированный массив: {worst_arr}")
    print("При выборе первого элемента как pivot:")
    print("Каждый pivot будет минимальным, разделение будет неравномерным")
    print("Количество сравнений: n + (n-1) + (n-2) + ... + 1 = n(n+1)/2 = O(n²)")
    
    # Демонстрация с подсчетом операций
    import time
    
    sizes = [100, 500, 1000]
    for size in sizes:
        # Худший случай
        worst_case = list(range(size))
        start = time.time()
        quick_sort_first_pivot(worst_case.copy())
        worst_time = time.time() - start
        
        # Лучший случай (случайный массив)
        import random
        random_case = list(range(size))
        random.shuffle(random_case)
        start = time.time()
        quick_sort(random_case.copy())
        random_time = time.time() - start
        
        print(f"\nРазмер {size}:")
        print(f"  Худший случай: {worst_time*1000:.2f}ms")
        print(f"  Случайный:     {random_time*1000:.2f}ms")
        print(f"  Отношение:     {worst_time/random_time:.1f}x")


# ============================================================================
# ПРАКТИЧЕСКИЕ РЕКОМЕНДАЦИИ
# ============================================================================

def practical_recommendations():
    """
    Практические рекомендации по использованию
    """
    print("\n" + "=" * 60)
    print("ПРАКТИЧЕСКИЕ РЕКОМЕНДАЦИИ")
    print("=" * 60)
    
    print("1. Выбор стратегии pivot:")
    print("   - Случайный pivot: хорош для общего случая")
    print("   - Медиана из трех: компромисс между простотой и эффективностью")
    print("   - Избегайте выбора первого/последнего элемента")
    
    print("\n2. Оптимизации:")
    print("   - Для малых массивов (< 10 элементов) используйте Insertion Sort")
    print("   - Introsort: переход на Heap Sort при глубокой рекурсии")
    print("   - Трехчастное разделение для массивов с дубликатами")
    
    print("\n3. Когда использовать:")
    print("   - Большие массивы с хорошим распределением данных")
    print("   - Когда важна скорость в среднем случае")
    print("   - In-place сортировка критична")
    
    print("\n4. Когда НЕ использовать:")
    print("   - Требуется стабильная сортировка")
    print("   - Гарантированная O(n log n) сложность важнее скорости")
    print("   - Маленькие массивы")


if __name__ == "__main__":
    demonstrate_quick_sort()
    analyze_complexity()
    demonstrate_worst_case()
    practical_recommendations()
