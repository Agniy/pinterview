"""
🟡 АЛГОРИТМЫ СОРТИРОВКИ - Вопросы и задачи для собеседований

Основные темы:
- Bubble Sort, Selection Sort, Insertion Sort
- Merge Sort, Quick Sort
- Heap Sort
- Сложность алгоритмов
"""

import time
import random


# ============================================================================
# ТЕОРЕТИЧЕСКИЕ ВОПРОСЫ
# ============================================================================

"""
Q1: Какие основные алгоритмы сортировки вы знаете?
A:
- O(n²): Bubble, Selection, Insertion
- O(n log n): Merge, Quick, Heap
- O(n): Counting, Radix (для специальных случаев)

Q2: Какой встроенный алгоритм сортировки в Python?
A: Timsort (гибрид Merge Sort и Insertion Sort), O(n log n)

Q3: Что такое стабильная сортировка?
A: Сохраняет относительный порядок равных элементов

Q4: В чем разница между in-place и not in-place сортировкой?
A:
- In-place: сортирует массив на месте, O(1) памяти
- Not in-place: создает новый массив, O(n) памяти
"""


# ============================================================================
# ЗАДАЧА 1: Bubble Sort (Пузырьковая сортировка)
# ============================================================================

def bubble_sort(arr):
    """
    🟢 Junior level
    Пузырьковая сортировка - O(n²)
    
    >>> bubble_sort([64, 34, 25, 12, 22, 11, 90])
    [11, 12, 22, 25, 34, 64, 90]
    """
    arr = arr.copy()
    n = len(arr)
    
    for i in range(n):
        swapped = False
        
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # Если не было обменов, массив отсортирован
        if not swapped:
            break
    
    return arr


# ============================================================================
# ЗАДАЧА 2: Selection Sort (Сортировка выбором)
# ============================================================================

def selection_sort(arr):
    """
    🟢 Junior level
    Сортировка выбором - O(n²)
    
    >>> selection_sort([64, 25, 12, 22, 11])
    [11, 12, 22, 25, 64]
    """
    arr = arr.copy()
    n = len(arr)
    
    for i in range(n):
        # Находим минимум в оставшейся части
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        # Меняем местами
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    
    return arr


# ============================================================================
# ЗАДАЧА 3: Insertion Sort (Сортировка вставками)
# ============================================================================

def insertion_sort(arr):
    """
    🟢 Junior level
    Сортировка вставками - O(n²)
    Эффективна для почти отсортированных массивов
    
    >>> insertion_sort([12, 11, 13, 5, 6])
    [5, 6, 11, 12, 13]
    """
    arr = arr.copy()
    
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        # Сдвигаем элементы больше key вправо
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
    
    return arr


# ============================================================================
# ЗАДАЧА 4: Merge Sort (Сортировка слиянием)
# ============================================================================

def merge_sort(arr):
    """
    🟡 Middle level
    Сортировка слиянием - O(n log n)
    Стабильная, не in-place
    
    >>> merge_sort([38, 27, 43, 3, 9, 82, 10])
    [3, 9, 10, 27, 38, 43, 82]
    """
    if len(arr) <= 1:
        return arr
    
    # Разделяем
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    # Сливаем
    return merge(left, right)


def merge(left, right):
    """Слияние двух отсортированных массивов"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result


# ============================================================================
# ЗАДАЧА 5: Quick Sort (Быстрая сортировка)
# ============================================================================

def quick_sort(arr):
    """
    🟡 Middle level
    Быстрая сортировка - O(n log n) в среднем, O(n²) в худшем
    In-place версия
    
    >>> quick_sort([10, 7, 8, 9, 1, 5])
    [1, 5, 7, 8, 9, 10]
    """
    arr = arr.copy()
    _quick_sort_helper(arr, 0, len(arr) - 1)
    return arr


def _quick_sort_helper(arr, low, high):
    """Вспомогательная рекурсивная функция"""
    if low < high:
        # Находим позицию pivot
        pi = partition(arr, low, high)
        
        # Рекурсивно сортируем части
        _quick_sort_helper(arr, low, pi - 1)
        _quick_sort_helper(arr, pi + 1, high)


def partition(arr, low, high):
    """Разделение массива по pivot"""
    pivot = arr[high]  # Выбираем последний элемент как pivot
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# Более компактная версия (не in-place)
def quick_sort_compact(arr):
    """
    🟡 Middle level
    Компактная версия Quick Sort
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort_compact(left) + middle + quick_sort_compact(right)


# ============================================================================
# ЗАДАЧА 6: Heap Sort (Пирамидальная сортировка)
# ============================================================================

def heap_sort(arr):
    """
    🔴 Senior level
    Пирамидальная сортировка - O(n log n)
    In-place, не стабильная
    
    >>> heap_sort([12, 11, 13, 5, 6, 7])
    [5, 6, 7, 11, 12, 13]
    """
    arr = arr.copy()
    n = len(arr)
    
    # Строим max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # Извлекаем элементы из heap
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    
    return arr


def heapify(arr, n, i):
    """Превращает поддерево с корнем i в max heap"""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


# ============================================================================
# ЗАДАЧА 7: Counting Sort (Сортировка подсчетом)
# ============================================================================

def counting_sort(arr):
    """
    🟡 Middle level
    Сортировка подсчетом - O(n + k), где k - диапазон значений
    Работает только для целых неотрицательных чисел
    
    >>> counting_sort([4, 2, 2, 8, 3, 3, 1])
    [1, 2, 2, 3, 3, 4, 8]
    """
    if not arr:
        return arr
    
    # Находим диапазон
    max_val = max(arr)
    min_val = min(arr)
    range_size = max_val - min_val + 1
    
    # Подсчитываем частоты
    count = [0] * range_size
    for num in arr:
        count[num - min_val] += 1
    
    # Строим результат
    result = []
    for i, freq in enumerate(count):
        result.extend([i + min_val] * freq)
    
    return result


