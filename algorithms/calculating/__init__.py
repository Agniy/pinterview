"""
Модуль с вычислительными алгоритмами
"""

from .max_consecutive import (
    max_consecutive_elements,
    max_consecutive_with_char,
    all_consecutive_sequences,
    get_next_dif_letter_idx
)
from .subarray_sum import (
    subarray_sum,
    subarray_sum_with_steps,
    subarray_sum_with_indices,
    subarray_sum_all_occurrences,
    subarray_sum_min_length,
    subarray_sum_with_negative,
    subarray_sum_prefix_sums,
    subarray_sum_prefix_sums_with_steps
)

__all__ = [
    # Max Consecutive
    'max_consecutive_elements',
    'max_consecutive_with_char',
    'all_consecutive_sequences',
    'get_next_dif_letter_idx',
    
    # Subarray Sum
    'subarray_sum',
    'subarray_sum_with_steps',
    'subarray_sum_with_indices',
    'subarray_sum_all_occurrences',
    'subarray_sum_min_length',
    'subarray_sum_with_negative',
    'subarray_sum_prefix_sums',
    'subarray_sum_prefix_sums_with_steps'
]

