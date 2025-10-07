import timeit

"""
Классические задачи динамического программирования
Содержит популярные алгоритмы DP с подробными объяснениями
"""


# ============================================================================
# 1. ЧИСЛА ФИБОНАЧЧИ
# ============================================================================

def fibonacci_naive(n):
    """
    Наивная рекурсивная реализация чисел Фибоначчи.
    
    Time Complexity: O(2^n) - экспоненциальная!
    Space Complexity: O(n) - глубина рекурсии
    """
    if n <= 1:
        return n
    return fibonacci_naive(n-1) + fibonacci_naive(n-2)


def fibonacci_memo(n, memo=None):
    """
    Рекурсивная реализация с мемоизацией.
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fibonacci_memo(n-1, memo) + fibonacci_memo(n-2, memo)
    return memo[n]


def fibonacci_dp(n):
    """
    Итеративная реализация с динамическим программированием.
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]


def fibonacci_optimized(n):
    """
    Оптимизированная версия с O(1) памяти.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    if n <= 1:
        return n
    
    prev2, prev1 = 0, 1
    
    for i in range(2, n + 1):
        print(prev2, prev1)
        current = prev1 + prev2
        prev2, prev1 = prev1, current
    
    return prev1


# ============================================================================
# 2. ЗАДАЧА О РЮКЗАКЕ (0/1 KNAPSACK)
# ============================================================================

def knapsack_01(weights, values, capacity):
    """
    Задача о рюкзаке 0/1.
    
    Args:
        weights (list): Веса предметов
        values (list): Стоимости предметов
        capacity (int): Вместимость рюкзака
    
    Returns:
        int: Максимальная стоимость
    
    Time Complexity: O(n * capacity)
    Space Complexity: O(n * capacity)
    """
    n = len(weights)
    
    # dp[i][w] = максимальная стоимость с первыми i предметами и весом w
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            # Не берем i-й предмет
            dp[i][w] = dp[i-1][w]
            
            # Берем i-й предмет (если помещается)
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], 
                             dp[i-1][w - weights[i-1]] + values[i-1])
    
    return dp[n][capacity]


def knapsack_01_optimized(weights, values, capacity):
    """
    Оптимизированная версия с O(capacity) памяти.
    
    Time Complexity: O(n * capacity)
    Space Complexity: O(capacity)
    """
    n = len(weights)
    dp = [0] * (capacity + 1)
    
    for i in range(n):
        # Идем справа налево, чтобы не перезаписать нужные значения
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    
    return dp[capacity]


def knapsack_items(weights, values, capacity):
    """
    Возвращает не только максимальную стоимость, но и выбранные предметы.
    
    Returns:
        tuple: (максимальная стоимость, список индексов выбранных предметов)
    """
    n = len(weights)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    # Заполняем таблицу
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            dp[i][w] = dp[i-1][w]
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], 
                             dp[i-1][w - weights[i-1]] + values[i-1])
    
    # Восстанавливаем решение
    selected_items = []
    w = capacity
    
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected_items.append(i-1)
            w -= weights[i-1]
    
    return dp[n][capacity], selected_items[::-1]


# ============================================================================
# 3. НАИБОЛЬШАЯ ОБЩАЯ ПОДПОСЛЕДОВАТЕЛЬНОСТЬ (LCS)
# ============================================================================

def lcs_length(s1, s2):
    """
    Находит длину наибольшей общей подпоследовательности.
    
    Args:
        s1 (str): Первая строка
        s2 (str): Вторая строка
    
    Returns:
        int: Длина LCS
    
    Time Complexity: O(m * n)
    Space Complexity: O(m * n)
    """
    m, n = len(s1), len(s2)
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]


def lcs_string(s1, s2):
    """
    Находит саму наибольшую общую подпоследовательность.
    
    Returns:
        str: LCS строка
    """
    m, n = len(s1), len(s2)
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    # Заполняем таблицу
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    # Восстанавливаем строку
    result = []
    i, j = m, n
    
    while i > 0 and j > 0:
        if s1[i-1] == s2[j-1]:
            result.append(s1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    
    return ''.join(reversed(result))


# ============================================================================
# 4. РАЗМЕН МОНЕТ
# ============================================================================

def coin_change_min_coins(coins, amount):
    """
    Минимальное количество монет для размена суммы.
    
    Args:
        coins (list): Доступные номиналы монет
        amount (int): Сумма для размена
    
    Returns:
        int: Минимальное количество монет (-1 если невозможно)
    
    Time Complexity: O(amount * len(coins))
    Space Complexity: O(amount)
    """
    # dp[i] = минимальное количество монет для суммы i
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # Для суммы 0 нужно 0 монет
    
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1


def coin_change_ways(coins, amount):
    """
    Количество способов размена суммы.
    
    Returns:
        int: Количество способов размена
    """
    # dp[i] = количество способов размена суммы i
    dp = [0] * (amount + 1)
    dp[0] = 1  # Один способ разменять 0 - не брать монеты
    
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]
    
    return dp[amount]


# ============================================================================
# 5. НАИБОЛЬШАЯ ВОЗРАСТАЮЩАЯ ПОДПОСЛЕДОВАТЕЛЬНОСТЬ (LIS)
# ============================================================================

def lis_length(arr):
    """
    Длина наибольшей возрастающей подпоследовательности.
    
    Args:
        arr (list): Исходный массив
    
    Returns:
        int: Длина LIS
    
    Time Complexity: O(n^2)
    Space Complexity: O(n)
    """
    n = len(arr)
    # dp[i] = длина LIS, заканчивающейся в позиции i
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)


def lis_sequence(arr):
    """
    Находит саму наибольшую возрастающую подпоследовательность.
    
    Returns:
        list: LIS последовательность
    """
    n = len(arr)
    dp = [1] * n
    parent = [-1] * n  # Для восстановления последовательности
    
    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                parent[i] = j
    
    # Находим конец LIS
    max_len = max(dp)
    end_index = dp.index(max_len)
    
    # Восстанавливаем последовательность
    result = []
    while end_index != -1:
        result.append(arr[end_index])
        end_index = parent[end_index]
    
    return result[::-1]


def lis_optimized(arr):
    """
    Оптимизированная версия с O(n log n).
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    import bisect
    
    # tail[i] = наименьший элемент, на который заканчивается LIS длины i+1
    tail = []
    
    for num in arr:
        # Ищем позицию для вставки
        pos = bisect.bisect_left(tail, num)
        
        if pos == len(tail):
            tail.append(num)
        else:
            tail[pos] = num
    
    return len(tail)


