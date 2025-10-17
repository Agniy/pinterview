"""
Примеры использования loop.run_in_executor()
Демонстрирует выполнение блокирующего кода в thread и process pools
"""

import asyncio
import time
import hashlib
from typing import List, Dict, Any, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# БАЗОВЫЕ ПРИМЕРЫ
# ============================================================================

# 1. Простейший пример с ThreadPoolExecutor
def blocking_io_operation(name: str, duration: float) -> str:
    """Блокирующая I/O операция"""
    logger.info(f"Начало блокирующей операции: {name}")
    time.sleep(duration)
    logger.info(f"Завершение блокирующей операции: {name}")
    return f"Результат: {name}"


async def basic_thread_pool_example():
    """Базовый пример использования ThreadPoolExecutor"""
    loop = asyncio.get_event_loop()
    
    # Создаем ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Запускаем блокирующие операции параллельно
        tasks = [
            loop.run_in_executor(executor, blocking_io_operation, f"Task-{i}", 1.0)
            for i in range(5)
        ]
        
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - start_time
        
        logger.info(f"Результаты: {results}")
        logger.info(f"Время выполнения: {elapsed:.2f}с (с 3 потоками)")


# 2. Пример с ProcessPoolExecutor для CPU-intensive задач
def cpu_intensive_fibonacci(n: int) -> int:
    """CPU-intensive вычисление числа Фибоначчи"""
    if n <= 1:
        return n
    return cpu_intensive_fibonacci(n - 1) + cpu_intensive_fibonacci(n - 2)


def calculate_fibonacci(n: int) -> Dict[str, Any]:
    """Вычисление Фибоначчи с метриками"""
    start = time.time()
    result = cpu_intensive_fibonacci(n)
    elapsed = time.time() - start
    return {
        'n': n,
        'result': result,
        'time': elapsed
    }


async def basic_process_pool_example():
    """Базовый пример использования ProcessPoolExecutor"""
    loop = asyncio.get_event_loop()
    
    # Создаем ProcessPoolExecutor для CPU-задач
    with ProcessPoolExecutor(max_workers=2) as executor:
        # Запускаем CPU-intensive задачи в разных процессах
        fibonacci_numbers = [30, 31, 32, 33]
        tasks = [
            loop.run_in_executor(executor, calculate_fibonacci, n)
            for n in fibonacci_numbers
        ]
        
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - start_time
        
        logger.info("=== Результаты вычисления Фибоначчи ===")
        for r in results:
            logger.info(f"fib({r['n']}) = {r['result']} (время: {r['time']:.3f}с)")
        logger.info(f"Общее время с ProcessPool: {elapsed:.2f}с")


# 3. Использование default executor (None)
async def default_executor_example():
    """Пример использования default executor"""
    loop = asyncio.get_event_loop()
    
    # Когда executor=None, используется default ThreadPoolExecutor
    task1 = loop.run_in_executor(None, blocking_io_operation, "Default-1", 0.5)
    task2 = loop.run_in_executor(None, blocking_io_operation, "Default-2", 0.5)
    task3 = loop.run_in_executor(None, blocking_io_operation, "Default-3", 0.5)
    
    results = await asyncio.gather(task1, task2, task3)
    logger.info(f"Результаты с default executor: {results}")


# ============================================================================
# СРАВНЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ
# ============================================================================

async def performance_comparison():
    """Сравнение последовательного и параллельного выполнения"""
    
    def heavy_computation(n: int) -> int:
        """Тяжелые вычисления"""
        time.sleep(0.5)
        return sum(i * i for i in range(n))
    
    numbers = [100000, 200000, 300000, 400000, 500000]
    
    # 1. Последовательное выполнение
    logger.info("=== Последовательное выполнение ===")
    start_time = time.time()
    sequential_results = [heavy_computation(n) for n in numbers]
    sequential_time = time.time() - start_time
    logger.info(f"Время: {sequential_time:.2f}с")
    
    # 2. Параллельное с ThreadPoolExecutor
    logger.info("\n=== Параллельное с ThreadPoolExecutor ===")
    loop = asyncio.get_event_loop()
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        tasks = [loop.run_in_executor(executor, heavy_computation, n) for n in numbers]
        parallel_results = await asyncio.gather(*tasks)
    parallel_time = time.time() - start_time
    logger.info(f"Время: {parallel_time:.2f}с")
    logger.info(f"Ускорение: {sequential_time/parallel_time:.2f}x")


# ============================================================================
# ПРАКТИЧЕСКИЕ ПРИМЕРЫ
# ============================================================================

