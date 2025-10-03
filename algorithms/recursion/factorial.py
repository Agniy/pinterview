"""
🟢 FACTORIAL (Факториал)

Временная сложность:
- Рекурсивная версия: O(n)
- Итеративная версия: O(n)

Пространственная сложность:
- Рекурсивная версия: O(n) - глубина стека вызовов
- Итеративная версия: O(1)

Особенности:
- Классический пример рекурсии
- Простая реализация для изучения базовых принципов
- Основа для понимания рекурсивного мышления
- Математическая функция: n! = n × (n-1) × (n-2) × ... × 1
"""


def factorial(n):
    """
    🟢 Junior level
    Вычисление факториала рекурсивно
    
    Принцип работы:
    1. Базовый случай: если n <= 1, возвращаем 1
    2. Рекурсивный случай: возвращаем n * factorial(n-1)
    
    Математическое определение:
    n! = n × (n-1)!
    0! = 1
    1! = 1
    
    Args:
        n: неотрицательное целое число
        
    Returns:
        факториал числа n
        
    >>> factorial(5)
    120
    >>> factorial(0)
    1
    >>> factorial(1)
    1
    """
    if n < 0:
        raise ValueError("Факториал определен только для неотрицательных чисел")
    
    # Базовый случай
    if n <= 1:
        return 1
    
    # Рекурсивный случай
    return n * factorial(n - 1)


def factorial_iterative(n):
    """
    Итеративная версия факториала
    
    >>> factorial_iterative(5)
    120
    """
    if n < 0:
        raise ValueError("Факториал определен только для неотрицательных чисел")
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    
    return result


def factorial_memoized(n, memo=None):
    """
    Мемоизированная версия (для демонстрации, здесь не очень полезна)
    """
    if memo is None:
        memo = {}
    
    if n < 0:
        raise ValueError("Факториал определен только для неотрицательных чисел")
    
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return 1
    
    memo[n] = n * factorial_memoized(n - 1, memo)
    return memo[n]


# ============================================================================
# ПОШАГОВОЕ ИСПОЛНЕНИЕ
# ============================================================================

def factorial_with_steps(n, level=0):
    """
    Версия с выводом пошагового исполнения
    """
    indent = "  " * level
    print(f"{indent}Вызываем factorial({n})")
    
    if n < 0:
        raise ValueError("Факториал определен только для неотрицательных чисел")
    
    if n <= 1:
        print(f"{indent}Базовый случай: возвращаем 1")
        return 1
    
    print(f"{indent}Рекурсивный вызов: {n} * factorial({n-1})")
    result = n * factorial_with_steps(n - 1, level + 1)
    print(f"{indent}Результат: {n} * {result // n} = {result}")
    
    return result


# ============================================================================
# РАСШИРЕННЫЕ ВЕРСИИ
# ============================================================================

def factorial_tail_recursive(n, accumulator=1):
    """
    Хвостовая рекурсия (Python не оптимизирует, но хорошая практика)
    """
    if n < 0:
        raise ValueError("Факториал определен только для неотрицательных чисел")
    
    if n <= 1:
        return accumulator
    
    return factorial_tail_recursive(n - 1, n * accumulator)


def factorial_big_int(n):
    """
    Версия для больших чисел с использованием строк
    """
    if n < 0:
        raise ValueError("Факториал определен только для неотрицательных чисел")
    
    if n <= 1:
        return "1"
    
    result = "1"
    for i in range(2, n + 1):
        result = multiply_strings(result, str(i))
    
    return result


def multiply_strings(num1, num2):
    """
    Умножение больших чисел в виде строк
    """
    m, n = len(num1), len(num2)
    result = [0] * (m + n)
    
    # Умножаем каждую цифру
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            mul = int(num1[i]) * int(num2[j])
            p1, p2 = i + j, i + j + 1
            total = mul + result[p2]
            
            result[p2] = total % 10
            result[p1] += total // 10
    
    # Убираем ведущие нули
    start = 0
    while start < len(result) and result[start] == 0:
        start += 1
    
    return ''.join(map(str, result[start:])) if start < len(result) else '0'


# ============================================================================
# МАТЕМАТИЧЕСКИЕ СВОЙСТВА
# ============================================================================

def stirling_approximation(n):
    """
    Приближение Стирлинга для факториала
    n! ≈ √(2πn) * (n/e)^n
    """
    import math
    return math.sqrt(2 * math.pi * n) * (n / math.e) ** n


def factorial_ratio(n, k):
    """
    Отношение факториалов n! / k!
    """
    if k > n:
        return 0
    
    result = 1
    for i in range(k + 1, n + 1):
        result *= i
    
    return result


def gamma_function_approximation(n):
    """
    Приближение через гамма-функцию
    n! = Γ(n+1)
    """
    import math
    return math.gamma(n + 1)


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

