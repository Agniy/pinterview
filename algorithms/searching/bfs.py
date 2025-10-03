"""
🟡 BFS (BREADTH-FIRST SEARCH) - Поиск в ширину

Временная сложность:
- O(V + E) где V - количество вершин, E - количество рёбер

Пространственная сложность:
- O(V) - размер очереди в худшем случае

Особенности:
- Использует очередь (FIFO)
- Идет по уровням, сначала все соседи, потом соседи соседей
- Гарантирует нахождение кратчайшего пути (для невзвешенных графов)
- Подходит для поиска кратчайших путей, уровней
"""

from collections import deque


def bfs(graph, start):
    """
    🟡 Middle level
    Поиск в ширину
    
    Принцип работы:
    1. Добавляем начальную вершину в очередь
    2. Пока очередь не пуста:
       - Извлекаем вершину из начала очереди
       - Помечаем как посещенную
       - Добавляем всех непосещенных соседей в конец очереди
    
    Args:
        graph: граф в виде словаря {вершина: [соседи]}
        start: начальная вершина
        
    Returns:
        список вершин в порядке обхода BFS
        
    >>> graph = {'A': ['B', 'C'], 'B': ['D', 'E'], 'C': ['F'], 'D': [], 'E': [], 'F': []}
    >>> bfs(graph, 'A')
    ['A', 'B', 'C', 'D', 'E', 'F']
    """
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
# ПОШАГОВОЕ ИСПОЛНЕНИЕ
# ============================================================================

def bfs_with_steps(graph, start):
    """
    Версия с выводом пошагового исполнения
    """
    print(f"BFS от вершины: {start}")
    print("=" * 50)
    
    visited = set()
    queue = deque([start])
    visited.add(start)
    result = []
    step = 0
    
    while queue:
        step += 1
        vertex = queue.popleft()
        result.append(vertex)
        
        print(f"Шаг {step}:")
        print(f"  Извлекаем из очереди: {vertex}")
        print(f"  Текущая очередь: {list(queue)}")
        print(f"  Посещенные: {visited}")
        print(f"  Результат: {result}")
        
        neighbors = graph.get(vertex, [])
        print(f"  Соседи {vertex}: {neighbors}")
        
        new_neighbors = []
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                new_neighbors.append(neighbor)
        
        if new_neighbors:
            print(f"  Добавляем в очередь: {new_neighbors}")
        
        print(f"  Новая очередь: {list(queue)}")
        print()
    
    print(f"Итоговый результат BFS: {result}")
    return result


# ============================================================================
# КРАТЧАЙШИЙ ПУТЬ
# ============================================================================

def shortest_path(graph, start, end):
    """
    Находит кратчайший путь между двумя вершинами
    
    >>> graph = {'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}
    >>> shortest_path(graph, 'A', 'D')
    ['A', 'B', 'D']
    """
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


def shortest_path_length(graph, start, end):
    """
    Находит длину кратчайшего пути
    """
    if start == end:
        return 0
    
    queue = deque([(start, 0)])
    visited = {start}
    
    while queue:
        vertex, distance = queue.popleft()
        
        for neighbor in graph.get(vertex, []):
            if neighbor == end:
                return distance + 1
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))
    
    return -1  # Путь не найден


# ============================================================================
# РАСШИРЕННЫЕ ВЕРСИИ
# ============================================================================

def bfs_levels(graph, start):
    """
    Возвращает вершины по уровням
    
    >>> graph = {'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}
    >>> bfs_levels(graph, 'A')
    [[['A'], ['B', 'C'], ['D']]]
    """
    visited = set()
    queue = deque([(start, 0)])
    visited.add(start)
    levels = defaultdict(list)
    levels[0] = [start]
    
    while queue:
        vertex, level = queue.popleft()
        
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, level + 1))
                levels[level + 1].append(neighbor)
    
    return [levels[i] for i in sorted(levels.keys())]


def bfs_components(graph):
    """
    Находит связные компоненты используя BFS
    """
    visited = set()
    components = []
    
    for vertex in graph:
        if vertex not in visited:
            component = bfs(graph, vertex)
            # Добавляем все вершины компонента в visited
            visited.update(component)
            components.append(component)
    
    return components


