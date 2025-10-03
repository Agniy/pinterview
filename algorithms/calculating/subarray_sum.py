"""
🟡 SUBARRAY SUM (Поиск подмассива с заданной суммой)

Временная сложность:
- O(n) - каждый элемент массива посещается максимум дважды

Пространственная сложность: O(1) - используем только константные переменные

Особенности:
- Алгоритм скользящего окна (sliding window)
- Работает только с неотрицательными числами
- Эффективный способ поиска подмассива с заданной суммой
- Использует технику двух указателей
"""


def subarray_sum(non_negative_arr, target):
    """
    🟡 Middle level
    Находит подмассив с заданной суммой используя технику скользящего окна
    
    Принцип работы:
    1. Используем два указателя: left и right
    2. Поддерживаем текущую сумму элементов в окне [left, right)
    3. Если сумма меньше target - расширяем окно вправо
    4. Если сумма больше target - сжимаем окно слева
    5. Если сумма равна target - возвращаем True
    
    Args:
        non_negative_arr: массив неотрицательных чисел
        target: целевая сумма
        
    Returns:
        True если найден подмассив с суммой target, иначе False
        
    >>> subarray_sum([1, 4, 20, 3, 10, 5], 33)
    True
    >>> subarray_sum([1, 4, 0, 0, 3, 10, 5], 7)
    True
    >>> subarray_sum([1, 4, 20, 3, 10, 5], 15)
    False
    """
    right, current_sum = 0, 0
    
    for left in range(len(non_negative_arr)):
        # Пересчитываем сумму при движении левой границы
        if left > 0:
            current_sum -= non_negative_arr[left - 1]
        
        # Расширяем окно вправо пока сумма меньше target
        while right < len(non_negative_arr) and current_sum < target:
            current_sum += non_negative_arr[right]
            right += 1
        
        # Проверяем, достигли ли целевой суммы
        if current_sum == target:
            return True
    
    return False


# ============================================================================
# ПОШАГОВОЕ ИСПОЛНЕНИЕ
# ============================================================================

def subarray_sum_with_steps(non_negative_arr, target):
    """
    Версия с выводом пошагового исполнения
    """
    print(f"Ищем подмассив с суммой {target} в массиве {non_negative_arr}")
    print("=" * 60)
    
    right, current_sum = 0, 0
    
    for left in range(len(non_negative_arr)):
        print(f"\nИтерация {left + 1}: left = {left}")
        
        # Пересчитываем сумму при движении левой границы
        if left > 0:
            print(f"  Убираем arr[{left-1}] = {non_negative_arr[left-1]}")
            current_sum -= non_negative_arr[left - 1]
            print(f"  Текущая сумма: {current_sum}")
        
        # Расширяем окно вправо
        print(f"  Расширяем окно с right = {right}")
        while right < len(non_negative_arr) and current_sum < target:
            print(f"    Добавляем arr[{right}] = {non_negative_arr[right]}")
            current_sum += non_negative_arr[right]
            right += 1
            print(f"    Текущая сумма: {current_sum}, right = {right}")
        
        # Проверяем результат
        print(f"  Окно: [{left}:{right}] = {non_negative_arr[left:right]}")
        print(f"  Сумма окна: {current_sum}")
        
        if current_sum == target:
            print(f"  ✓ Найдена сумма {target}!")
            print(f"  Подмассив: arr[{left}:{right}] = {non_negative_arr[left:right]}")
            return True
        elif current_sum > target:
            print(f"  Сумма {current_sum} > {target}, продолжаем")
        else:
            print(f"  Сумма {current_sum} < {target}, но массив закончился")
    
    print(f"\n✗ Подмассив с суммой {target} не найден")
    return False


# ============================================================================
# РАСШИРЕННЫЕ ВЕРСИИ
# ============================================================================

def subarray_sum_with_indices(non_negative_arr, target):
    """
    Возвращает индексы найденного подмассива
    """
    right, current_sum = 0, 0
    
    for left in range(len(non_negative_arr)):
        if left > 0:
            current_sum -= non_negative_arr[left - 1]
        
        while right < len(non_negative_arr) and current_sum < target:
            current_sum += non_negative_arr[right]
            right += 1
        
        if current_sum == target:
            return (left, right - 1)  # Возвращаем индексы (включительно)
    
    return None