def demonstrate_factorial():
    """
    Демонстрация работы алгоритма
    """
    print("=" * 60)
    print("FACTORIAL - Демонстрация")
    print("=" * 60)
    
    # Тест 1: Базовые случаи
    test_cases = [0, 1, 2, 3, 4, 5, 10]
    
    print("\nТест 1: Базовые вычисления")
    for n in test_cases:
        result = factorial(n)
        print(f"{n}! = {result}")
    
    # Тест 2: Сравнение версий
    print(f"\nТест 2: Сравнение версий")
    n = 5
    print(f"n = {n}")
    print(f"Рекурсивная версия: {factorial(n)}")
    print(f"Итеративная версия: {factorial_iterative(n)}")
    print(f"Мемоизированная версия: {factorial_memoized(n)}")
    print(f"Хвостовая рекурсия: {factorial_tail_recursive(n)}")
    
    # Тест 3: Пошаговое исполнение
    print(f"\nТест 3: Пошаговое исполнение factorial(4)")
    print("=" * 40)
    factorial_with_steps(4)
    
    # Тест 4: Большие числа
    print(f"\nТест 4: Большие числа")
    large_n = 20
    print(f"{large_n}! = {factorial_big_int(large_n)}")
    
    # Тест 5: Приближения
    print(f"\nТест 5: Приближения")
    n = 10
    exact = factorial(n)
    stirling = stirling_approximation(n)
    gamma = gamma_function_approximation(n)
    
    print(f"n = {n}")
    print(f"Точное значение: {exact}")
    print(f"Приближение Стирлинга: {stirling:.0f}")
    print(f"Гамма-функция: {gamma:.0f}")
    print(f"Ошибка Стирлинга: {abs(exact - stirling) / exact * 100:.2f}%")


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
    
    test_values = [5, 10, 15, 20]
    
    print("n\tРекурсивная\tИтеративная\tМемоизированная")
    print("-" * 55)
    
    for n in test_values:
        # Рекурсивная версия
        start = time.time()
        factorial(n)
        recursive_time = time.time() - start
        
        # Итеративная версия
        start = time.time()
        factorial_iterative(n)
        iterative_time = time.time() - start
        
        # Мемоизированная версия
        start = time.time()
        factorial_memoized(n)
        memoized_time = time.time() - start
        
        print(f"{n}\t{recursive_time*1000:.3f}ms\t\t{iterative_time*1000:.3f}ms\t\t{memoized_time*1000:.3f}ms")


# ============================================================================
# ПРАКТИЧЕСКИЕ ПРИМЕНЕНИЯ
# ============================================================================

def practical_applications():
    """
    Практические применения факториала
    """
    print("\n" + "=" * 60)
    print("ПРАКТИЧЕСКИЕ ПРИМЕНЕНИЯ ФАКТОРИАЛА")
    print("=" * 60)
    
    print("1. Комбинаторика:")
    print("   - Перестановки: n! способов расставить n элементов")
    print("   - Сочетания: C(n,k) = n! / (k! * (n-k)!)")
    print("   - Размещения: A(n,k) = n! / (n-k)!")
    
    print("\n2. Теория вероятностей:")
    print("   - Равновероятные исходы")
    print("   - Байесовская статистика")
    print("   - Распределения")
    
    print("\n3. Математический анализ:")
    print("   - Ряды Тейлора")
    print("   - Асимптотические разложения")
    print("   - Гамма-функция")
    
    print("\n4. Алгоритмы:")
    print("   - Генерация перестановок")
    print("   - Backtracking")
    print("   - Рекурсивные алгоритмы")
    
    print("\n5. Физика:")
    print("   - Статистическая механика")
    print("   - Квантовая механика")
    print("   - Термодинамика")


# ============================================================================
# ОБЩИЕ ОШИБКИ
# ============================================================================

def common_mistakes():
    """
    Общие ошибки при работе с факториалом
    """
    print("\n" + "=" * 60)
    print("ОБЩИЕ ОШИБКИ")
    print("=" * 60)
    
    print("1. Забывание базового случая:")
    print("   ❌ def factorial(n): return n * factorial(n-1)")
    print("   ✅ def factorial(n): return 1 if n <= 1 else n * factorial(n-1)")
    
    print("\n2. Неправильная обработка отрицательных чисел:")
    print("   ❌ Факториал отрицательного числа не определен!")
    print("   ✅ Всегда проверяйте входные данные")
    
    print("\n3. Переполнение стека:")
    print("   ❌ factorial(1000) может вызвать StackOverflow")
    print("   ✅ Используйте итеративную версию для больших чисел")
    
    print("\n4. Переполнение целых чисел:")
    print("   ❌ 20! > 2^63, может произойти переполнение")
    print("   ✅ Используйте специальные библиотеки для больших чисел")


# ============================================================================
# СВЯЗАННЫЕ ФУНКЦИИ
# ============================================================================

def related_functions():
    """
    Связанные математические функции
    """
    print("\n" + "=" * 60)
    print("СВЯЗАННЫЕ ФУНКЦИИ")
    print("=" * 60)
    
    print("1. Двойной факториал:")
    print("   n!! = n * (n-2) * (n-4) * ...")
    print("   5!! = 5 * 3 * 1 = 15")
    
    print("\n2. Суперфакториал:")
    print("   sf(n) = 1! * 2! * 3! * ... * n!")
    print("   sf(4) = 1! * 2! * 3! * 4! = 288")
    
    print("\n3. Праймориал:")
    print("   p# = произведение всех простых чисел ≤ p")
    print("   7# = 2 * 3 * 5 * 7 = 210")
    
    print("\n4. Гамма-функция:")
    print("   Γ(n) = (n-1)! для целых n")
    print("   Продолжает факториал на вещественные числа")


if __name__ == "__main__":
    demonstrate_factorial()
    performance_analysis()
    practical_applications()
    common_mistakes()
    related_functions()
