"""
🟢 FIBONACCI (Числа Фибоначчи)

Временная сложность:
- Наивная рекурсия: O(2^n) - экспоненциальная
- Мемоизация: O(n)
- Итеративная версия: O(n)
- Матричная версия: O(log n)

Пространственная сложность:
- Наивная рекурсия: O(n) - глубина стека
- Мемоизация: O(n)
- Итеративная версия: O(1)
- Матричная версия: O(log n)

Особенности:
- Классический пример неэффективной рекурсии
- Демонстрирует важность мемоизации
- Много оптимизаций и вариантов реализации
- Математическая последовательность: F(n) = F(n-1) + F(n-2)
"""


def fibonacci_naive(n):
    """
    🟢 Junior level
    Наивная рекурсивная версия (неэффективная)
    
    Принцип работы:
    1. Базовые случаи: F(0) = 0, F(1) = 1
    2. Рекурсивный случай: F(n) = F(n-1) + F(n-2)
    
    Проблема: вычисляет одни и те же значения многократно
    
    Args:
        n: номер числа Фибоначчи
        
    Returns:
        n-ное число Фибоначчи
        
    >>> fibonacci_naive(6)
    8
    """
    if n < 0:
        raise ValueError("Число Фибоначчи определено только для неотрицательных чисел")
    
    # Базовые случаи
    if n <= 1:
        return n
    
    # Рекурсивный случай
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)


def fibonacci_memoized(n, memo=None):
    """
    🟡 Middle level
    Мемоизированная версия - O(n)
    
    Использует кеширование для избежания повторных вычислений
    """
    if memo is None:
        memo = {}
    
    if n < 0:
        raise ValueError("Число Фибоначчи определено только для неотрицательных чисел")
    
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fibonacci_memoized(n - 1, memo) + fibonacci_memoized(n - 2, memo)
    return memo[n]


def fibonacci_iterative(n):
    """
    Итеративная версия - O(n), O(1) памяти
    """
    if n < 0:
        raise ValueError("Число Фибоначчи определено только для неотрицательных чисел")
    
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b


