"""
Алгоритм генерации валидных скобочных последовательностей.

Этот модуль содержит алгоритмы для генерации всех возможных валидных 
скобочных последовательностей для заданного количества пар скобок.
"""

from typing import List
import time
from functools import lru_cache


def generate_basic(n: int) -> List[str]:
    """
    Генерирует все валидные скобочные последовательности для n пар скобок.
    Базовый алгоритм с использованием backtracking.
    
    Args:
        n (int): Количество пар скобок.
    
    Returns:
        List[str]: Список всех валидных последовательностей.
    
    Временная сложность: O(4^n / sqrt(n)) - каталанские числа
    Пространственная сложность: O(4^n / sqrt(n))
    
    Примеры:
        >>> generate_basic(1)
        ['()']
        >>> generate_basic(2)
        ['(())', '()()']
        >>> generate_basic(3)
        ['((()))', '(()())', '(())()', '()(())', '()()()']
    """
    if n <= 0:
        return [""]
    
    result = []
    
    def backtrack(s: List[str], open_count: int, close_count: int):
        """
        Рекурсивная функция для генерации скобочных последовательностей.
        
        Args:
            s: Текущая строящаяся последовательность
            open_count: Количество открывающих скобок
            close_count: Количество закрывающих скобок
        """
        # Базовый случай: длина последовательности равна 2*n
        if len(s) == 2 * n:
            result.append("".join(s))
            return
        
        # Добавляем открывающую скобку, если их меньше n
        if open_count < n:
            s.append('(')
            backtrack(s, open_count + 1, close_count)
            s.pop()  # Backtrack
        
        # Добавляем закрывающую скобку, если их меньше открытых
        if close_count < open_count:
            s.append(')')
            backtrack(s, open_count, close_count + 1)
            s.pop()  # Backtrack
    
    backtrack([], 0, 0)
    return result


def generate_optimized(n: int) -> List[str]:
    """
    Оптимизированная версия генерации скобочных последовательностей.
    Использует меньше операций со списками и более эффективную рекурсию.
    
    Args:
        n (int): Количество пар скобок.
    
    Returns:
        List[str]: Список всех валидных последовательностей.
    
    Временная сложность: O(4^n / sqrt(n)) - каталанские числа
    Пространственная сложность: O(4^n / sqrt(n))
    """
    if n <= 0:
        return [""]
    
    result = []
    
    def backtrack(current: str, open_count: int, close_count: int):
        """
        Оптимизированная рекурсивная функция.
        Использует строку вместо списка для лучшей производительности.
        """
        # Базовый случай
        if len(current) == 2 * n:
            result.append(current)
            return
        
        # Добавляем открывающую скобку
        if open_count < n:
            backtrack(current + '(', open_count + 1, close_count)
        
        # Добавляем закрывающую скобку
        if close_count < open_count:
            backtrack(current + ')', open_count, close_count + 1)
    
    backtrack("", 0, 0)
    return result


def generate_iterative(n: int) -> List[str]:
    """
    Итеративная версия генерации скобочных последовательностей.
    Избегает рекурсии и использует стек для отслеживания состояния.
    
    Args:
        n (int): Количество пар скобок.
    
    Returns:
        List[str]: Список всех валидных последовательностей.
    
    Временная сложность: O(4^n / sqrt(n))
    Пространственная сложность: O(4^n / sqrt(n))
    """
    if n <= 0:
        return [""]
    
    result = []
    # Стек содержит кортежи: (current_string, open_count, close_count)
    stack = [("", 0, 0)]
    
    while stack:
        current, open_count, close_count = stack.pop()
        
        # Если достигли нужной длины, добавляем в результат
        if len(current) == 2 * n:
            result.append(current)
            continue
        
        # Добавляем закрывающую скобку (если возможно)
        if close_count < open_count:
            stack.append((current + ')', open_count, close_count + 1))
        
        # Добавляем открывающую скобку (если возможно)
        if open_count < n:
            stack.append((current + '(', open_count + 1, close_count))
    
    return result


@lru_cache(maxsize=None)
def catalan_number(n: int) -> int:
    """
    Вычисляет n-е каталанское число.
    Каталанские числа определяют количество валидных скобочных последовательностей.
    
    Args:
        n (int): Порядковый номер каталанского числа.
    
    Returns:
        int: n-е каталанское число.
    """
    if n <= 1:
        return 1
    
    result = 0
    for i in range(n):
        result += catalan_number(i) * catalan_number(n - 1 - i)
    
    return result


