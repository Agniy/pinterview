"""
🟡 ГЕНЕРАТОРЫ (Generators) - Вопросы и задачи для собеседований

Основные темы:
- yield
- Generator expressions
- Итераторы vs генераторы
- send(), throw(), close()
- yield from
"""

import sys


# ============================================================================
# ТЕОРЕТИЧЕСКИЕ ВОПРОСЫ
# ============================================================================

"""
Q1: Что такое генератор?
A: Функция, которая использует yield вместо return и возвращает
итератор, генерирующий значения по требованию (lazy evaluation).

Q2: В чем преимущество генераторов?
A:
- Экономия памяти (не хранят все значения)
- Ленивые вычисления (вычисляют по требованию)
- Могут работать с бесконечными последовательностями

Q3: В чем разница между yield и return?
A:
- return завершает функцию
- yield приостанавливает выполнение и возвращает значение,
  сохраняя состояние для продолжения

Q4: Что такое generator expression?
A: Компактная запись генератора: (x**2 for x in range(10))
Аналог list comprehension, но возвращает генератор, а не список.

Q5: Что делают методы send(), throw(), close()?
A:
- send(value) - отправляет значение в генератор
- throw(exception) - вызывает исключение внутри генератора
- close() - завершает генератор

Q6: Что такое yield from?
A: Делегирует выполнение другому генератору (Python 3.3+)
"""


# ============================================================================
# ЗАДАЧА 1: Простой генератор - последовательность чисел
# ============================================================================

def count_up_to(n):
    """
    🟢 Junior level
    Генератор чисел от 1 до n
    
    >>> list(count_up_to(5))
    [1, 2, 3, 4, 5]
    """
    count = 1
    while count <= n:
        yield count
        count += 1


def demo_count():
    print("Генератор от 1 до 5:")
    for num in count_up_to(5):
        print(num, end=' ')
    print()


# ============================================================================
# ЗАДАЧА 2: Бесконечный генератор
# ============================================================================

def infinite_sequence():
    """
    🟢 Junior level
    Бесконечная последовательность чисел
    """
    num = 0
    while True:
        yield num
        num += 1


def demo_infinite():
    print("\nПервые 10 чисел из бесконечного генератора:")
    gen = infinite_sequence()
    for _ in range(10):
        print(next(gen), end=' ')
    print()


# ============================================================================
# ЗАДАЧА 3: Генератор Фибоначчи
# ============================================================================

def fibonacci():
    """
    🟡 Middle level
    Бесконечный генератор чисел Фибоначчи
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def fibonacci_up_to(n):
    """
    Генератор Фибоначчи до n
    """
    a, b = 0, 1
    while a <= n:
        yield a
        a, b = b, a + b


def demo_fibonacci():
    print("\nПервые 10 чисел Фибоначчи:")
    fib = fibonacci()
    for _ in range(10):
        print(next(fib), end=' ')
    print()
    
    print("Фибоначчи до 100:")
    print(list(fibonacci_up_to(100)))


# ============================================================================
# ЗАДАЧА 4: Generator Expression
# ============================================================================

def demo_generator_expression():
    """
    🟢 Junior level
    Примеры generator expressions
    """
    
    # Квадраты чисел
    squares = (x**2 for x in range(10))
    print("\nКвадраты (generator):")
    print(list(squares))
    
    # Сравнение памяти: list vs generator
    list_comp = [x**2 for x in range(1000)]
    gen_exp = (x**2 for x in range(1000))
    
    print(f"\nРазмер list comprehension: {sys.getsizeof(list_comp)} bytes")
    print(f"Размер generator expression: {sys.getsizeof(gen_exp)} bytes")
    
    # Фильтрация с генератором
    even_squares = (x**2 for x in range(20) if x % 2 == 0)
    print(f"Четные квадраты: {list(even_squares)}")


# ============================================================================
# ЗАДАЧА 5: Чтение больших файлов
# ============================================================================

def read_large_file(file_path):
    """
    🟡 Middle level
    Генератор для чтения больших файлов построчно
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield line.strip()


