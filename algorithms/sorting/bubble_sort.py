"""
🟢 BUBBLE SORT (Пузырьковая сортировка)

Временная сложность:
- Лучший случай: O(n) - когда массив уже отсортирован
- Средний случай: O(n²)
- Худший случай: O(n²) - когда массив отсортирован в обратном порядке

Пространственная сложность: O(1) - in-place алгоритм

Стабильность: Да (сохраняет порядок равных элементов)
"""


def bubble_sort(arr):
    """
    🟢 Junior level
    Пузырьковая сортировка - простейший алгоритм сортировки
    
    Принцип работы:
    1. Сравниваем соседние элементы попарно
    2. Если порядок неправильный, меняем их местами
    3. Повторяем для всех пар до конца массива
    4. Повторяем весь процесс, пока массив не отсортируется
    
    Args:
        arr: список для сортировки
        
    Returns:
        отсортированный список
        
    >>> bubble_sort([64, 34, 25, 12, 22, 11, 90])
    [11, 12, 22, 25, 34, 64, 90]
    """
    arr = arr.copy()
    n = len(arr)
    
    # Внешний цикл - количество проходов
    for i in range(n):
        swapped = False
        
        # Внутренний цикл - сравнение соседних элементов
        # n - i - 1 потому что последние i элементов уже на своих местах
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                # Меняем элементы местами
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # Оптимизация: если не было обменов, массив отсортирован
        if not swapped:
            break
    
    return arr


# ============================================================================
# ПОШАГОВОЕ ИСПОЛНЕНИЕ
# ============================================================================

def bubble_sort_with_steps(arr):
    """
    Версия с выводом пошагового исполнения
    """
    arr = arr.copy()
    n = len(arr)
    step = 0
    
    print(f"Исходный массив: {arr}")
    print(f"Длина массива: {n}")
    print("=" * 50)
    
    for i in range(n):
        print(f"\nПроход {i + 1}:")
        swapped = False
        
        for j in range(0, n - i - 1):
            step += 1
            print(f"  Шаг {step}: Сравниваем arr[{j}]={arr[j]} и arr[{j+1}]={arr[j+1]}")
            
            if arr[j] > arr[j + 1]:
                print(f"    {arr[j]} > {arr[j+1]}, меняем местами")
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                print(f"    Массив после обмена: {arr}")
                swapped = True
            else:
                print(f"    {arr[j]} <= {arr[j+1]}, не меняем")
        
        print(f"  Результат прохода {i + 1}: {arr}")
        
        if not swapped:
            print(f"  Не было обменов - массив отсортирован!")
            break
    
    print(f"\nИтоговый результат: {arr}")
    print(f"Общее количество сравнений: {step}")
    return arr


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

def demonstrate_bubble_sort():
    """
    Демонстрация работы алгоритма
    """
    print("=" * 60)
    print("BUBBLE SORT - Демонстрация")
    print("=" * 60)
    
    # Тест 1: Простой массив
    test_arr1 = [64, 34, 25, 12, 22, 11, 90]
    print(f"\nТест 1: {test_arr1}")
    result1 = bubble_sort(test_arr1)
    print(f"Результат: {result1}")
    
    # Тест 2: Уже отсортированный массив
    test_arr2 = [1, 2, 3, 4, 5]
    print(f"\nТест 2 (уже отсортирован): {test_arr2}")
    result2 = bubble_sort(test_arr2)
    print(f"Результат: {result2}")
    
    # Тест 3: Обратно отсортированный массив
    test_arr3 = [5, 4, 3, 2, 1]
    print(f"\nТест 3 (обратный порядок): {test_arr3}")
    result3 = bubble_sort(test_arr3)
    print(f"Результат: {result3}")
    
    # Тест 4: Массив с дубликатами
    test_arr4 = [3, 1, 4, 1, 5, 9, 2, 6, 5]
    print(f"\nТест 4 (с дубликатами): {test_arr4}")
    result4 = bubble_sort(test_arr4)
    print(f"Результат: {result4}")
    
    # Пошаговое исполнение
    print("\n" + "=" * 60)
    print("ПОШАГОВОЕ ИСПОЛНЕНИЕ на примере [5, 2, 8, 1, 9]")
    print("=" * 60)
    bubble_sort_with_steps([5, 2, 8, 1, 9])


# ============================================================================
# СРАВНЕНИЕ С ДРУГИМИ АЛГОРИТМАМИ
# ============================================================================

def compare_with_builtin():
    """
    Сравнение производительности с встроенной сортировкой
    """
    import time
    import random
    
    print("\n" + "=" * 60)
    print("СРАВНЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ")
    print("=" * 60)
    
    sizes = [100, 500, 1000]
    
    for size in sizes:
        # Генерируем случайный массив
        arr = [random.randint(1, 1000) for _ in range(size)]
        
        # Тестируем Bubble Sort
        start = time.time()
        bubble_result = bubble_sort(arr)
        bubble_time = time.time() - start
        
        # Тестируем встроенную сортировку
        start = time.time()
        builtin_result = sorted(arr)
        builtin_time = time.time() - start
        
        print(f"Размер массива: {size}")
        print(f"  Bubble Sort: {bubble_time*1000:.2f}ms")
        print(f"  Built-in:    {builtin_time*1000:.2f}ms")
        print(f"  Разница:     {bubble_time/builtin_time:.1f}x медленнее")
        print()


if __name__ == "__main__":
    demonstrate_bubble_sort()
    compare_with_builtin()