# ============================================================================
# 6. РЕДАКЦИОННОЕ РАССТОЯНИЕ (EDIT DISTANCE)
# ============================================================================

def edit_distance(s1, s2):
    """
    Редакционное расстояние (расстояние Левенштейна).
    
    Args:
        s1 (str): Первая строка
        s2 (str): Вторая строка
    
    Returns:
        int: Минимальное количество операций для преобразования s1 в s2
    
    Операции: вставка, удаление, замена
    
    Time Complexity: O(m * n)
    Space Complexity: O(m * n)
    """
    m, n = len(s1), len(s2)
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    # Базовые случаи
    for i in range(m + 1):
        dp[i][0] = i  # Удалить все символы из s1
    for j in range(n + 1):
        dp[0][j] = j  # Вставить все символы в s1
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                # Символы одинаковые, операций не нужно
                dp[i][j] = dp[i-1][j-1]
            else:
                # Минимум из трех операций
                dp[i][j] = 1 + min(
                    dp[i-1][j],    # Удаление
                    dp[i][j-1],    # Вставка
                    dp[i-1][j-1]   # Замена
                )
    
    return dp[m][n]


def test_fibonacci_naive():
    """Тестирование наивной реализации Фибоначчи"""
    import time

    print("=== ЧИСЛА ФИБОНАЧЧИ (наивная) ===")
    n = 10
    start = time.time()
    print(f"F({n}) = {fibonacci_naive(n)}")
    time1 = time.time() - start
    print(f"Время: {time1:.6f}с")

# ============================================================================
# ТЕСТИРОВАНИЕ И ДЕМОНСТРАЦИЯ
# ============================================================================

def test_fibonacci():
    """Тестирование алгоритмов Фибоначчи"""
    print("=== ЧИСЛА ФИБОНАЧЧИ ===")
    
    n = 10
    print(f"F({n}) = {fibonacci_dp(n)}")
    print(f"Оптимизированная версия: {fibonacci_optimized(n)}")
    print(f"С мемоизацией: {fibonacci_memo(n)}")
    
    # Сравнение производительности
    import time
    
    n = 10
    start = time.time()
    result1 = fibonacci_dp(n)
    time1 = time.time() - start
    
    start = time.time()
    result2 = fibonacci_optimized(n)
    time2 = time.time() - start
    
    print(f"\nF({n}) = {result1}")
    print(f"DP время: {time1:.6f}с")
    print(f"Оптимизированная время: {time2:.6f}с")
    print()