# 4. Обработка файлов
def read_file(filename: str) -> Dict[str, Any]:
    """Блокирующее чтение файла (имитация)"""
    logger.info(f"Чтение файла: {filename}")
    time.sleep(0.3)  # Имитация I/O
    
    content = f"Содержимое файла {filename}\n" * 100
    return {
        'filename': filename,
        'size': len(content),
        'lines': content.count('\n'),
        'hash': hashlib.md5(content.encode()).hexdigest()
    }


async def parallel_file_processing():
    """Параллельная обработка файлов"""
    loop = asyncio.get_event_loop()
    files = [f"document_{i}.txt" for i in range(10)]
    
    logger.info("Начало обработки файлов...")
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        start_time = time.time()
        tasks = [loop.run_in_executor(executor, read_file, filename) for filename in files]
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - start_time
        
        total_size = sum(r['size'] for r in results)
        total_lines = sum(r['lines'] for r in results)
        
        logger.info(f"\n=== Результаты обработки файлов ===")
        logger.info(f"Файлов обработано: {len(results)}")
        logger.info(f"Общий размер: {total_size:,} байт")
        logger.info(f"Общее количество строк: {total_lines:,}")
        logger.info(f"Время: {elapsed:.2f}с")


# 5. Работа с базой данных (имитация)
def db_query(query_id: int, duration: float) -> Dict[str, Any]:
    """Имитация блокирующего запроса к БД"""
    logger.info(f"Выполнение запроса #{query_id}")
    time.sleep(duration)
    return {
        'query_id': query_id,
        'rows': query_id * 10,
        'duration': duration
    }


async def parallel_db_queries():
    """Параллельное выполнение запросов к БД"""
    loop = asyncio.get_event_loop()
    
    queries = [
        (1, 0.5),  # query_id, duration
        (2, 0.3),
        (3, 0.7),
        (4, 0.4),
        (5, 0.6)
    ]
    
    # Используем семафор для ограничения одновременных подключений к БД
    semaphore = asyncio.Semaphore(3)  # Максимум 3 одновременных запроса
    
    async def limited_db_query(qid: int, duration: float):
        async with semaphore:
            return await loop.run_in_executor(None, db_query, qid, duration)
    
    logger.info("Выполнение запросов к БД (макс. 3 одновременно)...")
    start_time = time.time()
    tasks = [limited_db_query(qid, dur) for qid, dur in queries]
    results = await asyncio.gather(*tasks)
    elapsed = time.time() - start_time
    
    logger.info(f"\n=== Результаты запросов ===")
    for r in results:
        logger.info(f"Запрос #{r['query_id']}: {r['rows']} строк за {r['duration']}с")
    logger.info(f"Общее время: {elapsed:.2f}с")


# ============================================================================
# ПРОДВИНУТЫЕ ПАТТЕРНЫ
# ============================================================================

# 6. Адаптивный выбор executor
class SmartExecutorManager:
    """Умный менеджер, выбирающий правильный executor"""
    
    def __init__(self):
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        self.process_pool = ProcessPoolExecutor(max_workers=2)
    
    async def execute(
        self, 
        func: Callable, 
        *args, 
        use_process: bool = False,
        **kwargs
    ):
        """Выполнение с автоматическим выбором executor"""
        loop = asyncio.get_event_loop()
        executor = self.process_pool if use_process else self.thread_pool
        
        return await loop.run_in_executor(
            executor, 
            lambda: func(*args, **kwargs)
        )
    
    def shutdown(self):
        """Остановка всех executor'ов"""
        self.thread_pool.shutdown(wait=True)
        self.process_pool.shutdown(wait=True)


async def smart_executor_example():
    """Пример умного выбора executor"""
    manager = SmartExecutorManager()
    
    try:
        # I/O задачи в thread pool
        io_tasks = [
            manager.execute(blocking_io_operation, f"IO-{i}", 0.5, use_process=False)
            for i in range(3)
        ]
        
        # CPU задачи в process pool
        cpu_tasks = [
            manager.execute(calculate_fibonacci, 30 + i, use_process=True)
            for i in range(2)
        ]
        
        # Выполняем все задачи параллельно
        all_results = await asyncio.gather(*io_tasks, *cpu_tasks)
        logger.info(f"Получено {len(all_results)} результатов")
        
    finally:
        manager.shutdown()


# 7. Обработка с таймаутом
async def executor_with_timeout():
    """Выполнение в executor с таймаутом"""
    loop = asyncio.get_event_loop()
    
    def slow_operation():
        time.sleep(5)  # Долгая операция
        return "Готово"
    
    try:
        # Устанавливаем таймаут 2 секунды
        task = loop.run_in_executor(None, slow_operation)
        result = await asyncio.wait_for(task, timeout=2.0)
        logger.info(f"Результат: {result}")
    except asyncio.TimeoutError:
        logger.warning("Операция превысила таймаут!")