# ============================================================================
# ЗАДАЧА 8: Сортировка по ключу (Key Sort)
# ============================================================================

def sort_by_key_example():
    """
    🟢 Junior level
    Примеры сортировки с ключом
    """
    
    # Сортировка кортежей
    students = [
        ("Alice", 25, 85),
        ("Bob", 22, 90),
        ("Charlie", 25, 80)
    ]
    
    print("По возрасту:")
    print(sorted(students, key=lambda x: x[1]))
    
    print("\nПо оценке (убывание):")
    print(sorted(students, key=lambda x: x[2], reverse=True))
    
    print("\nПо возрасту, потом оценке:")
    print(sorted(students, key=lambda x: (x[1], -x[2])))
    
    # Сортировка словарей
    people = [
        {'name': 'Alice', 'age': 30},
        {'name': 'Bob', 'age': 25},
        {'name': 'Charlie', 'age': 30}
    ]
    
    print("\nСловари по возрасту:")
    print(sorted(people, key=lambda x: x['age']))


# ============================================================================
# ЗАДАЧА 9: Топологическая сортировка
# ============================================================================

def topological_sort(graph):
    """
    🔴 Senior level
    Топологическая сортировка графа
    
    graph: {node: [dependencies]}
    >>> graph = {'A': [], 'B': ['A'], 'C': ['A'], 'D': ['B', 'C']}
    >>> topological_sort(graph)
    ['A', 'B', 'C', 'D'] (или ['A', 'C', 'B', 'D'])
    """
    visited = set()
    stack = []
    
    def dfs(node):
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(node)
    
    for node in graph:
        if node not in visited:
            dfs(node)
    
    return stack[::-1]


# ============================================================================
# ЗАДАЧА 10: Сравнение производительности
# ============================================================================

def benchmark_sorting():
    """
    🟡 Middle level
    Сравнение производительности алгоритмов
    """
    
    # Генерируем тестовые данные
    sizes = [100, 500, 1000]
    algorithms = [
        ("Bubble Sort", bubble_sort),
        ("Selection Sort", selection_sort),
        ("Insertion Sort", insertion_sort),
        ("Merge Sort", merge_sort),
        ("Quick Sort", quick_sort),
        ("Heap Sort", heap_sort),
        ("Counting Sort", counting_sort),
        ("Built-in sorted()", sorted)
    ]
    
    print("Сравнение алгоритмов сортировки:")
    print("-" * 60)
    
    for size in sizes:
        print(f"\nРазмер массива: {size}")
        arr = [random.randint(0, 1000) for _ in range(size)]
        
        for name, algo in algorithms:
            test_arr = arr.copy()
            
            start = time.time()
            result = algo(test_arr)
            end = time.time()
            
            print(f"  {name:20s}: {(end - start)*1000:.2f}ms")


# ============================================================================
# ЗАДАЧА 11: Специальные случаи
# ============================================================================

def sort_special_cases():
    """
    🟡 Middle level
    Специальные случаи сортировки
    """
    
    # Сортировка 0, 1, 2 (Dutch National Flag)
    def sort_012(arr):
        """O(n) для массива с тремя уникальными значениями"""
        low = mid = 0
        high = len(arr) - 1
        
        while mid <= high:
            if arr[mid] == 0:
                arr[low], arr[mid] = arr[mid], arr[low]
                low += 1
                mid += 1
            elif arr[mid] == 1:
                mid += 1
            else:
                arr[mid], arr[high] = arr[high], arr[mid]
                high -= 1
        
        return arr
    
    print("Сортировка 0, 1, 2:")
    print(sort_012([0, 1, 2, 0, 1, 2, 1, 0]))
    
    # Сортировка по частоте
    def sort_by_frequency(arr):
        """Сортирует элементы по частоте встречаемости"""
        from collections import Counter
        counts = Counter(arr)
        return sorted(arr, key=lambda x: (-counts[x], x))
    
    print("\nСортировка по частоте:")
    print(sort_by_frequency([4, 5, 6, 5, 4, 3, 4]))


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("АЛГОРИТМЫ СОРТИРОВКИ - Примеры и тесты")
    print("=" * 60)
    
    test_arr = [64, 34, 25, 12, 22, 11, 90]
    
    # Тест всех алгоритмов
    print(f"\nИсходный массив: {test_arr}")
    
    print(f"\nBubble Sort:    {bubble_sort(test_arr)}")
    print(f"Selection Sort: {selection_sort(test_arr)}")
    print(f"Insertion Sort: {insertion_sort(test_arr)}")
    print(f"Merge Sort:     {merge_sort(test_arr)}")
    print(f"Quick Sort:     {quick_sort(test_arr)}")
    print(f"Heap Sort:      {heap_sort(test_arr)}")
    print(f"Counting Sort:  {counting_sort(test_arr)}")
    
    # Сортировка с ключом
    print("\n" + "=" * 60)
    print("Сортировка с ключом:")
    sort_by_key_example()
    
    # Специальные случаи
    print("\n" + "=" * 60)
    print("Специальные случаи:")
    sort_special_cases()
    
    # Benchmark (только для небольших размеров)
    print("\n" + "=" * 60)
    benchmark_sorting()
    
    print("\n" + "=" * 60)

