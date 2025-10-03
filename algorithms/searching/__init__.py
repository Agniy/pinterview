"""
Модуль с алгоритмами поиска
"""

from .linear_search import (
    linear_search, 
    linear_search_with_steps, 
    linear_search_all_occurrences,
    linear_search_with_sentinel,
    linear_search_recursive
)
from .binary_search import (
    binary_search,
    binary_search_recursive,
    binary_search_with_steps,
    find_first_occurrence,
    find_last_occurrence,
    find_closest_element,
    count_occurrences,
    search_rotated_array,
    search_2d_matrix
)
from .dfs import (
    dfs_recursive,
    dfs_iterative,
    dfs_with_steps,
    dfs_path,
    dfs_all_paths,
    dfs_components,
    dfs_cycle_detection,
    dfs_tree,
    dfs_matrix
)
from .bfs import (
    bfs,
    bfs_with_steps,
    shortest_path,
    shortest_path_length,
    bfs_levels,
    bfs_components,
    bfs_bidirectional,
    bfs_matrix,
    bfs_tree_levels
)

__all__ = [
    # Linear Search
    'linear_search',
    'linear_search_with_steps',
    'linear_search_all_occurrences',
    'linear_search_with_sentinel',
    'linear_search_recursive',
    
    # Binary Search
    'binary_search',
    'binary_search_recursive',
    'binary_search_with_steps',
    'find_first_occurrence',
    'find_last_occurrence',
    'find_closest_element',
    'count_occurrences',
    'search_rotated_array',
    'search_2d_matrix',
    
    # DFS
    'dfs_recursive',
    'dfs_iterative',
    'dfs_with_steps',
    'dfs_path',
    'dfs_all_paths',
    'dfs_components',
    'dfs_cycle_detection',
    'dfs_tree',
    'dfs_matrix',
    
    # BFS
    'bfs',
    'bfs_with_steps',
    'shortest_path',
    'shortest_path_length',
    'bfs_levels',
    'bfs_components',
    'bfs_bidirectional',
    'bfs_matrix',
    'bfs_tree_levels'
]
