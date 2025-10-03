"""
🟡 MERGE SORT (Сортировка слиянием)

Временная сложность:
- Лучший случай: O(n log n)
- Средний случай: O(n log n)
- Худший случай: O(n log n)

Пространственная сложность: O(n) - требует дополнительной памяти

Стабильность: Да (сохраняет порядок равных элементов)

Особенности:
- Алгоритм "разделяй и властвуй"
- Гарантированная O(n log n) сложность
- Подходит для сортировки больших объемов данных
- Используется во многих встроенных сортировках (Timsort)
"""


def merge_sort(arr):
    """
    🟡 Middle level
    Сортировка слиянием - разделяй и властвуй
    
    Принцип работы:
    1. Разделяем массив пополам до получения единичных элементов
    2. Рекурсивно сортируем каждую половину
    3. Сливаем отсортированные половины в один массив
    
    Args:
        arr: список для сортировки
        
    Returns:
        отсортированный список
        
    >>> merge_sort([38, 27, 43, 3, 9, 82, 10])
    [3, 9, 10, 27, 38, 43, 82]
    """
    # Базовый случай
    if len(arr) <= 1:
        return arr
    
    # Разделяем массив пополам
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    # Сливаем отсортированные части
    return merge(left, right)


def merge(left, right):
    """
    Слияние двух отсортированных массивов
    """
    result = []
    i = j = 0
    
    # Сравниваем элементы и добавляем меньший
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Добавляем оставшиеся элементы
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result


# ============================================================================
# ПОШАГОВОЕ ИСПОЛНЕНИЕ
# ============================================================================

def merge_sort_with_steps(arr, level=0):
    """
    Версия с выводом пошагового исполнения
    """
    indent = "  " * level
    print(f"{indent}Вызываем merge_sort({arr})")
    
    # Базовый случай
    if len(arr) <= 1:
        print(f"{indent}Базовый случай: возвращаем {arr}")
        return arr
    
    # Разделяем
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    
    print(f"{indent}Разделяем: left={left}, right={right}")
    
    # Рекурсивно сортируем
    sorted_left = merge_sort_with_steps(left, level + 1)
    sorted_right = merge_sort_with_steps(right, level + 1)
    
    # Сливаем
    result = merge_with_steps(sorted_left, sorted_right, level + 1)
    print(f"{indent}Результат слияния: {result}")
    
    return result


def merge_with_steps(left, right, level=0):
    """
    Слияние с выводом шагов
    """
    indent = "  " * level
    print(f"{indent}Сливаем {left} и {right}")
    
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            print(f"{indent}  {left[i]} <= {right[j]}, добавляем {left[i]}")
            result.append(left[i])
            i += 1
        else:
            print(f"{indent}  {left[i]} > {right[j]}, добавляем {right[j]}")
            result.append(right[j])
            j += 1
    
    # Добавляем оставшиеся элементы
    if i < len(left):
        print(f"{indent}  Добавляем оставшиеся из left: {left[i:]}")
        result.extend(left[i:])
    
    if j < len(right):
        print(f"{indent}  Добавляем оставшиеся из right: {right[j:]}")
        result.extend(right[j:])
    
    print(f"{indent}  Результат слияния: {result}")
    return result


# ============================================================================
# IN-PLACE ВЕРСИЯ
# ============================================================================

def merge_sort_inplace(arr, left=0, right=None):
    """
    In-place версия Merge Sort
    Сложность по памяти: O(log n) для стека вызовов
    """
    if right is None:
        right = len(arr) - 1
    
    if left < right:
        mid = (left + right) // 2
        
        # Рекурсивно сортируем половины
        merge_sort_inplace(arr, left, mid)
        merge_sort_inplace(arr, mid + 1, right)
        
        # Сливаем in-place
        merge_inplace(arr, left, mid, right)
    
    return arr


def merge_inplace(arr, left, mid, right):
    """
    In-place слияние двух частей массива
    """
    # Создаем временные массивы
    left_arr = arr[left:mid + 1]
    right_arr = arr[mid + 1:right + 1]
    
    i = j = 0
    k = left
    
    # Сливаем
    while i < len(left_arr) and j < len(right_arr):
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1
    
    # Копируем оставшиеся элементы
    while i < len(left_arr):
        arr[k] = left_arr[i]
        i += 1
        k += 1
    
    while j < len(right_arr):
        arr[k] = right_arr[j]
        j += 1
        k += 1


# ============================================================================
# ИТЕРАТИВНАЯ ВЕРСИЯ
# ============================================================================

def merge_sort_iterative(arr):
    """
    Итеративная версия Merge Sort
    """
    arr = arr.copy()
    n = len(arr)
    
    # Размер подмассива увеличивается в 2 раза на каждой итерации
    size = 1
    while size < n:
        # Объединяем подмассивы размером size
        for left in range(0, n, 2 * size):
            mid = min(left + size - 1, n - 1)
            right = min(left + 2 * size - 1, n - 1)
            
            # Сливаем подмассивы
            merge_iterative(arr, left, mid, right)
        
        size *= 2
    
    return arr


def merge_iterative(arr, left, mid, right):
    """
    Слияние для итеративной версии
    """
    left_arr = arr[left:mid + 1]
    right_arr = arr[mid + 1:right + 1]
    
    i = j = 0
    k = left
    
    while i < len(left_arr) and j < len(right_arr):
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1
    
    while i < len(left_arr):
        arr[k] = left_arr[i]
        i += 1
        k += 1
    
    while j < len(right_arr):
        arr[k] = right_arr[j]
        j += 1
        k += 1


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