def read_in_chunks(file_path, chunk_size=1024):
    """
    Чтение файла кусками
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk


# ============================================================================
# ЗАДАЧА 6: Генератор простых чисел
# ============================================================================

def is_prime(n):
    """Проверка на простое число"""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def primes_generator(limit=None):
    """
    🟡 Middle level
    Генератор простых чисел
    """
    num = 2
    while limit is None or num <= limit:
        if is_prime(num):
            yield num
        num += 1


def demo_primes():
    print("\nПервые 10 простых чисел:")
    gen = primes_generator()
    for _ in range(10):
        print(next(gen), end=' ')
    print()


# ============================================================================
# ЗАДАЧА 7: Генератор перестановок
# ============================================================================

def permutations(items):
    """
    🔴 Senior level
    Генератор всех перестановок списка
    """
    if len(items) <= 1:
        yield items
    else:
        for i, item in enumerate(items):
            rest = items[:i] + items[i+1:]
            for p in permutations(rest):
                yield [item] + p


def demo_permutations():
    print("\nПерестановки [1, 2, 3]:")
    for perm in permutations([1, 2, 3]):
        print(perm)


# ============================================================================
# ЗАДАЧА 8: Генератор с send()
# ============================================================================

def running_average():
    """
    🔴 Senior level
    Генератор вычисляющий скользящее среднее
    """
    total = 0
    count = 0
    average = None
    
    while True:
        value = yield average
        if value is not None:
            total += value
            count += 1
            average = total / count


def demo_send():
    print("\nСкользящее среднее с send():")
    avg_gen = running_average()
    next(avg_gen)  # Инициализация
    
    print(f"Добавляем 10: {avg_gen.send(10)}")
    print(f"Добавляем 20: {avg_gen.send(20)}")
    print(f"Добавляем 30: {avg_gen.send(30)}")


# ============================================================================
# ЗАДАЧА 9: yield from
# ============================================================================

def chain(*iterables):
    """
    🟡 Middle level
    Объединяет несколько итераторов
    """
    for iterable in iterables:
        yield from iterable


def demo_yield_from():
    print("\nyield from - объединение итераторов:")
    result = list(chain([1, 2, 3], [4, 5], [6, 7, 8]))
    print(result)


def flatten(nested_list):
    """
    Рекурсивное разворачивание вложенного списка
    """
    for item in nested_list:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


def demo_flatten():
    print("\nРазворачивание вложенного списка:")
    nested = [1, [2, 3, [4, 5]], 6, [7, [8, 9]]]
    print(f"Вложенный: {nested}")
    print(f"Развернутый: {list(flatten(nested))}")


# ============================================================================
# ЗАДАЧА 10: Генератор окон (sliding window)
# ============================================================================

def sliding_window(iterable, window_size):
    """
    🟡 Middle level
    Генератор скользящего окна
    
    >>> list(sliding_window([1, 2, 3, 4, 5], 3))
    [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
    """
    from collections import deque
    
    iterator = iter(iterable)
    window = deque(maxlen=window_size)
    
    # Заполняем первое окно
    for _ in range(window_size):
        try:
            window.append(next(iterator))
        except StopIteration:
            return
    
    yield list(window)
    
    # Скользим
    for item in iterator:
        window.append(item)
        yield list(window)


def demo_sliding_window():
    print("\nСкользящее окно размером 3:")
    for window in sliding_window([1, 2, 3, 4, 5, 6], 3):
        print(window)


# ============================================================================
# ЗАДАЧА 11: Генератор батчей
# ============================================================================

def batch_generator(iterable, batch_size):
    """
    🟡 Middle level
    Разбивает последовательность на батчи
    """
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    
    # Последний неполный батч
    if batch:
        yield batch


def demo_batches():
    print("\nБатчи размером 3:")
    for batch in batch_generator(range(10), 3):
        print(batch)


# ============================================================================
# ЗАДАЧА 12: Генератор с состоянием (конечный автомат)
# ============================================================================

def traffic_light():
    """
    🔴 Senior level
    Генератор-светофор (конечный автомат)
    """
    states = ['Red', 'Yellow', 'Green', 'Yellow']
    index = 0
    
    while True:
        command = yield states[index]
        
        if command == 'next':
            index = (index + 1) % len(states)
        elif command == 'reset':
            index = 0


def demo_traffic_light():
    print("\nГенератор-светофор:")
    light = traffic_light()
    print(f"Старт: {next(light)}")
    print(f"Next: {light.send('next')}")
    print(f"Next: {light.send('next')}")
    print(f"Next: {light.send('next')}")
    print(f"Reset: {light.send('reset')}")


# ============================================================================
# ЗАДАЧА 13: Параллельная обработка с генераторами
# ============================================================================

def process_pipeline(data):
    """
    🔴 Senior level
    Цепочка обработки данных через генераторы
    """
    
    def read_data():
        for item in data:
            yield item
    
    def filter_even(gen):
        for item in gen:
            if item % 2 == 0:
                yield item
    
    def square(gen):
        for item in gen:
            yield item ** 2
    
    def multiply_by_10(gen):
        for item in gen:
            yield item * 10
    
    # Построение pipeline
    pipeline = read_data()
    pipeline = filter_even(pipeline)
    pipeline = square(pipeline)
    pipeline = multiply_by_10(pipeline)
    
    return pipeline


def demo_pipeline():
    print("\nPipeline обработки:")
    data = range(1, 11)
    print(f"Исходные данные: {list(data)}")
    
    result = list(process_pipeline(data))
    print(f"Результат (четные -> квадрат -> *10): {result}")


# ============================================================================
# ЗАДАЧА 14: Генератор для итерации по дереву
# ============================================================================

class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def inorder_traversal(root):
    """
    🔴 Senior level
    Генератор для обхода дерева (in-order)
    """
    if root:
        yield from inorder_traversal(root.left)
        yield root.value
        yield from inorder_traversal(root.right)


def demo_tree():
    print("\nОбход дерева:")
    #       4
    #      / \
    #     2   6
    #    / \ / \
    #   1  3 5  7
    
    tree = TreeNode(4,
        TreeNode(2, TreeNode(1), TreeNode(3)),
        TreeNode(6, TreeNode(5), TreeNode(7))
    )
    
    print("In-order:", list(inorder_traversal(tree)))


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("ГЕНЕРАТОРЫ - Примеры и тесты")
    print("=" * 60)
    
    # Тест 1: Простой генератор
    demo_count()
    
    # Тест 2: Бесконечный генератор
    demo_infinite()
    
    # Тест 3: Фибоначчи
    demo_fibonacci()
    
    # Тест 4: Generator expressions
    demo_generator_expression()
    
    # Тест 5: Простые числа
    demo_primes()
    
    # Тест 6: Перестановки
    demo_permutations()
    
    # Тест 7: send()
    demo_send()
    
    # Тест 8: yield from
    demo_yield_from()
    demo_flatten()
    
    # Тест 9: Скользящее окно
    demo_sliding_window()
    
    # Тест 10: Батчи
    demo_batches()
    
    # Тест 11: Светофор (состояние)
    demo_traffic_light()
    
    # Тест 12: Pipeline
    demo_pipeline()
    
    # Тест 13: Обход дерева
    demo_tree()
    
    print("\n" + "=" * 60)

