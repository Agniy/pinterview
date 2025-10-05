#!/usr/bin/env python3
"""
Демонстрационный скрипт для алгоритма генерации скобочных последовательностей.
"""

from parentheses_generator import (
    generate_basic, 
    generate_optimized, 
    generate_iterative,
    count_sequences,
    explain_algorithm,
    benchmark_algorithms
)


def demo_basic_usage():
    """Демонстрация базового использования алгоритмов."""
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ БАЗОВОГО ИСПОЛЬЗОВАНИЯ")
    print("=" * 60)
    
    for n in range(1, 6):
        print(f"\nДля n={n}:")
        sequences = generate_basic(n)
        print(f"  Количество последовательностей: {len(sequences)}")
        print(f"  Последовательности: {sequences}")
        
        # Проверяем, что количество совпадает с каталанским числом
        expected_count = count_sequences(n)
        print(f"  Ожидаемое количество (каталанское число): {expected_count}")
        print(f"  ✓ Совпадение: {len(sequences) == expected_count}")


def demo_algorithm_comparison():
    """Демонстрация сравнения разных алгоритмов."""
    print("\n" + "=" * 60)
    print("СРАВНЕНИЕ АЛГОРИТМОВ")
    print("=" * 60)
    
    n = 4
    print(f"\nГенерация для n={n}:")
    
    # Базовый алгоритм
    basic_result = generate_basic(n)
    print(f"Базовый алгоритм: {len(basic_result)} последовательностей")
    
    # Оптимизированный алгоритм
    optimized_result = generate_optimized(n)
    print(f"Оптимизированный алгоритм: {len(optimized_result)} последовательностей")
    
    # Итеративный алгоритм
    iterative_result = generate_iterative(n)
    print(f"Итеративный алгоритм: {len(iterative_result)} последовательностей")
    
    # Проверяем, что все результаты одинаковые
    all_same = (
        set(basic_result) == set(optimized_result) == set(iterative_result)
    )
    print(f"✓ Все алгоритмы дают одинаковый результат: {all_same}")


def demo_performance_benchmark():
    """Демонстрация бенчмарка производительности."""
    print("\n" + "=" * 60)
    print("БЕНЧМАРК ПРОИЗВОДИТЕЛЬНОСТИ")
    print("=" * 60)
    
    # Тестируем для разных значений n
    for n in [3, 4, 5]:
        print(f"\nТестирование для n={n}:")
        results = benchmark_algorithms(n, 3)
        
        print(f"{'Алгоритм':<12} {'Время (сек)':<12} {'Количество':<12} {'Ожидаемое':<12}")
        print("-" * 50)
        
        for algo_name, result in results.items():
            print(f"{algo_name:<12} {result['avg_time']:<12.6f} "
                  f"{result['count']:<12} {result['expected_count']:<12}")


def demo_step_by_step():
    """Демонстрация пошагового объяснения."""
    print("\n" + "=" * 60)
    print("ПОШАГОВОЕ ОБЪЯСНЕНИЕ")
    print("=" * 60)
    
    # Подробное объяснение для n=3
    explain_algorithm(3)


def demo_validation():
    """Демонстрация валидации результатов."""
    print("\n" + "=" * 60)
    print("ВАЛИДАЦИЯ РЕЗУЛЬТАТОВ")
    print("=" * 60)
    
    def is_valid_parentheses(s: str) -> bool:
        """Проверяет валидность скобочной последовательности."""
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
    
    n = 4
    sequences = generate_basic(n)
    
    print(f"\nПроверка валидности для n={n}:")
    print(f"Всего последовательностей: {len(sequences)}")
    
    valid_count = 0
    for i, seq in enumerate(sequences, 1):
        is_valid = is_valid_parentheses(seq)
        valid_count += is_valid
        status = "✓" if is_valid else "✗"
        print(f"{i:2d}. {seq} {status}")
    
    print(f"\nВалидных последовательностей: {valid_count}/{len(sequences)}")
    print(f"✓ Все последовательности валидны: {valid_count == len(sequences)}")


def demo_edge_cases():
    """Демонстрация граничных случаев."""
    print("\n" + "=" * 60)
    print("ГРАНИЧНЫЕ СЛУЧАИ")
    print("=" * 60)
    
    # n = 0
    result_0 = generate_basic(0)
    print(f"n=0: {result_0} (должно быть [\"\"])")
    
    # n = 1
    result_1 = generate_basic(1)
    print(f"n=1: {result_1} (должно быть [\"()\"])")
    
    # Проверяем все алгоритмы
    algorithms = [generate_basic, generate_optimized, generate_iterative]
    names = ["basic", "optimized", "iterative"]
    
    print(f"\nСравнение всех алгоритмов для граничных случаев:")
    for n in [0, 1]:
        print(f"\nn={n}:")
        results = []
        for algo in algorithms:
            result = algo(n)
            results.append(set(result))
            print(f"  {algo.__name__}: {result}")
        
        all_same = all(r == results[0] for r in results)
        print(f"  ✓ Все алгоритмы дают одинаковый результат: {all_same}")


def main():
    """Главная функция демонстрации."""
    print("ДЕМОНСТРАЦИЯ АЛГОРИТМА ГЕНЕРАЦИИ СКОБОЧНЫХ ПОСЛЕДОВАТЕЛЬНОСТЕЙ")
    print("=" * 70)
    
    try:
        # Запускаем все демонстрации
        demo_basic_usage()
        demo_algorithm_comparison()
        demo_performance_benchmark()
        demo_step_by_step()
        demo_validation()
        demo_edge_cases()
        
        print("\n" + "=" * 70)
        print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА УСПЕШНО!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\nОшибка во время демонстрации: {e}")
        raise


if __name__ == "__main__":
    main()