def demonstrate_merge_sort():
    """
    Демонстрация работы алгоритма
    """
    print("=" * 60)
    print("MERGE SORT - Демонстрация")
    print("=" * 60)
    
    # Тест 1: Простой массив
    test_arr1 = [38, 27, 43, 3, 9, 82, 10]
    print(f"\nТест 1: {test_arr1}")
    result1 = merge_sort(test_arr1)
    print(f"Результат: {result1}")
    
    # Тест 2: Уже отсортированный массив
    test_arr2 = [1, 2, 3, 4, 5]
    print(f"\nТест 2 (уже отсортирован): {test_arr2}")
    result2 = merge_sort(test_arr2)
    print(f"Результат: {result2}")
    
    # Тест 3: Обратно отсортированный массив
    test_arr3 = [5, 4, 3, 2, 1]
    print(f"\nТест 3 (обратный порядок): {test_arr3}")
    result3 = merge_sort(test_arr3)
    print(f"Результат: {result3}")
    
    # Тест 4: Массив с дубликатами
    test_arr4 = [3, 1, 4, 1, 5, 9, 2, 6, 5]
    print(f"\nТест 4 (с дубликатами): {test_arr4}")
    result4 = merge_sort(test_arr4)
    print(f"Результат: {result4}")
    
    # Пошаговое исполнение
    print("\n" + "=" * 60)
    print("ПОШАГОВОЕ ИСПОЛНЕНИЕ на примере [6, 3, 8, 1]")
    print("=" * 60)
    merge_sort_with_steps([6, 3, 8, 1])
    
    # Сравнение версий
    print("\n" + "=" * 60)
    print("СРАВНЕНИЕ ВЕРСИЙ")
    print("=" * 60)
    
    test_arr = [64, 34, 25, 12, 22, 11, 90]
    print(f"Исходный массив: {test_arr}")
    print(f"Рекурсивная версия: {merge_sort(test_arr)}")
    print(f"In-place версия: {merge_sort_inplace(test_arr.copy())}")
    print(f"Итеративная версия: {merge_sort_iterative(test_arr)}")


# ============================================================================
# АНАЛИЗ СЛОЖНОСТИ
# ============================================================================

def analyze_complexity():
    """
    Детальный анализ сложности алгоритма
    """
    print("\n" + "=" * 60)
    print("АНАЛИЗ СЛОЖНОСТИ MERGE SORT")
    print("=" * 60)
    
    print("Временная сложность:")
    print("- Разделение массива: O(log n) уровней")
    print("- На каждом уровне: O(n) операций слияния")
    print("- Общая сложность: O(n log n)")
    print()
    print("Пространственная сложность:")
    print("- Рекурсивная версия: O(n) дополнительной памяти")
    print("- In-place версия: O(log n) для стека вызовов")
    print("- Итеративная версия: O(n) для временных массивов")
    print()
    print("Преимущества:")
    print("- Гарантированная O(n log n) сложность")
    print("- Стабильная сортировка")
    print("- Подходит для больших данных")
    print("- Предсказуемая производительность")
    print()
    print("Недостатки:")
    print("- Требует дополнительной памяти O(n)")
    print("- Не in-place (кроме специальной версии)")
    print("- Медленнее Quick Sort в среднем случае")


# ============================================================================
# ВИЗУАЛИЗАЦИЯ ДЕРЕВА РЕКУРСИИ
# ============================================================================

def visualize_recursion_tree(arr):
    """
    Визуализация дерева рекурсии
    """
    print("\n" + "=" * 60)
    print("ДЕРЕВО РЕКУРСИИ")
    print("=" * 60)
    
    def print_tree(arr, level=0, side=""):
        indent = "  " * level
        if level > 0:
            indent += f"[{side}] "
        
        if len(arr) <= 1:
            print(f"{indent}Лист: {arr}")
            return
        
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]
        
        print(f"{indent}Разделяем: {arr}")
        print_tree(left, level + 1, "L")
        print_tree(right, level + 1, "R")
    
    print_tree(arr)


# ============================================================================
# ПРИМЕНЕНИЕ В РЕАЛЬНЫХ ЗАДАЧАХ
# ============================================================================

def real_world_examples():
    """
    Примеры применения в реальных задачах
    """
    print("\n" + "=" * 60)
    print("ПРИМЕНЕНИЕ В РЕАЛЬНЫХ ЗАДАЧАХ")
    print("=" * 60)
    
    print("1. Сортировка больших файлов:")
    print("   - External Merge Sort для данных больше RAM")
    print("   - Разделение файла на блоки, сортировка каждого, слияние")
    
    print("\n2. Сортировка связанных списков:")
    print("   - Merge Sort идеален для linked list")
    print("   - O(1) дополнительной памяти для слияния")
    
    print("\n3. Параллельная сортировка:")
    print("   - Легко распараллеливается")
    print("   - Каждая половина сортируется независимо")
    
    print("\n4. Инверсии в массиве:")
    print("   - Подсчет инверсий с помощью модифицированного Merge Sort")
    print("   - O(n log n) сложность")
    
    print("\n5. Встроенные сортировки:")
    print("   - Timsort (Python) основан на Merge Sort")
    print("   - Java Arrays.sort() для объектов использует Merge Sort")


if __name__ == "__main__":
    demonstrate_merge_sort()
    analyze_complexity()
    visualize_recursion_tree([6, 3, 8, 1, 9, 2])
    real_world_examples()
