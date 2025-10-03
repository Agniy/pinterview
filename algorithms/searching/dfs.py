"""
🟡 DFS (DEPTH-FIRST SEARCH) - Поиск в глубину

Временная сложность:
- O(V + E) где V - количество вершин, E - количество рёбер

Пространственная сложность:
- Рекурсивная версия: O(V) - глубина стека вызовов
- Итеративная версия: O(V) - размер стека

Особенности:
- Использует стек (явный или неявный)
- Идет максимально глубоко по одной ветке
- Подходит для поиска путей, циклов, топологической сортировки
- Основа для многих алгоритмов на графах
"""

from collections import defaultdict


def dfs_recursive(graph, start, visited=None):
    """
    🟡 Middle level
    Поиск в глубину (рекурсивная версия)
    
    Принцип работы:
    1. Помечаем текущую вершину как посещенную
    2. Обрабатываем текущую вершину
    3. Рекурсивно посещаем все непосещенные соседние вершины
    
    Args:
        graph: граф в виде словаря {вершина: [соседи]}
        start: начальная вершина
        visited: множество посещенных вершин
        
    Returns:
        список вершин в порядке обхода DFS
        
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
    Поиск в глубину (итеративная версия)
    
    Использует явный стек вместо рекурсии
    """
    visited = set()
    stack = [start]
    result = []
    
    while stack:
        vertex = stack.pop()
        
        if vertex not in visited:
            visited.add(vertex)
            result.append(vertex)
            
            # Добавляем соседей в обратном порядке для сохранения порядка
            for neighbor in reversed(graph.get(vertex, [])):
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return result


# ============================================================================
# ПОШАГОВОЕ ИСПОЛНЕНИЕ
# ============================================================================

def dfs_with_steps(graph, start, visited=None, level=0):
    """
    Версия с выводом пошагового исполнения
    """
    if visited is None:
        visited = set()
    
    indent = "  " * level
    print(f"{indent}Посещаем вершину: {start}")
    print(f"{indent}Стек вызовов: {visited}")
    
    visited.add(start)
    result = [start]
    
    neighbors = graph.get(start, [])
    print(f"{indent}Соседи {start}: {neighbors}")
    
    for i, neighbor in enumerate(neighbors):
        if neighbor not in visited:
            print(f"{indent}Переходим к соседу {i+1}/{len(neighbors)}: {neighbor}")
            result.extend(dfs_with_steps(graph, neighbor, visited, level + 1))
        else:
            print(f"{indent}Сосед {neighbor} уже посещен, пропускаем")
    
    print(f"{indent}Возвращаемся из вершины {start}")
    return result


# ============================================================================
# РАСШИРЕННЫЕ ВЕРСИИ
# ============================================================================

def dfs_path(graph, start, end, path=None):
    """
    Находит путь от start до end используя DFS
    
    >>> graph = {'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}
    >>> dfs_path(graph, 'A', 'D')
    ['A', 'B', 'D']
    """
    if path is None:
        path = []
    
    path = path + [start]
    
    if start == end:
        return path
    
    for neighbor in graph.get(start, []):
        if neighbor not in path:  # Избегаем циклов
            new_path = dfs_path(graph, neighbor, end, path)
            if new_path:
                return new_path
    
    return None


def dfs_all_paths(graph, start, end, path=None):
    """
    Находит все пути от start до end
    """
    if path is None:
        path = []
    
    path = path + [start]
    
    if start == end:
        return [path]
    
    paths = []
    for neighbor in graph.get(start, []):
        if neighbor not in path:
            new_paths = dfs_all_paths(graph, neighbor, end, path)
            for new_path in new_paths:
                paths.append(new_path)
    
    return paths


def dfs_components(graph):
    """
    Находит все связные компоненты графа
    """
    visited = set()
    components = []
    
    for vertex in graph:
        if vertex not in visited:
            component = dfs_recursive(graph, vertex, visited)
            components.append(component)
    
    return components


