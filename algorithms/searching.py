"""
🟡 АЛГОРИТМЫ ПОИСКА - Вопросы и задачи для собеседований

Основные темы:
- Линейный поиск
- Бинарный поиск
- Поиск в глубину (DFS)
- Поиск в ширину (BFS)
"""


# ============================================================================
# ЗАДАЧА 1: Линейный поиск
# ============================================================================

def linear_search(arr, target):
    """
    🟢 Junior level
    Линейный поиск - O(n)
    
    >>> linear_search([1, 3, 5, 7, 9], 5)
    2
    """
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1


# ============================================================================
# ЗАДАЧА 2: Бинарный поиск
# ============================================================================

def binary_search(arr, target):
    """
    🟢 Junior level
    Бинарный поиск (итеративный) - O(log n)
    Требует отсортированный массив
    
    >>> binary_search([1, 3, 5, 7, 9, 11], 7)
    3
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


def binary_search_recursive(arr, target, left=0, right=None):
    """
    🟡 Middle level
    Бинарный поиск (рекурсивный)
    """
    if right is None:
        right = len(arr) - 1
    
    if left > right:
        return -1
    
    mid = (left + right) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)


# ============================================================================
# ЗАДАЧА 3: Поиск первого и последнего вхождения
# ============================================================================

def find_first_occurrence(arr, target):
    """
    🟡 Middle level
    Находит первое вхождение элемента
    """
    left, right = 0, len(arr) - 1
    result = -1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            result = mid
            right = mid - 1  # Ищем в левой части
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result


def find_last_occurrence(arr, target):
    """
    Находит последнее вхождение элемента
    """
    left, right = 0, len(arr) - 1
    result = -1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            result = mid
            left = mid + 1  # Ищем в правой части
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result


# ============================================================================
# ЗАДАЧА 4: Поиск пика в массиве
# ============================================================================

def find_peak_element(arr):
    """
    🟡 Middle level
    Находит пиковый элемент (больше соседей)
    
    >>> find_peak_element([1, 3, 20, 4, 1, 0])
    2  # индекс элемента 20
    """
    left, right = 0, len(arr) - 1
    
    while left < right:
        mid = (left + right) // 2
        
        if arr[mid] < arr[mid + 1]:
            left = mid + 1
        else:
            right = mid
    
    return left


# ============================================================================
# ЗАДАЧА 5: Поиск в ротированном массиве
# ============================================================================

def search_rotated(arr, target):
    """
    🔴 Senior level
    Поиск в отсортированном ротированном массиве
    
    >>> search_rotated([4, 5, 6, 7, 0, 1, 2], 0)
    4
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        
        # Определяем, какая половина отсортирована
        if arr[left] <= arr[mid]:
            # Левая половина отсортирована
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            # Правая половина отсортирована
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1


# ============================================================================
# ЗАДАЧА 6: Поиск в 2D матрице
# ============================================================================

