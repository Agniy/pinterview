"""
Модуль с алгоритмами рекурсии
"""

from .factorial import (
    factorial,
    factorial_iterative,
    factorial_memoized,
    factorial_with_steps,
    factorial_tail_recursive,
    factorial_big_int,
    stirling_approximation,
    factorial_ratio,
    gamma_function_approximation
)
from .fibonacci import (
    fibonacci_naive,
    fibonacci_memoized,
    fibonacci_iterative,
    fibonacci_matrix,
    fibonacci_with_steps,
    fibonacci_sequence,
    fibonacci_generator,
    fibonacci_big_int,
    fibonacci_ratio_convergence,
    fibonacci_binet
)

__all__ = [
    # Factorial
    'factorial',
    'factorial_iterative',
    'factorial_memoized',
    'factorial_with_steps',
    'factorial_tail_recursive',
    'factorial_big_int',
    'stirling_approximation',
    'factorial_ratio',
    'gamma_function_approximation',
    
    # Fibonacci
    'fibonacci_naive',
    'fibonacci_memoized',
    'fibonacci_iterative',
    'fibonacci_matrix',
    'fibonacci_with_steps',
    'fibonacci_sequence',
    'fibonacci_generator',
    'fibonacci_big_int',
    'fibonacci_ratio_convergence',
    'fibonacci_binet'
]