def fibonacci_matrix(n):
    """
    🔴 Senior level
    Матричная версия - O(log n)
    
    Использует быстрое возведение матрицы в степень
    """
    if n < 0:
        raise ValueError("Число Фибоначчи определено только для неотрицательных чисел")
    
    if n <= 1:
        return n
    
    def matrix_multiply(A, B):
        return [[A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
                [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]]
    
    def matrix_power(matrix, power):
        if power == 1:
            return matrix
        
        if power % 2 == 0:
            half = matrix_power(matrix, power // 2)
            return matrix_multiply(half, half)
        else:
            return matrix_multiply(matrix, matrix_power(matrix, power - 1))
    
    # Матрица для вычисления F(n)
    fib_matrix = [[1, 1], [1, 0]]
    result_matrix = matrix_power(fib_matrix, n - 1)
    
    return result_matrix[0][0]


# ============================================================================
# ПОШАГОВОЕ ИСПОЛНЕНИЕ
# ============================================================================

def fibonacci_with_steps(n, level=0, memo=None):
    """
    Версия с выводом пошагового исполнения
    """
    if memo is None:
        memo = {}
    
    indent = "  " * level
    print(f"{indent}Вызываем fibonacci({n})")
    
    if n < 0:
        raise ValueError("Число Фибоначчи определено только для неотрицательных чисел")
    
    if n in memo:
        print(f"{indent}Найдено в кеше: {memo[n]}")
        return memo[n]
    
    if n <= 1:
        print(f"{indent}Базовый случай: возвращаем {n}")
        return n
    
    print(f"{indent}Вычисляем fibonacci({n-1}) + fibonacci({n-2})")
    result = (fibonacci_with_steps(n - 1, level + 1, memo) + 
              fibonacci_with_steps(n - 2, level + 1, memo))
    
    memo[n] = result
    print(f"{indent}Результат: {result}")
    return result


# ============================================================================
# РАСШИРЕННЫЕ ВЕРСИИ
# ============================================================================

def fibonacci_sequence(n):
    """
    Генерирует последовательность Фибоначчи до n-ного числа
    """
    if n < 0:
        raise ValueError("Число Фибоначчи определено только для неотрицательных чисел")
    
    if n == 0:
        return [0]
    elif n == 1:
        return [0, 1]
    
    sequence = [0, 1]
    for i in range(2, n + 1):
        sequence.append(sequence[i-1] + sequence[i-2])
    
    return sequence


def fibonacci_generator(n):
    """
    Генератор чисел Фибоначчи
    """
    if n < 0:
        raise ValueError("Число Фибоначчи определено только для неотрицательных чисел")
    
    a, b = 0, 1
    for _ in range(n + 1):
        yield a
        a, b = b, a + b


def fibonacci_big_int(n):
    """
    Версия для больших чисел
    """
    if n < 0:
        raise ValueError("Число Фибоначчи определено только для неотрицательных чисел")
    
    if n <= 1:
        return str(n)
    
    a, b = "0", "1"
    for _ in range(2, n + 1):
        a, b = b, add_strings(a, b)
    
    return b


def add_strings(num1, num2):
    """
    Сложение больших чисел в виде строк
    """
    result = []
    carry = 0
    i, j = len(num1) - 1, len(num2) - 1
    
    while i >= 0 or j >= 0 or carry:
        total = carry
        if i >= 0:
            total += int(num1[i])
            i -= 1
        if j >= 0:
            total += int(num2[j])
            j -= 1
        
        result.append(str(total % 10))
        carry = total // 10
    
    return ''.join(reversed(result))


# ============================================================================
# МАТЕМАТИЧЕСКИЕ СВОЙСТВА
# ============================================================================

def fibonacci_ratio_convergence(n):
    """
    Проверяет сходимость отношения F(n+1)/F(n) к золотому сечению
    """
    if n < 1:
        return None
    
    fib_n = fibonacci_iterative(n)
    fib_n_plus_1 = fibonacci_iterative(n + 1)
    
    return fib_n_plus_1 / fib_n


def golden_ratio():
    """
    Золотое сечение φ = (1 + √5) / 2
    """
    import math
    return (1 + math.sqrt(5)) / 2


def fibonacci_binet(n):
    """
    Формула Бине для вычисления F(n)
    F(n) = (φ^n - ψ^n) / √5
    где φ = (1 + √5)/2, ψ = (1 - √5)/2
    """
    import math
    
    phi = (1 + math.sqrt(5)) / 2
    psi = (1 - math.sqrt(5)) / 2
    
    return round((phi**n - psi**n) / math.sqrt(5))


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

def demonstrate_fibonacci():
    """
    Демонстрация работы алгоритма
    """
    print("=" * 60)
    print("FIBONACCI - Демонстрация")
    print("=" * 60)
    
    # Тест 1: Базовые вычисления
    test_cases = [0, 1, 2, 3, 4, 5, 6, 10, 15]
    
    print("\nТест 1: Базовые вычисления")
    for n in test_cases:
        result = fibonacci_iterative(n)
        print(f"F({n}) = {result}")
    
    # Тест 2: Сравнение версий
    print(f"\nТест 2: Сравнение версий")
    n = 10
    print(f"n = {n}")
    print(f"Итеративная версия: {fibonacci_iterative(n)}")
    print(f"Мемоизированная версия: {fibonacci_memoized(n)}")
    print(f"Матричная версия: {fibonacci_matrix(n)}")
    print(f"Формула Бине: {fibonacci_binet(n)}")
    
    # Тест 3: Последовательность
    print(f"\nТест 3: Последовательность Фибоначчи")
    sequence = fibonacci_sequence(10)
    print(f"F(0) до F(10): {sequence}")
    
    # Тест 4: Генератор
    print(f"\nТест 4: Генератор")
    fib_gen = fibonacci_generator(10)
    print(f"Через генератор: {list(fib_gen)}")
    
    # Тест 5: Золотое сечение
    print(f"\nТест 5: Приближение к золотому сечению")
    phi = golden_ratio()
    print(f"Золотое сечение φ = {phi:.10f}")
    
    for n in [5, 10, 15, 20]:
        ratio = fibonacci_ratio_convergence(n)
        print(f"F({n+1})/F({n}) = {ratio:.10f}, ошибка: {abs(ratio - phi):.2e}")
    
    # Пошаговое исполнение
    print("\n" + "=" * 60)
    print("ПОШАГОВОЕ ИСПОЛНЕНИЕ (с мемоизацией)")
    print("=" * 60)
    fibonacci_with_steps(6)


# ============================================================================
# АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ
# ============================================================================

def performance_analysis():
    """
    Анализ производительности разных версий
    """
    import time
    
    print("\n" + "=" * 60)
    print("АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ")
    print("=" * 60)
    
    test_values = [10, 20, 30, 35]
    
    print("n\tИтеративная\tМемоизированная\tМатричная\tФормула Бине")
    print("-" * 70)
    
    for n in test_values:
        # Итеративная версия
        start = time.time()
        result1 = fibonacci_iterative(n)
        time1 = time.time() - start
        
        # Мемоизированная версия
        start = time.time()
        result2 = fibonacci_memoized(n)
        time2 = time.time() - start
        
        # Матричная версия
        start = time.time()
        result3 = fibonacci_matrix(n)
        time3 = time.time() - start
        
        # Формула Бине
        start = time.time()
        result4 = fibonacci_binet(n)
        time4 = time.time() - start
        
        print(f"{n}\t{time1*1000:.3f}ms\t\t{time2*1000:.3f}ms\t\t{time3*1000:.3f}ms\t\t{time4*1000:.3f}ms")
        
        # Проверяем корректность
        if not (result1 == result2 == result3 == result4):
            print(f"  ⚠️ Ошибка: результаты не совпадают для n={n}")


# ============================================================================
# ПРАКТИЧЕСКИЕ ПРИМЕНЕНИЯ
# ============================================================================

def practical_applications():
    """
    Практические применения чисел Фибоначчи
    """
    print("\n" + "=" * 60)
    print("ПРАКТИЧЕСКИЕ ПРИМЕНЕНИЯ")
    print("=" * 60)
    
    print("1. Природа и биология:")
    print("   - Спирали в растениях (подсолнухи, сосновые шишки)")
    print("   - Размножение кроликов")
    print("   - Структура листьев")
    
    print("\n2. Искусство и дизайн:")
    print("   - Золотое сечение в архитектуре")
    print("   - Пропорции в живописи")
    print("   - Дизайн интерфейсов")
    
    print("\n3. Финансы:")
    print("   - Технический анализ (уровни Фибоначчи)")
    print("   - Планирование инвестиций")
    print("   - Риск-менеджмент")
    
    print("\n4. Компьютерные науки:")
    print("   - Алгоритмы сортировки")
    print("   - Структуры данных (кучи Фибоначчи)")
    print("   - Хеширование")
    
    print("\n5. Математика:")
    print("   - Теория чисел")
    print("   - Комбинаторика")
    print("   - Диофантовы уравнения")


# ============================================================================
# ОПТИМИЗАЦИИ И ТРЮКИ
# ============================================================================

def optimizations_and_tricks():
    """
    Оптимизации и трюки для чисел Фибоначчи
    """
    print("\n" + "=" * 60)
    print("ОПТИМИЗАЦИИ И ТРЮКИ")
    print("=" * 60)
    
    print("1. Мемоизация:")
    print("   - Кеширование результатов")
    print("   - Избежание повторных вычислений")
    print("   - Снижение сложности с O(2^n) до O(n)")
    
    print("\n2. Итеративная версия:")
    print("   - O(1) дополнительной памяти")
    print("   - Избежание переполнения стека")
    print("   - Константное время на итерацию")
    
    print("\n3. Матричная версия:")
    print("   - O(log n) временная сложность")
    print("   - Быстрое возведение в степень")
    print("   - Подходит для очень больших n")
    
    print("\n4. Формула Бине:")
    print("   - O(1) вычисление")
    print("   - Точность ограничена точностью float")
    print("   - Хороша для приближенных вычислений")
    
    print("\n5. Работа с большими числами:")
    print("   - Строковое представление")
    print("   - Специальные библиотеки")
    print("   - Модульная арифметика")


# ============================================================================
# ОБЩИЕ ОШИБКИ
# ============================================================================

def common_mistakes():
    """
    Общие ошибки при работе с числами Фибоначчи
    """
    print("\n" + "=" * 60)
    print("ОБЩИЕ ОШИБКИ")
    print("=" * 60)
    
    print("1. Использование наивной рекурсии:")
    print("   ❌ fibonacci_naive(50) может работать очень долго")
    print("   ✅ Используйте мемоизацию или итеративную версию")
    
    print("\n2. Переполнение стека:")
    print("   ❌ fibonacci_naive(1000) вызовет StackOverflow")
    print("   ✅ Используйте итеративную или матричную версию")
    
    print("\n3. Переполнение целых чисел:")
    print("   ❌ F(100) > 2^63, может произойти переполнение")
    print("   ✅ Используйте строковое представление или библиотеки")
    
    print("\n4. Неточность формулы Бине:")
    print("   ❌ Для больших n может быть неточно")
    print("   ✅ Проверяйте точность или используйте другие методы")


if __name__ == "__main__":
    demonstrate_fibonacci()
    performance_analysis()
    practical_applications()
    optimizations_and_tricks()
    common_mistakes()