def subarray_sum_all_occurrences(non_negative_arr, target):
    """
    Находит все подмассивы с заданной суммой
    """
    result = []
    right, current_sum = 0, 0
    
    for left in range(len(non_negative_arr)):
        if left > 0:
            current_sum -= non_negative_arr[left - 1]
        
        while right < len(non_negative_arr) and current_sum < target:
            current_sum += non_negative_arr[right]
            right += 1
        
        if current_sum == target:
            result.append((left, right - 1))
        
        # Продолжаем поиск, сдвигая левую границу
        # Это позволяет найти все возможные подмассивы
    
    return result


def subarray_sum_min_length(non_negative_arr, target):
    """
    Находит подмассив с заданной суммой минимальной длины
    """
    min_length = float('inf')
    result_indices = None
    right, current_sum = 0, 0
    
    for left in range(len(non_negative_arr)):
        if left > 0:
            current_sum -= non_negative_arr[left - 1]
        
        while right < len(non_negative_arr) and current_sum < target:
            current_sum += non_negative_arr[right]
            right += 1
        
        if current_sum == target:
            length = right - left
            if length < min_length:
                min_length = length
                result_indices = (left, right - 1)
    
    return result_indices if min_length != float('inf') else None


def subarray_sum_prefix_sums(non_negative_arr, target):
    """
    🟡 Middle level
    Второй вариант: поиск подмассива с заданной суммой через префиксные суммы
    
    Принцип работы:
    1. Вычисляем префиксные суммы для всех позиций
    2. Для каждой позиции ищем, есть ли префиксная сумма (prefix[i] - target)
    3. Если найдена, то подмассив от (prefix_sum_index + 1) до i имеет нужную сумму
    
    Args:
        non_negative_arr: массив неотрицательных чисел
        target: целевая сумма
        
    Returns:
        True если найден подмассив с суммой target, иначе False
        
    >>> subarray_sum_prefix_sums([1, 4, 20, 3, 10, 5], 33)
    True
    >>> subarray_sum_prefix_sums([1, 4, 0, 0, 3, 10, 5], 7)
    True
    """
    prefix_sum = {0: -1}  # Сумма 0 встречается перед индексом -1
    current_sum = 0
    
    for i, num in enumerate(non_negative_arr):
        current_sum += num
        
        # Ищем, встречалась ли раньше сумма (current_sum - target)
        if current_sum - target in prefix_sum:
            return True
        
        # Сохраняем текущую сумму только если её ещё нет
        # Для неотрицательных чисел это гарантирует левую границу
        if current_sum not in prefix_sum:
            prefix_sum[current_sum] = i
    
    return False


def subarray_sum_with_negative(arr, target):
    """
    Версия для массива с отрицательными числами
    Использует хеш-таблицу для хранения сумм
    """
    prefix_sum = {0: -1}  # Сумма 0 встречается перед индексом -1
    current_sum = 0
    
    for i, num in enumerate(arr):
        current_sum += num
        
        # Ищем, встречалась ли раньше сумма (current_sum - target)
        if current_sum - target in prefix_sum:
            start_idx = prefix_sum[current_sum - target] + 1
            return (start_idx, i)
        
        # Сохраняем текущую сумму
        if current_sum not in prefix_sum:
            prefix_sum[current_sum] = i
    
    return None


def subarray_sum_prefix_sums_with_steps(non_negative_arr, target):
    """
    Пошаговое исполнение второго варианта с префиксными суммами
    """
    print(f"Второй вариант: Поиск подмассива с суммой {target} через префиксные суммы")
    print(f"Массив: {non_negative_arr}")
    print("=" * 70)
    
    prefix_sum = {0: -1}  # Сумма 0 встречается перед индексом -1
    current_sum = 0
    
    print("Инициализация:")
    print(f"  prefix_sum = {prefix_sum}")
    print(f"  current_sum = {current_sum}")
    print()
    
    for i, num in enumerate(non_negative_arr):
        print(f"Шаг {i + 1}: arr[{i}] = {num}")
        
        # Вычисляем текущую префиксную сумму
        current_sum += num
        print(f"  current_sum = {current_sum}")
        
        # Ищем нужную сумму
        needed_sum = current_sum - target
        print(f"  Ищем префиксную сумму: {needed_sum}")
        print(f"  Текущие префиксные суммы: {list(prefix_sum.keys())}")
        
        if needed_sum in prefix_sum:
            start_idx = prefix_sum[needed_sum] + 1
            print(f"  ✓ Найдена префиксная сумма {needed_sum} на позиции {prefix_sum[needed_sum]}")
            print(f"  ✓ Подмассив arr[{start_idx}:{i+1}] = {non_negative_arr[start_idx:i+1]}")
            print(f"  ✓ Сумма подмассива: {sum(non_negative_arr[start_idx:i+1])} = {target}")
            return True
        
        # Сохраняем текущую сумму
        if current_sum not in prefix_sum:
            prefix_sum[current_sum] = i
            print(f"  Сохраняем префиксную сумму {current_sum} на позиции {i}")
        else:
            print(f"  Префиксная сумма {current_sum} уже существует")
        
        print(f"  Обновленный prefix_sum: {prefix_sum}")
        print()
    
    print("✗ Подмассив с заданной суммой не найден")
    return False


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