def search_2d_matrix(matrix, target):
    """
    🟡 Middle level
    Поиск в отсортированной 2D матрице
    
    >>> matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    >>> search_2d_matrix(matrix, 3)
    True
    """
    if not matrix or not matrix[0]:
        return False
    
    rows, cols = len(matrix), len(matrix[0])
    left, right = 0, rows * cols - 1
    
    while left <= right:
        mid = (left + right) // 2
        mid_value = matrix[mid // cols][mid % cols]
        
        if mid_value == target:
            return True
        elif mid_value < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return False


# ============================================================================
# ЗАДАЧА 7: DFS (Depth-First Search)
# ============================================================================

def dfs_recursive(graph, start, visited=None):
    """
    🟡 Middle level
    Поиск в глубину (рекурсивный)
    
    >>> graph = {'A': ['B', 'C'], 'B': ['D', 'E'], 'C': ['F'], 'D': [], 'E': [], 'F': []}
    >>> dfs_recursive(graph, 'A')
    ['A', 'B', 'D', 'E', 'C', 'F']
    """
    if visited is None:
        visited = set()
    
    visited.add(start)
    result = [start]
    
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            result.extend(dfs_recursive(graph, neighbor, visited))
    
    return result


def dfs_iterative(graph, start):
    """
    Поиск в глубину (итеративный)
    """
    visited = set()
    stack = [start]
    result = []
    
    while stack:
        vertex = stack.pop()
        
        if vertex not in visited:
            visited.add(vertex)
            result.append(vertex)
            
            # Добавляем соседей в обратном порядке
            for neighbor in reversed(graph.get(vertex, [])):
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return result


# ============================================================================
# ЗАДАЧА 8: BFS (Breadth-First Search)
# ============================================================================

def bfs(graph, start):
    """
    🟡 Middle level
    Поиск в ширину
    
    >>> graph = {'A': ['B', 'C'], 'B': ['D', 'E'], 'C': ['F'], 'D': [], 'E': [], 'F': []}
    >>> bfs(graph, 'A')
    ['A', 'B', 'C', 'D', 'E', 'F']
    """
    from collections import deque
    
    visited = set()
    queue = deque([start])
    visited.add(start)
    result = []
    
    while queue:
        vertex = queue.popleft()
        result.append(vertex)
        
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return result


# ============================================================================
# ЗАДАЧА 9: Кратчайший путь (BFS)
# ============================================================================

def shortest_path(graph, start, end):
    """
    🟡 Middle level
    Находит кратчайший путь между двумя узлами
    """
    from collections import deque
    
    if start == end:
        return [start]
    
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        vertex, path = queue.popleft()
        
        for neighbor in graph.get(vertex, []):
            if neighbor == end:
                return path + [neighbor]
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None  # Путь не найден


# ============================================================================
# ЗАДАЧА 10: Поиск подстроки (Naive)
# ============================================================================

def find_substring(text, pattern):
    """
    🟢 Junior level
    Наивный поиск подстроки - O(n*m)
    
    >>> find_substring("hello world", "wor")
    6
    """
    n, m = len(text), len(pattern)
    
    for i in range(n - m + 1):
        if text[i:i+m] == pattern:
            return i
    
    return -1


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("АЛГОРИТМЫ ПОИСКА - Примеры и тесты")
    print("=" * 60)
    
    # Тест 1: Линейный и бинарный поиск
    arr = [1, 3, 5, 7, 9, 11, 13]
    print(f"\nМассив: {arr}")
    print(f"Линейный поиск (7): {linear_search(arr, 7)}")
    print(f"Бинарный поиск (7): {binary_search(arr, 7)}")
    
    # Тест 2: Первое и последнее вхождение
    arr_dup = [1, 2, 2, 2, 3, 4, 5]
    print(f"\nМассив с дубликатами: {arr_dup}")
    print(f"Первое вхождение (2): {find_first_occurrence(arr_dup, 2)}")
    print(f"Последнее вхождение (2): {find_last_occurrence(arr_dup, 2)}")
    
    # Тест 3: Пик
    arr_peak = [1, 3, 20, 4, 1, 0]
    print(f"\nМассив: {arr_peak}")
    peak_idx = find_peak_element(arr_peak)
    print(f"Пиковый элемент: индекс {peak_idx}, значение {arr_peak[peak_idx]}")
    
    # Тест 4: Ротированный массив
    rotated = [4, 5, 6, 7, 0, 1, 2]
    print(f"\nРотированный массив: {rotated}")
    print(f"Поиск 0: индекс {search_rotated(rotated, 0)}")
    
    # Тест 5: DFS и BFS
    graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': [],
        'F': []
    }
    
    print(f"\nГраф: {graph}")
    print(f"DFS от A: {dfs_recursive(graph, 'A')}")
    print(f"BFS от A: {bfs(graph, 'A')}")
    
    # Тест 6: Кратчайший путь
    graph2 = {
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['D', 'E'],
        'D': ['E'],
        'E': []
    }
    
    print(f"\nГраф: {graph2}")
    print(f"Кратчайший путь A -> E: {shortest_path(graph2, 'A', 'E')}")
    
    print("\n" + "=" * 60)