def count_sequences(n: int) -> int:
    """
    Быстрое вычисление количества валидных скобочных последовательностей
    без их генерации.
    
    Args:
        n (int): Количество пар скобок.
    
    Returns:
        int: Количество валидных последовательностей.
    """
    return catalan_number(n)


def benchmark_algorithms(n: int, iterations: int = 1) -> dict:
    """
    Сравнивает производительность разных алгоритмов.
    
    Args:
        n (int): Количество пар скобок для тестирования.
        iterations (int): Количество итераций для усреднения времени.
    
    Returns:
        dict: Словарь с результатами бенчмарков.
    """
    algorithms = {
        'basic': generate_basic,
        'optimized': generate_optimized,
        'iterative': generate_iterative
    }
    
    results = {}
    
    for name, algorithm in algorithms.items():
        times = []
        for _ in range(iterations):
            start_time = time.time()
            sequences = algorithm(n)
            end_time = time.time()
            times.append(end_time - start_time)
        
        results[name] = {
            'avg_time': sum(times) / len(times),
            'count': len(sequences),
            'expected_count': count_sequences(n)
        }
    
    return results


def explain_algorithm(n: int = 3) -> None:
    """
    Подробное объяснение работы алгоритма с примерами.
    
    Args:
        n (int): Количество пар скобок для демонстрации.
    """
    print("=" * 60)
    print("ОБЪЯСНЕНИЕ АЛГОРИТМА ГЕНЕРАЦИИ СКОБОЧНЫХ ПОСЛЕДОВАТЕЛЬНОСТЕЙ")
    print("=" * 60)
    
    print(f"\n1. ЦЕЛЬ: Генерируем все валидные скобочные последовательности для {n} пар скобок")
    print(f"   Ожидаемое количество: {count_sequences(n)} (n-е каталанское число)")
    
    print("\n2. ПРАВИЛА ВАЛИДНОСТИ:")
    print("   - Количество открывающих скобок = количество закрывающих = n")
    print("   - В любой позиции количество открывающих >= количества закрывающих")
    print("   - Общая длина последовательности = 2*n")
    
    print("\n3. АЛГОРИТМ (Backtracking):")
    print("   - Начинаем с пустой строки")
    print("   - На каждом шаге можем добавить '(' или ')' (если это валидно)")
    print("   - Если достигаем длины 2*n, сохраняем результат")
    print("   - Откатываемся назад (backtrack) для поиска других вариантов")
    
    print(f"\n4. ДЕМОНСТРАЦИЯ ДЛЯ n={n}:")
    sequences = generate_basic(n)
    for i, seq in enumerate(sequences, 1):
        print(f"   {i}. {seq}")
    
    print("\n5. ВРЕМЕННАЯ СЛОЖНОСТЬ:")
    print("   - O(4^n / sqrt(n)) - каталанские числа")
    print("   - Для n=1: 1 последовательность")
    print("   - Для n=2: 2 последовательности") 
    print("   - Для n=3: 5 последовательностей")
    print("   - Для n=4: 14 последовательностей")
    print("   - Рост экспоненциальный, но медленнее чем 2^(2n)")
    
    print("\n6. ПРОСТРАНСТВЕННАЯ СЛОЖНОСТЬ:")
    print("   - O(4^n / sqrt(n)) для хранения всех результатов")
    print("   - O(n) для стека рекурсии")


if __name__ == "__main__":
    # Демонстрация работы алгоритмов
    print("ГЕНЕРАЦИЯ СКОБОЧНЫХ ПОСЛЕДОВАТЕЛЬНОСТЕЙ")
    print("=" * 50)
    
    # Тестируем для разных значений n
    for n in range(1, 5):
        print(f"\nn = {n}:")
        sequences = generate_basic(n)
        print(f"Количество последовательностей: {len(sequences)}")
        print(f"Последовательности: {sequences}")
    
    # Бенчмарк для n=4
    print(f"\nБЕНЧМАРК АЛГОРИТМОВ (n=4):")
    benchmark_results = benchmark_algorithms(4, 3)
    for algo_name, result in benchmark_results.items():
        print(f"{algo_name:>10}: {result['avg_time']:.6f}s, "
              f"count={result['count']}, expected={result['expected_count']}")
    
    # Подробное объяснение
    explain_algorithm(3)