def dfs_cycle_detection(graph):
    """
    Обнаруживает циклы в графе
    """
    def has_cycle(vertex, visited, rec_stack):
        visited.add(vertex)
        rec_stack.add(vertex)
        
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                if has_cycle(neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                return True
        
        rec_stack.remove(vertex)
        return False
    
    visited = set()
    rec_stack = set()
    
    for vertex in graph:
        if vertex not in visited:
            if has_cycle(vertex, visited, rec_stack):
                return True
    
    return False


# ============================================================================
# DFS ДЛЯ РАЗНЫХ ТИПОВ ГРАФОВ
# ============================================================================

def dfs_tree(tree, root):
    """
    DFS для дерева
    """
    result = []
    
    def traverse(node):
        if node is None:
            return
        result.append(node)
        for child in tree.get(node, []):
            traverse(child)
    
    traverse(root)
    return result


def dfs_matrix(matrix, start_row, start_col, visited=None):
    """
    DFS для 2D матрицы (поиск островов, лабиринтов)
    """
    if visited is None:
        visited = set()
    
    rows, cols = len(matrix), len(matrix[0])
    
    # Проверяем границы и посещенные ячейки
    if (start_row < 0 or start_row >= rows or 
        start_col < 0 or start_col >= cols or
        (start_row, start_col) in visited):
        return
    
    visited.add((start_row, start_col))
    
    # Рекурсивно посещаем соседние ячейки
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dr, dc in directions:
        dfs_matrix(matrix, start_row + dr, start_col + dc, visited)
    
    return visited


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

def demonstrate_dfs():
    """
    Демонстрация работы алгоритма
    """
    print("=" * 60)
    print("DFS (DEPTH-FIRST SEARCH) - Демонстрация")
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
    
    # Тест 1: Базовый DFS
    print(f"\nТест 1: DFS от вершины 'A'")
    result1 = dfs_recursive(graph, 'A')
    print(f"Рекурсивная версия: {result1}")
    
    result1_iter = dfs_iterative(graph, 'A')
    print(f"Итеративная версия: {result1_iter}")
    
    # Тест 2: Поиск пути
    print(f"\nТест 2: Поиск пути от 'A' до 'F'")
    path = dfs_path(graph, 'A', 'F')
    print(f"Путь: {path}")
    
    # Тест 3: Все пути
    print(f"\nТест 3: Все пути от 'A' до 'F'")
    all_paths = dfs_all_paths(graph, 'A', 'F')
    for i, path in enumerate(all_paths):
        print(f"Путь {i+1}: {path}")
    
    # Тест 4: Связные компоненты
    print(f"\nТест 4: Связные компоненты")
    disconnected_graph = {
        'A': ['B'],
        'B': ['A'],
        'C': ['D'],
        'D': ['C'],
        'E': []
    }
    print(f"Граф: {disconnected_graph}")
    components = dfs_components(disconnected_graph)
    print(f"Компоненты: {components}")
    
    # Тест 5: Обнаружение циклов
    print(f"\nТест 5: Обнаружение циклов")
    cyclic_graph = {
        'A': ['B'],
        'B': ['C'],
        'C': ['A']
    }
    print(f"Граф с циклом: {cyclic_graph}")
    has_cycle = dfs_cycle_detection(cyclic_graph)
    print(f"Есть цикл: {has_cycle}")
    
    # Пошаговое исполнение
    print("\n" + "=" * 60)
    print("ПОШАГОВОЕ ИСПОЛНЕНИЕ")
    print("=" * 60)
    dfs_with_steps(graph, 'A')


# ============================================================================
# ВИЗУАЛИЗАЦИЯ ГРАФА
# ============================================================================

def visualize_graph(graph):
    """
    Простая визуализация графа
    """
    print("\n" + "=" * 60)
    print("ВИЗУАЛИЗАЦИЯ ГРАФА")
    print("=" * 60)
    
    print("Граф:")
    for vertex, neighbors in graph.items():
        print(f"  {vertex} -> {neighbors}")
    
    print("\nASCII представление:")
    print("     A")
    print("    / \\")
    print("   B   C")
    print("  / \\   \\")
    print(" D   E   F")


# ============================================================================
# АНАЛИЗ СЛОЖНОСТИ
# ============================================================================

def analyze_complexity():
    """
    Анализ временной и пространственной сложности
    """
    print("\n" + "=" * 60)
    print("АНАЛИЗ СЛОЖНОСТИ DFS")
    print("=" * 60)
    
    print("Временная сложность:")
    print("- O(V + E) где V - вершины, E - рёбра")
    print("- Каждая вершина посещается один раз")
    print("- Каждое ребро проверяется один раз")
    
    print("\nПространственная сложность:")
    print("- Рекурсивная версия: O(V) - глубина стека вызовов")
    print("- Итеративная версия: O(V) - размер явного стека")
    print("- Посещенные вершины: O(V)")
    
    print("\nСравнение с BFS:")
    print("- DFS: использует стек, идет вглубь")
    print("- BFS: использует очередь, идет вширь")
    print("- Оба: O(V + E) временная сложность")


# ============================================================================
# ПРАКТИЧЕСКИЕ ПРИМЕНЕНИЯ
# ============================================================================

def practical_applications():
    """
    Практические применения DFS
    """
    print("\n" + "=" * 60)
    print("ПРАКТИЧЕСКИЕ ПРИМЕНЕНИЯ DFS")
    print("=" * 60)
    
    print("1. Поиск путей:")
    print("   - Нахождение пути между двумя вершинами")
    print("   - Поиск всех возможных путей")
    print("   - Поиск гамильтоновых путей")
    
    print("\n2. Обнаружение циклов:")
    print("   - Проверка наличия циклов в графе")
    print("   - Топологическая сортировка")
    print("   - Анализ зависимостей")
    
    print("\n3. Связность:")
    print("   - Поиск связных компонентов")
    print("   - Проверка связности графа")
    print("   - Поиск мостов и точек сочленения")
    
    print("\n4. Обход деревьев:")
    print("   - Preorder, inorder, postorder обходы")
    print("   - Вычисление выражений")
    print("   - Анализ синтаксических деревьев")
    
    print("\n5. Лабиринты и игры:")
    print("   - Поиск выхода из лабиринта")
    print("   - Игры с состояниями (шахматы, судоку)")
    print("   - Backtracking алгоритмы")
    
    print("\n6. Компиляторы:")
    print("   - Анализ синтаксиса")
    print("   - Обход AST (Abstract Syntax Tree)")
    print("   - Генерация кода")


# ============================================================================
# РЕАЛЬНЫЕ ПРИМЕРЫ
# ============================================================================

def real_world_examples():
    """
    Реальные примеры использования DFS
    """
    print("\n" + "=" * 60)
    print("РЕАЛЬНЫЕ ПРИМЕРЫ")
    print("=" * 60)
    
    print("1. Социальные сети:")
    print("   - Поиск друзей через общих знакомых")
    print("   - Анализ групп и сообществ")
    print("   - Рекомендации связей")
    
    print("\n2. Веб-краулеры:")
    print("   - Обход веб-страниц по ссылкам")
    print("   - Индексация сайтов")
    print("   - Поиск мертвых ссылок")
    
    print("\n3. Файловые системы:")
    print("   - Обход директорий")
    print("   - Поиск файлов")
    print("   - Анализ структуры папок")
    
    print("\n4. Сетевые протоколы:")
    print("   - Маршрутизация в сетях")
    print("   - Поиск кратчайших путей")
    print("   - Анализ топологии сети")


if __name__ == "__main__":
    demonstrate_dfs()
    visualize_graph({'A': ['B', 'C'], 'B': ['D', 'E'], 'C': ['F'], 'D': [], 'E': ['F'], 'F': []})
    analyze_complexity()
    practical_applications()
    real_world_examples()