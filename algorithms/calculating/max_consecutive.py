"""
🟡 АЛГОРИТМ: Максимальная последовательность одинаковых элементов

Временная сложность: O(n)
Пространственная сложность: O(1)

Применение:
- Поиск максимальной последовательности повторяющихся символов
- Анализ строк и массивов
- Задачи на скользящее окно
"""


def get_next_dif_letter_idx(input_str, cur_letter_idx):
    """
    Находит индекс следующего символа, отличного от текущего.
    
    Args:
        input_str: входная строка
        cur_letter_idx: индекс текущего символа
        
    Returns:
        Индекс первого символа, отличного от текущего
        
    Пример:
        >>> get_next_dif_letter_idx("aaabbb", 0)
        3
        >>> get_next_dif_letter_idx("aaabbb", 3)
        6
    """
    next_letter_idx = cur_letter_idx
    while next_letter_idx < len(input_str) \
    and input_str[next_letter_idx] == input_str[cur_letter_idx]:
        next_letter_idx += 1
    return next_letter_idx


def max_consecutive_elements(input_str):
    """
    🟡 Middle level
    Находит длину максимальной последовательности одинаковых элементов.
    
    Временная сложность: O(n) - один проход по строке
    Пространственная сложность: O(1) - используем только переменные
    
    Args:
        input_str: входная строка
        
    Returns:
        Длина максимальной последовательности одинаковых символов
        
    Примеры:
        >>> max_consecutive_elements("aaabbbcc")
        3
        >>> max_consecutive_elements("a")
        1
        >>> max_consecutive_elements("")
        0
        >>> max_consecutive_elements("aabbbbcccc")
        4
    """
    if not input_str:
        return 0
        
    result, cur_letter_idx = 0, 0
    while cur_letter_idx < len(input_str):
        next_letter_idx = get_next_dif_letter_idx(input_str, cur_letter_idx)
        result = max(result, next_letter_idx - cur_letter_idx)
        cur_letter_idx = next_letter_idx
    return result


# ============================================================================
# РАСШИРЕННЫЕ ВЕРСИИ
# ============================================================================

def max_consecutive_with_char(input_str):
    """
    Возвращает длину и символ максимальной последовательности.
    
    >>> max_consecutive_with_char("aaabbbcc")
    (3, 'a')
    """
    if not input_str:
        return (0, '')
    
    max_len = 0
    max_char = ''
    cur_idx = 0
    
    while cur_idx < len(input_str):
        next_idx = get_next_dif_letter_idx(input_str, cur_idx)
        length = next_idx - cur_idx
        
        if length > max_len:
            max_len = length
            max_char = input_str[cur_idx]
        
        cur_idx = next_idx
    
    return (max_len, max_char)


def all_consecutive_sequences(input_str):
    """
    Возвращает все последовательности с их длинами.
    
    >>> all_consecutive_sequences("aaabbbcc")
    [('a', 3), ('b', 3), ('c', 2)]
    """
    if not input_str:
        return []
    
    sequences = []
    cur_idx = 0
    
    while cur_idx < len(input_str):
        next_idx = get_next_dif_letter_idx(input_str, cur_idx)
        length = next_idx - cur_idx
        sequences.append((input_str[cur_idx], length))
        cur_idx = next_idx
    
    return sequences


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("МАКСИМАЛЬНАЯ ПОСЛЕДОВАТЕЛЬНОСТЬ - Примеры и тесты")
    print("=" * 60)
    
    # Тест 1: Базовые случаи
    test_strings = [
        "aaabbbcc",
        "a",
        "",
        "aabbbbcccc",
        "aaaaaa",
        "abcdefg",
        "aaabbbaaabbbb"
    ]
    
    print("\nТест 1: Максимальная длина последовательности:")
    for s in test_strings:
        result = max_consecutive_elements(s)
        print(f"  '{s}' -> {result}")
    
    # Тест 2: С символом
    print("\nТест 2: Максимальная последовательность с символом:")
    for s in test_strings[:4]:
        if s:
            length, char = max_consecutive_with_char(s)
            print(f"  '{s}' -> длина={length}, символ='{char}'")
    
    # Тест 3: Все последовательности
    print("\nТест 3: Все последовательности:")
    test_str = "aaabbbcc"
    sequences = all_consecutive_sequences(test_str)
    print(f"  '{test_str}' ->")
    for char, length in sequences:
        print(f"    '{char}' * {length}")
    
    # Тест 4: Производительность
    print("\nТест 4: Производительность на большой строке:")
    import time
    
    large_str = "a" * 10000 + "b" * 5000 + "c" * 15000 + "d" * 1000
    start = time.time()
    result = max_consecutive_elements(large_str)
    end = time.time()
    
    print(f"  Длина строки: {len(large_str)}")
    print(f"  Результат: {result}")
    print(f"  Время: {(end - start)*1000:.2f}ms")
    
    print("\n" + "=" * 60)