# 8. Обработка ошибок в executor
async def error_handling_in_executor():
    """Обработка ошибок при выполнении в executor"""
    loop = asyncio.get_event_loop()
    
    def risky_operation(should_fail: bool):
        time.sleep(0.5)
        if should_fail:
            raise ValueError("Ошибка в блокирующей операции!")
        return "Успех"
    
    tasks = [
        loop.run_in_executor(None, risky_operation, False),
        loop.run_in_executor(None, risky_operation, True),
        loop.run_in_executor(None, risky_operation, False),
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.error(f"Задача {i} завершилась с ошибкой: {result}")
        else:
            logger.info(f"Задача {i} успешна: {result}")


# ============================================================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================================================

async def run_all_executor_examples():
    """Запуск всех примеров run_in_executor"""
    print("=" * 70)
    print("ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ loop.run_in_executor()")
    print("=" * 70)
    
    print("\n1. Базовый пример - ThreadPoolExecutor:")
    print("-" * 70)
    await basic_thread_pool_example()
    
    print("\n2. Базовый пример - ProcessPoolExecutor:")
    print("-" * 70)
    await basic_process_pool_example()
    
    print("\n3. Default executor:")
    print("-" * 70)
    await default_executor_example()
    
    print("\n4. Сравнение производительности:")
    print("-" * 70)
    await performance_comparison()
    
    print("\n5. Параллельная обработка файлов:")
    print("-" * 70)
    await parallel_file_processing()
    
    print("\n6. Параллельные запросы к БД:")
    print("-" * 70)
    await parallel_db_queries()
    
    print("\n7. Умный менеджер executor'ов:")
    print("-" * 70)
    await smart_executor_example()
    
    print("\n8. Выполнение с таймаутом:")
    print("-" * 70)
    await executor_with_timeout()
    
    print("\n9. Обработка ошибок:")
    print("-" * 70)
    await error_handling_in_executor()
    
    print("\n" + "=" * 70)
    print("ВСЕ ПРИМЕРЫ ЗАВЕРШЕНЫ")
    print("=" * 70)


# ============================================================================
# ИНФОРМАЦИЯ ДЛЯ ИНТЕРВЬЮ
# ============================================================================

def print_interview_tips():
    """Важные моменты для интервью"""
    print("\n" + "=" * 70)
    print("ВАЖНЫЕ МОМЕНТЫ ДЛЯ ИНТЕРВЬЮ - run_in_executor()")
    print("=" * 70)
    
    tips = """
    1. КОГДА ИСПОЛЬЗОВАТЬ:
       • Для запуска блокирующего кода в асинхронном контексте
       • Когда нужно интегрировать legacy синхронный код
       • Для I/O операций: чтение файлов, БД запросы, сетевые вызовы
       • Для CPU-intensive задач: вычисления, обработка данных
    
    2. ThreadPoolExecutor vs ProcessPoolExecutor:
       • ThreadPoolExecutor:
         - Для I/O-bound операций
         - Меньше overhead
         - Общая память (осторожно с GIL!)
       
       • ProcessPoolExecutor:
         - Для CPU-bound операций
         - Обход GIL
         - Больше overhead (сериализация данных)
    
    3. DEFAULT EXECUTOR:
       • Когда executor=None, используется ThreadPoolExecutor
       • Создается автоматически event loop'ом
       • Ограниченное количество потоков (обычно 5)
    
    4. BEST PRACTICES:
       • Всегда используйте context manager (with) для executor'ов
       • Ограничивайте количество одновременных задач
       • Используйте таймауты для долгих операций
       • Обрабатывайте исключения из executor'ов
       • Правильно завершайте executor'ы (.shutdown())
    
    5. ТИПИЧНЫЕ ОШИБКИ:
       • Запуск async функций в executor (используйте sync функции!)
       • Слишком много одновременных задач
       • Забывание про GIL при использовании ThreadPool для CPU
       • Не обработка исключений
       • Утечки ресурсов (не закрытые executor'ы)
    
    6. ПРОИЗВОДИТЕЛЬНОСТЬ:
       • ThreadPool: быстрый старт, подходит для I/O
       • ProcessPool: медленный старт, подходит для CPU
       • Default executor: удобно для простых случаев
       • Семафоры: контроль конкурентности
    
    7. ИНТЕГРАЦИЯ:
       • Можно комбинировать с asyncio.gather()
       • Можно использовать с asyncio.wait()
       • Работает с таймаутами (asyncio.wait_for)
       • Совместим с семафорами и другими примитивами
    """
    
    print(tips)
    print("=" * 70)


if __name__ == "__main__":
    # Запуск всех примеров
    asyncio.run(run_all_executor_examples())
    
    # Вывод советов для интервью
    print_interview_tips()