def demonstrate_subarray_sum():
    """
    Демонстрация работы алгоритма
    """
    print("=" * 60)
    print("SUBARRAY SUM - Демонстрация")
    print("=" * 60)
    
    # Тест 1: Базовый случай
    test_arr1 = [1, 4, 20, 3, 10, 5]
    target1 = 33
    print(f"\nТест 1: Массив {test_arr1}, ищем сумму {target1}")
    result1 = subarray_sum(test_arr1, target1)
    print(f"Результат: {result1}")
    
    # Тест 2: С нулями
    test_arr2 = [1, 4, 0, 0, 3, 10, 5]
    target2 = 7
    print(f"\nТест 2: Массив {test_arr2}, ищем сумму {target2}")
    result2 = subarray_sum(test_arr2, target2)
    print(f"Результат: {result2}")
    
    # Тест 3: Не найдено
    test_arr3 = [1, 4, 20, 3, 10, 5]
    target3 = 15
    print(f"\nТест 3: Массив {test_arr3}, ищем сумму {target3}")
    result3 = subarray_sum(test_arr3, target3)
    print(f"Результат: {result3}")
    
    # Тест 4: Один элемент
    test_arr4 = [5]
    target4 = 5
    print(f"\nТест 4: Массив {test_arr4}, ищем сумму {target4}")
    result4 = subarray_sum(test_arr4, target4)
    print(f"Результат: {result4}")
    
    # Тест 5: С индексами
    test_arr5 = [1, 4, 20, 3, 10, 5]
    target5 = 33
    print(f"\nТест 5: Массив {test_arr5}, ищем сумму {target5}")
    indices = subarray_sum_with_indices(test_arr5, target5)
    if indices:
        start, end = indices
        print(f"Найдено: индексы [{start}:{end+1}] = {test_arr5[start:end+1]}")
    else:
        print("Не найдено")
    
    # Сравнение двух вариантов
    print("\n" + "=" * 60)
    print("СРАВНЕНИЕ ДВУХ ВАРИАНТОВ")
    print("=" * 60)
    
    test_arr = [1, 4, 20, 3, 10, 5]
    target = 33
    print(f"Массив: {test_arr}, целевая сумма: {target}")
    print(f"Вариант 1 (скользящее окно): {subarray_sum(test_arr, target)}")
    print(f"Вариант 2 (префиксные суммы): {subarray_sum_prefix_sums(test_arr, target)}")
    
    # Пошаговое исполнение
    print("\n" + "=" * 60)
    print("ПОШАГОВОЕ ИСПОЛНЕНИЕ - ВАРИАНТ 1 (Скользящее окно)")
    print("=" * 60)
    subarray_sum_with_steps([1, 4, 20, 3, 10, 5], 33)
    
    print("\n" + "=" * 60)
    print("ПОШАГОВОЕ ИСПОЛНЕНИЕ - ВАРИАНТ 2 (Префиксные суммы)")
    print("=" * 60)
    subarray_sum_prefix_sums_with_steps([1, 4, 20, 3, 10, 5], 33)


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
    
    sizes = [100, 1000, 10000]
    
    for size in sizes:
        # Генерируем случайный массив
        arr = [random.randint(1, 100) for _ in range(size)]
        target = random.randint(50, size * 50)
        
        # Тестируем производительность
        start = time.time()
        result = subarray_sum(arr, target)
        end = time.time()
        
        print(f"\nРазмер массива: {size}")
        print(f"Целевая сумма: {target}")
        print(f"Результат: {result}")
        print(f"Время выполнения: {(end - start)*1000:.3f}ms")


# ============================================================================
# СРАВНЕНИЕ С ДРУГИМИ ПОДХОДАМИ
# ============================================================================

