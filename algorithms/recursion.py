"""
🟡 РЕКУРСИЯ - Вопросы и задачи для собеседований

Основные темы:
- Базовая рекурсия
- Хвостовая рекурсия
- Рекурсия vs итерация
- Backtracking
- Динамическое программирование
"""


# ============================================================================
# ТЕОРЕТИЧЕСКИЕ ВОПРОСЫ
# ============================================================================

"""
Q1: Что такое рекурсия?
A: Функция, которая вызывает сама себя

Q2: Что такое базовый случай (base case)?
A: Условие выхода из рекурсии, предотвращает бесконечную рекурсию

Q3: В чем разница между рекурсией и итерацией?
A:
- Рекурсия: более читаема, использует стек вызовов
- Итерация: более эффективна по памяти

Q4: Что такое хвостовая рекурсия?
A: Когда рекурсивный вызов - последняя операция функции
Python не оптимизирует хвостовую рекурсию!

Q5: Что такое мемоизация?
A: Кеширование результатов для избежания повторных вычислений
"""


# ============================================================================
# ЗАДАЧА 1: Факториал
# ============================================================================

def factorial(n):
    """
    🟢 Junior level
    Факториал числа
    
    >>> factorial(5)
    120
    """
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def factorial_iterative(n):
    """Итеративная версия"""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


# ============================================================================
# ЗАДАЧА 2: Числа Фибоначчи
# ============================================================================

