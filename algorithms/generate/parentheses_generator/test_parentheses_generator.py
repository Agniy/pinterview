"""
Тесты для алгоритма генерации скобочных последовательностей.
"""

import pytest
from parentheses_generator import (
    generate_basic, 
    generate_optimized, 
    generate_iterative,
    count_sequences,
    catalan_number,
    benchmark_algorithms
)


class TestParenthesesGenerator:
    """Тесты для всех версий алгоритма генерации скобочных последовательностей."""
    
    def test_generate_basic_edge_cases(self):
        """Тестирование граничных случаев для базового алгоритма."""
        assert generate_basic(0) == [""]
        assert generate_basic(1) == ["()"]
    
    def test_generate_optimized_edge_cases(self):
        """Тестирование граничных случаев для оптимизированного алгоритма."""
        assert generate_optimized(0) == [""]
        assert generate_optimized(1) == ["()"]
    
    def test_generate_iterative_edge_cases(self):
        """Тестирование граничных случаев для итеративного алгоритма."""
        assert generate_iterative(0) == [""]
        assert generate_iterative(1) == ["()"]
    
    def test_generate_basic_small_values(self):
        """Тестирование базового алгоритма для малых значений."""
        assert generate_basic(2) == ["(())", "()()"]
        assert generate_basic(3) == ["((()))", "(()())", "(())()", "()(())", "()()()"]
    
    def test_generate_optimized_small_values(self):
        """Тестирование оптимизированного алгоритма для малых значений."""
        assert generate_optimized(2) == ["(())", "()()"]
        assert generate_optimized(3) == ["((()))", "(()())", "(())()", "()(())", "()()()"]
    
    def test_generate_iterative_small_values(self):
        """Тестирование итеративного алгоритма для малых значений."""
        assert generate_iterative(2) == ["(())", "()()"]
        assert generate_iterative(3) == ["((()))", "(()())", "(())()", "()(())", "()()()"]
    
    def test_all_algorithms_produce_same_result(self):
        """Проверка, что все алгоритмы дают одинаковый результат."""
        for n in range(1, 5):
            basic = set(generate_basic(n))
            optimized = set(generate_optimized(n))
            iterative = set(generate_iterative(n))
            
            assert basic == optimized == iterative, f"Алгоритмы дают разные результаты для n={n}"
    
    def test_validity_of_generated_sequences(self):
        """Проверка валидности всех сгенерированных последовательностей."""
        def is_valid_parentheses(s: str) -> bool:
            """Проверяет, является ли строка валидной скобочной последовательностью."""
            if not s:
                return True
            
            count = 0
            for char in s:
                if char == '(':
                    count += 1
                elif char == ')':
                    count -= 1
                    if count < 0:
                        return False
            
            return count == 0
        
        for n in range(1, 5):
            sequences = generate_basic(n)
            
            # Проверяем количество
            assert len(sequences) == count_sequences(n)
            
            # Проверяем валидность каждой последовательности
            for seq in sequences:
                assert is_valid_parentheses(seq), f"Невалидная последовательность: {seq}"
                assert len(seq) == 2 * n, f"Неправильная длина последовательности: {seq}"
    
    def test_no_duplicates(self):
        """Проверка отсутствия дубликатов в результатах."""
        for n in range(1, 5):
            sequences = generate_basic(n)
            assert len(sequences) == len(set(sequences)), f"Есть дубликаты для n={n}"
    
    def test_catalan_numbers(self):
        """Тестирование вычисления каталанских чисел."""
        expected = [1, 1, 2, 5, 14, 42, 132, 429]
        for i, expected_val in enumerate(expected):
            assert catalan_number(i) == expected_val, f"Неправильное каталанское число для n={i}"
    
    def test_count_sequences(self):
        """Тестирование функции подсчета количества последовательностей."""
        expected_counts = [1, 1, 2, 5, 14, 42, 132, 429]
        for i, expected_count in enumerate(expected_counts):
            assert count_sequences(i) == expected_count, f"Неправильный подсчет для n={i}"
    
    def test_large_input_handling(self):
        """Тестирование обработки больших входных данных."""
        # Для n=5 должно быть 42 последовательности
        sequences = generate_basic(5)
        assert len(sequences) == 42
        
        # Проверяем, что все последовательности валидны
        for seq in sequences:
            assert len(seq) == 10  # 2 * 5
            # Простая проверка валидности
            count = 0
            for char in seq:
                if char == '(':
                    count += 1
                else:
                    count -= 1
                assert count >= 0, f"Невалидная последовательность: {seq}"
            assert count == 0, f"Невалидная последовательность: {seq}"


class TestPerformance:
    """Тесты производительности."""
    
    def test_benchmark_function_works(self):
        """Проверка, что функция бенчмарка работает корректно."""
        results = benchmark_algorithms(3, 2)
        
        assert 'basic' in results
        assert 'optimized' in results
        assert 'iterative' in results
        
        # Проверяем, что все алгоритмы дают одинаковое количество результатов
        counts = [results[algo]['count'] for algo in results]
        assert all(count == counts[0] for count in counts)
        
        # Проверяем, что количество совпадает с ожидаемым
        assert counts[0] == count_sequences(3)


@pytest.fixture
def sample_sequences():
    """Фикстура с примерами последовательностей для тестов."""
    return {
        1: ["()"],
        2: ["(())", "()()"],
        3: ["((()))", "(()())", "(())()", "()(())", "()()()"],
        4: [
            "(((())))", "((()()))", "((())())", "((()))()", "(()(()))",
            "(()()())", "(()())()", "(())(())", "(())()()", "()((()))",
            "()(()())", "()(())()", "()()(())", "()()()()"
        ]
    }


def test_sequences_match_expected(sample_sequences):
    """Тест проверяет, что генерируемые последовательности соответствуют ожидаемым."""
    for n, expected in sample_sequences.items():
        actual = generate_basic(n)
        assert set(actual) == set(expected), f"Несоответствие для n={n}"


def test_sequences_are_sorted():
    """Проверка, что последовательности генерируются в правильном порядке."""
    for n in range(1, 5):
        sequences = generate_basic(n)
        # Проверяем, что последовательности отсортированы
        assert sequences == sorted(sequences), f"Последовательности не отсортированы для n={n}"


if __name__ == "__main__":
    # Запуск тестов
    pytest.main([__file__, "-v"])