def compare_approaches():
    """
    Сравнение с другими подходами
    """
    print("\n" + "=" * 60)
    print("СРАВНЕНИЕ ПОДХОДОВ")
    print("=" * 60)
    
    print("1. Наивный подход (все подмассивы):")
    print("   - Временная сложность: O(n²)")
    print("   - Проверяет все возможные подмассивы")
    print("   - Простая реализация, но неэффективная")
    
    print("\n2. Алгоритм скользящего окна (Вариант 1):")
    print("   - Временная сложность: O(n)")
    print("   - Пространственная сложность: O(1)")
    print("   - Использует свойство неотрицательности")
    print("   - Эффективный и элегантный")
    print("   - Два указателя: left и right")
    
    print("\n3. Префиксные суммы (Вариант 2):")
    print("   - Временная сложность: O(n)")
    print("   - Пространственная сложность: O(n)")
    print("   - Использует хеш-таблицу для хранения сумм")
    print("   - Более универсальный подход")
    print("   - Легко адаптируется для отрицательных чисел")
    
    print("\n4. Хеш-таблица (для любых чисел):")
    print("   - Временная сложность: O(n)")
    print("   - Пространственная сложность: O(n)")
    print("   - Работает с отрицательными числами")
    print("   - Аналогичен варианту 2, но без ограничений")


# ============================================================================
# ПРАКТИЧЕСКИЕ ПРИМЕНЕНИЯ
# ============================================================================

def practical_applications():
    """
    Практические применения
    """
    print("\n" + "=" * 60)
    print("ПРАКТИЧЕСКИЕ ПРИМЕНЕНИЯ")
    print("=" * 60)
    
    print("1. Финансовые приложения:")
    print("   - Поиск периода с заданной прибылью")
    print("   - Анализ временных рядов")
    print("   - Поиск трендов в данных")
    
    print("\n2. Анализ данных:")
    print("   - Поиск сегментов с заданными характеристиками")
    print("   - Анализ производительности")
    print("   - Поиск аномалий в данных")
    
    print("\n3. Игровая разработка:")
    print("   - Поиск комбинаций с заданным эффектом")
    print("   - Балансировка игровых механик")
    print("   - Анализ прогрессии игрока")
    
    print("\n4. Обработка сигналов:")
    print("   - Поиск сегментов с заданной энергией")
    print("   - Анализ аудио/видео данных")
    print("   - Фильтрация сигналов")


# ============================================================================
# ОГРАНИЧЕНИЯ И ТРЕБОВАНИЯ
# ============================================================================

def limitations_and_requirements():
    """
    Ограничения и требования алгоритма
    """
    print("\n" + "=" * 60)
    print("ОГРАНИЧЕНИЯ И ТРЕБОВАНИЯ")
    print("=" * 60)
    
    print("Требования:")
    print("✓ Массив должен содержать только неотрицательные числа")
    print("✓ Целевая сумма должна быть неотрицательной")
    print("✓ Массив не должен быть пустым")
    
    print("\nОграничения:")
    print("✗ Не работает с отрицательными числами")
    print("✗ Находит только первый подходящий подмассив")
    print("✗ Возвращает только True/False (не индексы)")
    
    print("\nАльтернативы:")
    print("- Для массивов с отрицательными числами используйте хеш-таблицу")
    print("- Для поиска всех подмассивов используйте модифицированную версию")
    print("- Для поиска минимальной длины используйте специальную версию")


# ============================================================================
# ОБЩИЕ ОШИБКИ
# ============================================================================

def common_mistakes():
    """
    Общие ошибки при реализации
    """
    print("\n" + "=" * 60)
    print("ОБЩИЕ ОШИБКИ")
    print("=" * 60)
    
    print("1. Забывание проверки на неотрицательность:")
    print("   ❌ Алгоритм может работать неправильно с отрицательными числами")
    print("   ✅ Всегда проверяйте входные данные")
    
    print("\n2. Неправильная работа с границами:")
    print("   ❌ right может выйти за границы массива")
    print("   ✅ Всегда проверяйте границы в while цикле")
    
    print("\n3. Неточность в обновлении суммы:")
    print("   ❌ Забывание вычесть элемент при движении left")
    print("   ✅ Всегда корректно обновляйте current_sum")
    
    print("\n4. Неэффективная реализация:")
    print("   ❌ Использование вложенных циклов O(n²)")
    print("   ✅ Используйте технику скользящего окна O(n)")


if __name__ == "__main__":
    demonstrate_subarray_sum()
    performance_analysis()
    compare_approaches()
    practical_applications()
    limitations_and_requirements()
    common_mistakes()