def bfs_bidirectional(graph, start, end):
    """
    Двунаправленный BFS для более быстрого поиска пути
    """
    if start == end:
        return [start]
    
    # Очереди для поиска от start и от end
    queue_start = deque([start])
    queue_end = deque([end])
    
    # Словари для хранения путей
    path_start = {start: [start]}
    path_end = {end: [end]}
    
    visited_start = {start}
    visited_end = {end}
    
    while queue_start and queue_end:
        # Поиск от start
        if queue_start:
            vertex = queue_start.popleft()
            
            for neighbor in graph.get(vertex, []):
                if neighbor in visited_end:
                    # Найдено пересечение
                    return path_start[vertex] + path_end[neighbor][::-1]
                
                if neighbor not in visited_start:
                    visited_start.add(neighbor)
                    queue_start.append(neighbor)
                    path_start[neighbor] = path_start[vertex] + [neighbor]
        
        # Поиск от end
        if queue_end:
            vertex = queue_end.popleft()
            
            for neighbor in graph.get(vertex, []):
                if neighbor in visited_start:
                    # Найдено пересечение
                    return path_start[neighbor] + path_end[vertex][::-1]
                
                if neighbor not in visited_end:
                    visited_end.add(neighbor)
                    queue_end.append(neighbor)
                    path_end[neighbor] = path_end[vertex] + [neighbor]
    
    return None


# ============================================================================
# BFS ДЛЯ РАЗНЫХ ТИПОВ ГРАФОВ
# ============================================================================

def bfs_matrix(matrix, start_row, start_col):
    """
    BFS для 2D матрицы (поиск кратчайшего пути в лабиринте)
    """
    rows, cols = len(matrix), len(matrix[0])
    visited = set()
    queue = deque([(start_row, start_col, 0)])
    visited.add((start_row, start_col))
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while queue:
        row, col, distance = queue.popleft()
        
        # Проверяем, достигли ли цели (например, выхода)
        if matrix[row][col] == 'E':  # E - выход
            return distance
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            if (0 <= new_row < rows and 0 <= new_col < cols and
                (new_row, new_col) not in visited and
                matrix[new_row][new_col] != '#'):  # # - стена
                
                visited.add((new_row, new_col))
                queue.append((new_row, new_col, distance + 1))
    
    return -1  # Путь не найден


def bfs_tree_levels(tree, root):
    """
    BFS для дерева - обход по уровням
    """
    if not tree:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node)
            
            # Добавляем детей в очередь
            for child in tree.get(node, []):
                queue.append(child)
        
        result.append(level)
    
    return result


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

def demonstrate_bfs():
    """
    Демонстрация работы алгоритма
    """
    print("=" * 60)
    print("BFS (BREADTH-FIRST SEARCH) - Демонстрация")
    print("=" * 60)
    
    # Создаем граф
    graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['F'],
        'F': []
    }
    
    print(f"Граф: {graph}")
    
    # Тест 1: Базовый BFS
    print(f"\nТест 1: BFS от вершины 'A'")
    result1 = bfs(graph, 'A')
    print(f"Результат: {result1}")
    
    # Тест 2: Кратчайший путь
    print(f"\nТест 2: Кратчайший путь от 'A' до 'F'")
    path = shortest_path(graph, 'A', 'F')
    print(f"Путь: {path}")
    print(f"Длина пути: {len(path) - 1}")
    
    # Тест 3: Длина пути
    print(f"\nТест 3: Длина кратчайшего пути от 'A' до 'D'")
    length = shortest_path_length(graph, 'A', 'D')
    print(f"Длина: {length}")
    
    # Тест 4: Обход по уровням
    print(f"\nТест 4: Обход по уровням")
    levels = bfs_levels(graph, 'A')
    for i, level in enumerate(levels):
        print(f"Уровень {i}: {level}")
    
    # Тест 5: Связные компоненты
    print(f"\nТест 5: Связные компоненты")
    disconnected_graph = {
        'A': ['B'],
        'B': ['A'],
        'C': ['D'],
        'D': ['C'],
        'E': []
    }
    print(f"Граф: {disconnected_graph}")
    components = bfs_components(disconnected_graph)
    print(f"Компоненты: {components}")
    
    # Пошаговое исполнение
    print("\n" + "=" * 60)
    print("ПОШАГОВОЕ ИСПОЛНЕНИЕ")
    print("=" * 60)
    bfs_with_steps(graph, 'A')