def fibonacci(n):
    """
    🟢 Junior level
    n-ное число Фибоначчи (неоптимизированная версия)
    
    >>> fibonacci(6)
    8
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_memoized(n, memo=None):
    """
    🟡 Middle level
    С мемоизацией - O(n)
    """
    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fibonacci_memoized(n - 1, memo) + fibonacci_memoized(n - 2, memo)
    return memo[n]


# ============================================================================
# ЗАДАЧА 3: Сумма цифр числа
# ============================================================================

def sum_of_digits(n):
    """
    🟢 Junior level
    Сумма цифр числа
    
    >>> sum_of_digits(1234)
    10
    """
    if n == 0:
        return 0
    return n % 10 + sum_of_digits(n // 10)


# ============================================================================
# ЗАДАЧА 4: Переворот строки
# ============================================================================

def reverse_string(s):
    """
    🟢 Junior level
    Переворот строки рекурсивно
    
    >>> reverse_string("hello")
    'olleh'
    """
    if len(s) <= 1:
        return s
    return s[-1] + reverse_string(s[:-1])


# ============================================================================
# ЗАДАЧА 5: Проверка палиндрома
# ============================================================================

def is_palindrome(s):
    """
    🟢 Junior level
    Проверка палиндрома
    
    >>> is_palindrome("racecar")
    True
    """
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_palindrome(s[1:-1])


# ============================================================================
# ЗАДАЧА 6: Степень числа
# ============================================================================

def power(base, exp):
    """
    🟡 Middle level
    Возведение в степень - O(log n)
    
    >>> power(2, 10)
    1024
    """
    if exp == 0:
        return 1
    if exp == 1:
        return base
    
    # Оптимизация: используем деление экспоненты пополам
    if exp % 2 == 0:
        half = power(base, exp // 2)
        return half * half
    else:
        return base * power(base, exp - 1)


# ============================================================================
# ЗАДАЧА 7: Наибольший общий делитель (GCD)
# ============================================================================

def gcd(a, b):
    """
    🟡 Middle level
    Алгоритм Евклида
    
    >>> gcd(48, 18)
    6
    """
    if b == 0:
        return a
    return gcd(b, a % b)


# ============================================================================
# ЗАДАЧА 8: Ханойская башня
# ============================================================================

def hanoi(n, source='A', target='C', auxiliary='B'):
    """
    🟡 Middle level
    Ханойская башня
    """
    if n == 1:
        print(f"Переместить диск 1 с {source} на {target}")
        return
    
    hanoi(n - 1, source, auxiliary, target)
    print(f"Переместить диск {n} с {source} на {target}")
    hanoi(n - 1, auxiliary, target, source)


# ============================================================================
# ЗАДАЧА 9: Все подмножества
# ============================================================================

def subsets(arr):
    """
    🔴 Senior level
    Генерирует все подмножества
    
    >>> subsets([1, 2, 3])
    [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
    """
    if not arr:
        return [[]]
    
    # Рекурсивно получаем подмножества без первого элемента
    rest_subsets = subsets(arr[1:])
    
    # Добавляем первый элемент к каждому подмножеству
    with_first = [[arr[0]] + subset for subset in rest_subsets]
    
    return rest_subsets + with_first


# ============================================================================
# ЗАДАЧА 10: Генерация скобочных последовательностей
# ============================================================================

def generate_parentheses(n):
    """
    🔴 Senior level
    Генерирует все правильные скобочные последовательности
    
    >>> generate_parentheses(3)
    ['((()))', '(()())', '(())()', '()(())', '()()()']
    """
    result = []
    
    def backtrack(current, open_count, close_count):
        if len(current) == 2 * n:
            result.append(current)
            return
        
        if open_count < n:
            backtrack(current + '(', open_count + 1, close_count)
        
        if close_count < open_count:
            backtrack(current + ')', open_count, close_count + 1)
    
    backtrack('', 0, 0)
    return result


# ============================================================================
# ЗАДАЧА 11: Перестановки
# ============================================================================

def permutations(arr):
    """
    🔴 Senior level
    Генерирует все перестановки
    
    >>> permutations([1, 2, 3])
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    """
    if len(arr) <= 1:
        return [arr]
    
    result = []
    for i, elem in enumerate(arr):
        rest = arr[:i] + arr[i+1:]
        for perm in permutations(rest):
            result.append([elem] + perm)
    
    return result


# ============================================================================
# ЗАДАЧА 12: N Queens (N ферзей)
# ============================================================================

def solve_n_queens(n):
    """
    🔴 Senior level
    Задача о N ферзях на шахматной доске
    """
    def is_safe(board, row, col):
        # Проверка столбца
        for i in range(row):
            if board[i] == col:
                return False
        
        # Проверка диагоналей
        for i in range(row):
            if abs(board[i] - col) == abs(i - row):
                return False
        
        return True
    
    def solve(row, board):
        if row == n:
            result.append(board[:])
            return
        
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                solve(row + 1, board)
                board[row] = -1
    
    result = []
    solve(0, [-1] * n)
    return result


def print_board(board):
    """Печатает доску с ферзями"""
    n = len(board)
    for row in range(n):
        line = ['.' * n]
        if board[row] != -1:
            line = ['.'] * n
            line[board[row]] = 'Q'
        print(' '.join(line))
    print()


# ============================================================================
# ЗАДАЧА 13: Разбиение числа
# ============================================================================

def partition_number(n):
    """
    🔴 Senior level
    Все способы разбиения числа на сумму положительных чисел
    
    >>> partition_number(4)
    [[4], [3, 1], [2, 2], [2, 1, 1], [1, 1, 1, 1]]
    """
    def helper(n, max_val):
        if n == 0:
            return [[]]
        
        result = []
        for i in range(min(n, max_val), 0, -1):
            for partition in helper(n - i, i):
                result.append([i] + partition)
        
        return result
    
    return helper(n, n)


# ============================================================================
# ЗАДАЧА 14: Генерация IP адресов
# ============================================================================

def restore_ip_addresses(s):
    """
    🔴 Senior level
    Генерирует все возможные IP адреса из строки
    
    >>> restore_ip_addresses("25525511135")
    ['255.255.11.135', '255.255.111.35']
    """
    def is_valid(segment):
        if not segment or len(segment) > 3:
            return False
        if segment[0] == '0' and len(segment) > 1:
            return False
        return 0 <= int(segment) <= 255
    
    def backtrack(start, parts):
        if len(parts) == 4:
            if start == len(s):
                result.append('.'.join(parts))
            return
        
        for length in range(1, 4):
            if start + length > len(s):
                break
            
            segment = s[start:start + length]
            if is_valid(segment):
                backtrack(start + length, parts + [segment])
    
    result = []
    backtrack(0, [])
    return result


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("РЕКУРСИЯ - Примеры и тесты")
    print("=" * 60)
    
    # Тест 1: Факториал
    print("\n1. Факториал:")
    print(f"factorial(5) = {factorial(5)}")
    print(f"factorial_iterative(5) = {factorial_iterative(5)}")
    
    # Тест 2: Фибоначчи
    print("\n2. Фибоначчи:")
    print(f"fibonacci(10) = {fibonacci(10)}")
    print(f"fibonacci_memoized(10) = {fibonacci_memoized(10)}")
    
    # Тест 3: Сумма цифр
    print("\n3. Сумма цифр:")
    print(f"sum_of_digits(1234) = {sum_of_digits(1234)}")
    
    # Тест 4: Переворот строки
    print("\n4. Переворот строки:")
    print(f"reverse_string('hello') = {reverse_string('hello')}")
    
    # Тест 5: Палиндром
    print("\n5. Проверка палиндрома:")
    print(f"is_palindrome('racecar') = {is_palindrome('racecar')}")
    print(f"is_palindrome('hello') = {is_palindrome('hello')}")
    
    # Тест 6: Степень
    print("\n6. Степень:")
    print(f"power(2, 10) = {power(2, 10)}")
    
    # Тест 7: GCD
    print("\n7. Наибольший общий делитель:")
    print(f"gcd(48, 18) = {gcd(48, 18)}")
    
    # Тест 8: Ханойская башня
    print("\n8. Ханойская башня (3 диска):")
    hanoi(3)
    
    # Тест 9: Подмножества
    print("\n9. Все подмножества [1, 2, 3]:")
    print(subsets([1, 2, 3]))
    
    # Тест 10: Скобочные последовательности
    print("\n10. Скобочные последовательности (n=3):")
    print(generate_parentheses(3))
    
    # Тест 11: Перестановки
    print("\n11. Перестановки [1, 2, 3]:")
    print(permutations([1, 2, 3]))
    
    # Тест 12: N Queens
    print("\n12. 4 Ферзя (первое решение):")
    solutions = solve_n_queens(4)
    if solutions:
        print_board(solutions[0])
    print(f"Всего решений: {len(solutions)}")
    
    print("\n" + "=" * 60)