def test_knapsack():
    """Тестирование задачи о рюкзаке"""
    print("=== ЗАДАЧА О РЮКЗАКЕ ===")
    
    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    capacity = 7
    
    max_value = knapsack_01(weights, values, capacity)
    max_value_opt = knapsack_01_optimized(weights, values, capacity)
    max_value_items, selected = knapsack_items(weights, values, capacity)
    
    print(f"Веса: {weights}")
    print(f"Стоимости: {values}")
    print(f"Вместимость: {capacity}")
    print(f"Максимальная стоимость: {max_value}")
    print(f"Оптимизированная версия: {max_value_opt}")
    print(f"Выбранные предметы (индексы): {selected}")
    print(f"Выбранные веса: {[weights[i] for i in selected]}")
    print(f"Выбранные стоимости: {[values[i] for i in selected]}")
    print()


def test_lcs():
    """Тестирование LCS"""
    print("=== НАИБОЛЬШАЯ ОБЩАЯ ПОДПОСЛЕДОВАТЕЛЬНОСТЬ ===")
    
    s1 = "ABCDGH"
    s2 = "AEDFHR"
    
    length = lcs_length(s1, s2)
    sequence = lcs_string(s1, s2)
    
    print(f"Строка 1: {s1}")
    print(f"Строка 2: {s2}")
    print(f"Длина LCS: {length}")
    print(f"LCS: {sequence}")
    print()


def test_coin_change():
    """Тестирование размена монет"""
    print("=== РАЗМЕН МОНЕТ ===")
    
    coins = [1, 3, 4]
    amount = 6
    
    min_coins = coin_change_min_coins(coins, amount)
    ways = coin_change_ways(coins, amount)
    
    print(f"Монеты: {coins}")
    print(f"Сумма: {amount}")
    print(f"Минимальное количество монет: {min_coins}")
    print(f"Количество способов размена: {ways}")
    print()


def test_lis():
    """Тестирование LIS"""
    print("=== НАИБОЛЬШАЯ ВОЗРАСТАЮЩАЯ ПОДПОСЛЕДОВАТЕЛЬНОСТЬ ===")
    
    arr = [10, 9, 2, 5, 3, 7, 101, 18]
    
    length = lis_length(arr)
    sequence = lis_sequence(arr)
    length_opt = lis_optimized(arr)
    
    print(f"Массив: {arr}")
    print(f"Длина LIS: {length}")
    print(f"LIS: {sequence}")
    print(f"Оптимизированная длина: {length_opt}")
    print()


def test_edit_distance():
    """Тестирование редакционного расстояния"""
    print("=== РЕДАКЦИОННОЕ РАССТОЯНИЕ ===")
    
    s1 = "kitten"
    s2 = "sitting"
    
    distance = edit_distance(s1, s2)
    
    print(f"Строка 1: {s1}")
    print(f"Строка 2: {s2}")
    print(f"Редакционное расстояние: {distance}")
    print()


if __name__ == "__main__":
    print("=== КЛАССИЧЕСКИЕ ЗАДАЧИ ДИНАМИЧЕСКОГО ПРОГРАММИРОВАНИЯ ===")
    print()

    fibonacci_optimized(10)
    # test_fibonacci_naive()
    # test_fibonacci()
    # test_knapsack()
    # test_lcs()
    # test_coin_change()
    # test_lis()
    # test_edit_distance()
    
    print("=== СРАВНЕНИЕ СЛОЖНОСТИ ===")
    print("""
    Задача                    | Время        | Память
    --------------------------|--------------|--------
    Фибоначчи (наивная)       | O(2^n)       | O(n)
    Фибоначчи (DP)            | O(n)         | O(n)
    Фибоначчи (оптимизированная)| O(n)       | O(1)
    Рюкзак 0/1                | O(n*W)       | O(n*W)
    Рюкзак 0/1 (оптимизированная)| O(n*W)    | O(W)
    LCS                       | O(m*n)       | O(m*n)
    Размен монет              | O(amount*n)  | O(amount)
    LIS (наивная)             | O(n^2)       | O(n)
    LIS (оптимизированная)    | O(n log n)   | O(n)
    Редакционное расстояние   | O(m*n)       | O(m*n)
    """)