# ============================================================================
# СРАВНЕНИЕ DFS И BFS
# ============================================================================

def compare_dfs_bfs():
    """
    Сравнение DFS и BFS
    """
    print("\n" + "=" * 60)
    print("СРАВНЕНИЕ DFS И BFS")
    print("=" * 60)
    
    graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['F'],
        'F': []
    }
    
    print("Граф:")
    for vertex, neighbors in graph.items():
        print(f"  {vertex} -> {neighbors}")
    
    print(f"\nDFS от 'A': {dfs_recursive(graph, 'A')}")
    print(f"BFS от 'A': {bfs(graph, 'A')}")
    
    print("\nСравнение:")
    print("┌─────────────────┬─────────────────┬─────────────────┐")
    print("│ Характеристика  │ DFS             │ BFS             │")
    print("├─────────────────┼─────────────────┼─────────────────┤")
    print("│ Структура данных│ Стек            │ Очередь         │")
    print("│ Порядок обхода  │ Вглубь          │ По уровням      │")
    print("│ Кратчайший путь │ Не гарантирован │ Гарантирован    │")
    print("│ Память          │ O(V)            │ O(V)            │")
    print("│ Время           │ O(V + E)        │ O(V + E)        │")
    print("└─────────────────┴─────────────────┴─────────────────┘")


# ============================================================================
# АНАЛИЗ СЛОЖНОСТИ
# ============================================================================

def analyze_complexity():
    """
    Анализ временной и пространственной сложности
    """
    print("\n" + "=" * 60)
    print("АНАЛИЗ СЛОЖНОСТИ BFS")
    print("=" * 60)
    
    print("Временная сложность:")
    print("- O(V + E) где V - вершины, E - рёбра")
    print("- Каждая вершина добавляется в очередь один раз")
    print("- Каждое ребро проверяется один раз")
    
    print("\nПространственная сложность:")
    print("- O(V) - размер очереди в худшем случае")
    print("- O(V) - множество посещенных вершин")
    
    print("\nОсобенности:")
    print("- Гарантирует кратчайший путь для невзвешенных графов")
    print("- Использует больше памяти чем DFS (очередь vs стек)")
    print("- Подходит для поиска по уровням")


# ============================================================================
# ПРАКТИЧЕСКИЕ ПРИМЕНЕНИЯ
# ============================================================================

def practical_applications():
    """
    Практические применения BFS
    """
    print("\n" + "=" * 60)
    print("ПРАКТИЧЕСКИЕ ПРИМЕНЕНИЯ BFS")
    print("=" * 60)
    
    print("1. Кратчайшие пути:")
    print("   - Поиск кратчайшего пути в невзвешенном графе")
    print("   - Навигация в играх")
    print("   - Сетевые протоколы")
    
    print("\n2. Социальные сети:")
    print("   - Поиск людей на расстоянии N")
    print("   - Анализ влияния")
    print("   - Рекомендации")
    
    print("\n3. Лабиринты и игры:")
    print("   - Поиск выхода из лабиринта")
    print("   - ИИ для игр")
    print("   - Поиск ближайших объектов")
    
    print("\n4. Сетевые алгоритмы:")
    print("   - Поиск в локальной сети")
    print("   - Обнаружение устройств")
    print("   - Анализ топологии")
    
    print("\n5. Веб-краулеры:")
    print("   - Поиск страниц на определенной глубине")
    print("   - Контроль глубины сканирования")
    print("   - Анализ структуры сайта")


def dfs_recursive(graph, start, visited=None):
    """Импорт функции DFS для сравнения"""
    if visited is None:
        visited = set()
    
    visited.add(start)
    result = [start]
    
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            result.extend(dfs_recursive(graph, neighbor, visited))
    
    return result


if __name__ == "__main__":
    demonstrate_bfs()
    compare_dfs_bfs()
    analyze_complexity()
    practical_applications()
