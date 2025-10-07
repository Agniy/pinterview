"""
Вопросы для интервью по asyncio
Структурированы по уровням сложности и темам
"""

# ============================================================================
# БАЗОВЫЕ ВОПРОСЫ
# ============================================================================

BASIC_QUESTIONS = {
    "1. Что такое asyncio и зачем он нужен?": {
        "question": "Объясните концепцию asyncio в Python. В каких случаях его использование оправдано?",
        "answer": """
asyncio - это библиотека для написания конкурентного кода с использованием async/await синтаксиса.

Основные преимущества:
- Неблокирующие I/O операции
- Эффективное использование ресурсов
- Простота написания конкурентного кода

Когда использовать:
- Много I/O операций (сеть, файлы, база данных)
- Нужна высокая производительность
- Много одновременных соединений

Когда НЕ использовать:
- CPU-intensive задачи
- Простые синхронные программы
- Критически важные системы, где простота важнее производительности
        """,
        "code_example": """
# Плохо - блокирующий код
def fetch_data():
    response = requests.get('https://api.example.com/data')  # Блокирует
    return response.json()

# Хорошо - асинхронный код
async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.example.com/data') as response:
            return await response.json()
        """
    },

    "2. Разница между async и await": {
        "question": "Объясните разницу между ключевыми словами async и await",
        "answer": """
async - ключевое слово для определения асинхронной функции
await - ключевое слово для ожидания результата асинхронной операции

async def - создает корутину (coroutine)
await - приостанавливает выполнение до завершения операции
        """,
        "code_example": """
# async создает корутину
async def my_function():
    return "Hello"

# await ожидает результат
async def main():
    result = await my_function()  # Ждем завершения
    print(result)

# Без await функция не выполнится
async def wrong():
    result = my_function()  # Получаем объект корутины, а не результат
    print(result)  # <coroutine object my_function at 0x...>
        """
    },

    "3. Что такое корутина?": {
        "question": "Что такое корутина и чем она отличается от обычной функции?",
        "answer": """
Корутина (coroutine) - это специальный тип функции, которая может быть приостановлена и возобновлена.

Отличия от обычной функции:
- Может быть приостановлена с помощью await
- Возвращает объект корутины, а не результат
- Выполняется только при вызове через await или asyncio.run()
- Может кооперативно передавать управление другим корутинам
        """,
        "code_example": """
import asyncio

# Обычная функция
def normal_function():
    return "Hello"

# Корутина
async def coroutine_function():
    await asyncio.sleep(1)  # Приостанавливается здесь
    return "Hello"

# Вызов обычной функции
result1 = normal_function()  # Сразу получаем результат

# Вызов корутины
result2 = coroutine_function()  # Получаем объект корутины
print(type(result2))  # <class 'coroutine'>

# Правильный вызов корутины
result3 = await coroutine_function()  # Получаем результат
        """
    },

    "4. Как запустить асинхронную функцию?": {
        "question": "Какие способы запуска асинхронных функций вы знаете?",
        "answer": """
Основные способы запуска:

1. asyncio.run() - для запуска из синхронного кода
2. await - для запуска из другой асинхронной функции
3. asyncio.create_task() - для создания задачи
4. asyncio.gather() - для параллельного выполнения
        """,
        "code_example": """
import asyncio

async def my_coroutine():
    await asyncio.sleep(1)
    return "Done"

# 1. asyncio.run() - точка входа
async def main():
    result = await my_coroutine()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())

# 2. await - из другой корутины
async def another_coroutine():
    result = await my_coroutine()
    return result

# 3. create_task() - создание задачи
async def with_task():
    task = asyncio.create_task(my_coroutine())
    result = await task
    return result

# 4. gather() - параллельное выполнение
async def parallel():
    tasks = [my_coroutine() for _ in range(3)]
    results = await asyncio.gather(*tasks)
    return results
        """
    },

    "5. Разница между asyncio.gather() и asyncio.wait()": {
        "question": "В чем разница между asyncio.gather() и asyncio.wait()?",
        "answer": """
asyncio.gather():
- Ждет завершения ВСЕХ задач
- Возвращает результаты в том же порядке
- Если одна задача падает с ошибкой, останавливает все
- Проще в использовании

asyncio.wait():
- Более гибкий контроль
- Может ждать по разным условиям (FIRST_COMPLETED, FIRST_EXCEPTION, ALL_COMPLETED)
- Возвращает два множества: done и pending
- Нужно вручную обрабатывать результаты
        """,
        "code_example": """
import asyncio

async def task(name, delay):
    await asyncio.sleep(delay)
    return f"Task {name} completed"

# asyncio.gather() - ждет все задачи
async def gather_example():
    results = await asyncio.gather(
        task("A", 1),
        task("B", 2),
        task("C", 1.5)
    )
    print(results)  # ['Task A completed', 'Task B completed', 'Task C completed']

# asyncio.wait() - более гибкий контроль
async def wait_example():
    tasks = [
        asyncio.create_task(task("A", 1)),
        asyncio.create_task(task("B", 2)),
        asyncio.create_task(task("C", 1.5))
    ]
    
    # Ждем завершения первой задачи
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    
    print(f"Завершено: {len(done)}")
    print(f"Ожидает: {len(pending)}")
    
    # Отменяем оставшиеся задачи
    for task in pending:
        task.cancel()
        """
    }
}

# ============================================================================
# СРЕДНИЕ ВОПРОСЫ
# ============================================================================

INTERMEDIATE_QUESTIONS = {
    "1. Обработка исключений в asyncio": {
        "question": "Как правильно обрабатывать исключения в асинхронном коде?",
        "answer": """
Исключения в asyncio обрабатываются так же, как в обычном Python, но есть особенности:

1. try/except работает с await
2. asyncio.gather() с return_exceptions=True не прерывает выполнение
3. Исключения в задачах нужно обрабатывать отдельно
4. CancelledError - специальное исключение для отмененных задач
        """,
        "code_example": """
import asyncio

async def risky_task(should_fail):
    await asyncio.sleep(0.5)
    if should_fail:
        raise ValueError("Something went wrong!")
    return "Success"

# 1. Обычная обработка исключений
async def basic_exception_handling():
    try:
        result = await risky_task(True)
        print(result)
    except ValueError as e:
        print(f"Caught exception: {e}")

# 2. gather() с return_exceptions=True
async def gather_with_exceptions():
    tasks = [
        risky_task(False),
        risky_task(True),
        risky_task(False)
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Task {i} failed: {result}")
        else:
            print(f"Task {i} succeeded: {result}")

# 3. Обработка CancelledError
async def cancellable_task():
    try:
        await asyncio.sleep(10)  # Долгая задача
        return "Completed"
    except asyncio.CancelledError:
        print("Task was cancelled")
        raise  # Важно переподнять исключение
        """
    },

    "2. Семафоры и ограничение конкурентности": {
        "question": "Что такое семафор в asyncio и зачем он нужен?",
        "answer": """
Семафор (Semaphore) - это примитив синхронизации, который ограничивает количество одновременных операций.

Используется для:
- Ограничения количества одновременных HTTP запросов
- Контроля доступа к ресурсам с ограниченной пропускной способностью
- Предотвращения перегрузки системы

Принцип работы:
- Семафор имеет счетчик
- acquire() уменьшает счетчик, release() увеличивает
- Если счетчик = 0, acquire() ждет освобождения
        """,
        "code_example": """
import asyncio

async def limited_operation(semaphore, task_id):
    async with semaphore:  # Автоматически acquire/release
        print(f"Task {task_id} started")
        await asyncio.sleep(1)  # Имитация работы
        print(f"Task {task_id} completed")

async def semaphore_example():
    # Максимум 3 одновременные операции
    semaphore = asyncio.Semaphore(3)
    
    tasks = [
        asyncio.create_task(limited_operation(semaphore, i))
        for i in range(10)
    ]
    
    await asyncio.gather(*tasks)

# Ручное управление семафором
async def manual_semaphore():
    semaphore = asyncio.Semaphore(2)
    
    await semaphore.acquire()  # Получаем разрешение
    try:
        # Выполняем работу
        await asyncio.sleep(1)
    finally:
        semaphore.release()  # Освобождаем разрешение
        """
    },

    "3. Event и Condition для координации": {
        "question": "Как использовать Event и Condition для координации задач?",
        "answer": """
Event - простой механизм уведомления:
- set() - устанавливает событие
- clear() - сбрасывает событие  
- wait() - ждет установки события

Condition - более сложный механизм с блокировкой:
- wait() - ждет уведомления
- notify() - уведомляет одну задачу
- notify_all() - уведомляет все задачи
- acquire()/release() - управление блокировкой
        """,
        "code_example": """
import asyncio

# Event - простое уведомление
async def waiter(event, task_id):
    print(f"Task {task_id} waiting for event")
    await event.wait()
    print(f"Task {task_id} received event!")

async def event_example():
    event = asyncio.Event()
    
    # Создаем задачи-ожидатели
    waiters = [asyncio.create_task(waiter(event, i)) for i in range(3)]
    
    await asyncio.sleep(1)
    print("Setting event!")
    event.set()  # Все ожидающие задачи получат уведомление
    
    await asyncio.gather(*waiters)

# Condition - более сложная координация
async def producer(condition, queue):
    for i in range(5):
        await asyncio.sleep(0.5)
        async with condition:
            queue.append(f"Item {i}")
            condition.notify()  # Уведомляем потребителя
            print(f"Produced: Item {i}")

async def consumer(condition, queue):
    while True:
        async with condition:
            while not queue:
                await condition.wait()  # Ждем уведомления
            
            item = queue.pop(0)
            print(f"Consumed: {item}")
            
            if item == "Item 4":  # Последний элемент
                break

async def condition_example():
    condition = asyncio.Condition()
    queue = []
    
    await asyncio.gather(
        producer(condition, queue),
        consumer(condition, queue)
    )
        """
    },

    "4. Асинхронные контекстные менеджеры": {
        "question": "Как создать и использовать асинхронные контекстные менеджеры?",
        "answer": """
Асинхронный контекстный менеджер реализует методы __aenter__ и __aexit__.

Используется для:
- Управления асинхронными ресурсами
- Автоматического закрытия соединений
- Обработки исключений в асинхронном коде

Синтаксис: async with
        """,
        "code_example": """
import asyncio
from contextlib import asynccontextmanager

# 1. Класс с __aenter__ и __aexit__
class AsyncResource:
    async def __aenter__(self):
        print("Acquiring resource")
        await asyncio.sleep(0.1)  # Имитация инициализации
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Releasing resource")
        await asyncio.sleep(0.1)  # Имитация очистки
        if exc_type is not None:
            print(f"Exception occurred: {exc_val}")
    
    async def do_work(self):
        print("Doing work")
        await asyncio.sleep(1)

# 2. Декоратор @asynccontextmanager
@asynccontextmanager
async def async_timer():
    start = asyncio.get_event_loop().time()
    print("Timer started")
    try:
        yield
    finally:
        end = asyncio.get_event_loop().time()
        print(f"Timer ended: {end - start:.2f}s")

# Использование
async def use_async_context_manager():
    async with AsyncResource() as resource:
        await resource.do_work()
    
    async with async_timer():
        await asyncio.sleep(1)
        """
    },

    "5. Асинхронные генераторы": {
        "question": "Что такое асинхронные генераторы и как их использовать?",
        "answer": """
Асинхронный генератор - это функция с yield, которая может быть приостановлена.

Особенности:
- Использует async def и yield
- Итерируется с async for
- Может содержать await внутри
- Полезен для потоковой обработки данных

Методы:
- __aiter__() - возвращает асинхронный итератор
- __anext__() - возвращает следующее значение
        """,
        "code_example": """
import asyncio

# Асинхронный генератор
async def async_range(n):
    for i in range(n):
        await asyncio.sleep(0.1)  # Имитация асинхронной операции
        yield i * i

# Использование с async for
async def use_async_generator():
    async for value in async_range(5):
        print(f"Received: {value}")

# Асинхронный генератор для чтения файла
async def read_file_async(filename):
    # Имитация асинхронного чтения файла
    lines = ["line1", "line2", "line3", "line4", "line5"]
    for line in lines:
        await asyncio.sleep(0.1)  # Имитация I/O
        yield line

async def process_file():
    async for line in read_file_async("data.txt"):
        print(f"Processing: {line}")

# Ручная итерация
async def manual_iteration():
    gen = async_range(3)
    try:
        while True:
            value = await gen.__anext__()
            print(f"Manual: {value}")
    except StopAsyncIteration:
        print("Generator exhausted")
        """
    }
}

# ============================================================================
# ПРОДВИНУТЫЕ ВОПРОСЫ
# ============================================================================

ADVANCED_QUESTIONS = {
    "1. Event Loop и его настройка": {
        "question": "Что такое Event Loop и как его настраивать?",
        "answer": """
Event Loop - это ядро asyncio, которое управляет выполнением корутин.

Основные функции:
- Планирование и выполнение корутин
- Обработка I/O операций
- Управление задачами и их приоритетами

Настройки:
- set_debug(True) - включение отладочного режима
- set_exception_handler() - обработчик исключений
- call_soon() - планирование синхронных функций
- call_later() - отложенный вызов
        """,
        "code_example": """
import asyncio
import sys

def custom_exception_handler(loop, context):
    print(f"Exception in event loop: {context}")

async def main():
    loop = asyncio.get_running_loop()
    
    # Настройка обработчика исключений
    loop.set_exception_handler(custom_exception_handler)
    
    # Включение отладочного режима
    loop.set_debug(True)
    
    # Планирование синхронной функции
    def sync_function():
        print("Synchronous function called")
    
    loop.call_soon(sync_function)
    
    # Отложенный вызов
    loop.call_later(1.0, sync_function)
    
    await asyncio.sleep(2)

# Создание кастомного event loop
async def custom_loop_example():
    # Получение текущего loop
    loop = asyncio.get_running_loop()
    
    # Информация о loop
    print(f"Loop: {loop}")
    print(f"Is running: {loop.is_running()}")
    print(f"Is closed: {loop.is_closed()}")
    
    # Планирование задач
    future = loop.create_future()
    loop.call_soon(future.set_result, "Hello")
    
    result = await future
    print(f"Future result: {result}")
        """
    },

    "2. Производительность и оптимизация": {
        "question": "Как оптимизировать производительность asyncio приложений?",
        "answer": """
Основные принципы оптимизации:

1. Избегать блокирующих операций
2. Правильно использовать пулы соединений
3. Ограничивать конкурентность семафорами
4. Использовать батчинг для I/O операций
5. Мониторить производительность
6. Настраивать размеры буферов

Проблемы производительности:
- Блокирующие вызовы в async функциях
- Слишком много одновременных задач
- Неэффективное использование памяти
- Неправильная обработка исключений
        """,
        "code_example": """
import asyncio
import time
import aiohttp
from concurrent.futures import ThreadPoolExecutor

# Плохо - блокирующий вызов в async функции
async def bad_example():
    # Это заблокирует event loop!
    time.sleep(1)  # Используйте await asyncio.sleep(1)
    return "done"

# Хорошо - неблокирующий вызов
async def good_example():
    await asyncio.sleep(1)  # Не блокирует event loop
    return "done"

# Оптимизация HTTP запросов с пулом соединений
async def optimized_http_requests():
    connector = aiohttp.TCPConnector(
        limit=100,  # Общий лимит соединений
        limit_per_host=30,  # Лимит на хост
        ttl_dns_cache=300,  # TTL DNS кэша
        use_dns_cache=True,
    )
    
    timeout = aiohttp.ClientTimeout(total=30)
    
    async with aiohttp.ClientSession(
        connector=connector,
        timeout=timeout
    ) as session:
        # Батчинг запросов
        urls = [f"https://httpbin.org/delay/1" for _ in range(10)]
        
        tasks = [
            session.get(url) for url in urls
        ]
        
        responses = await asyncio.gather(*tasks)
        return [await resp.json() for resp in responses]

# Использование ThreadPoolExecutor для CPU-intensive задач
async def cpu_intensive_with_threadpool():
    def cpu_task(n):
        # CPU-intensive операция
        return sum(i * i for i in range(n))
    
    loop = asyncio.get_running_loop()
    
    with ThreadPoolExecutor() as executor:
        # Выполняем в отдельном потоке
        result = await loop.run_in_executor(executor, cpu_task, 1000000)
        return result

# Мониторинг производительности
async def performance_monitoring():
    start_time = time.time()
    
    # Ваш код здесь
    await asyncio.sleep(1)
    
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f}s")
    
    # Мониторинг задач
    loop = asyncio.get_running_loop()
    print(f"Active tasks: {len(asyncio.all_tasks())}")
        """
    },

    "3. Паттерны проектирования": {
        "question": "Какие паттерны проектирования полезны в asyncio?",
        "answer": """
Основные паттерны для asyncio:

1. Producer-Consumer - для обработки очередей
2. Connection Pool - для управления соединениями
3. Circuit Breaker - для защиты от сбоев
4. Retry Pattern - для повторных попыток
5. Observer Pattern - для событий
6. Singleton - для глобальных ресурсов
7. Factory - для создания объектов
8. Decorator - для добавления функциональности

Каждый паттерн решает специфические проблемы асинхронного программирования.
        """,
        "code_example": """
import asyncio
from typing import Dict, List, Callable, Any
from dataclasses import dataclass
from enum import Enum

# 1. Singleton для глобального ресурса
class AsyncSingleton:
    _instance = None
    _lock = asyncio.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    async def initialize(self):
        async with self._lock:
            if not hasattr(self, '_initialized'):
                await asyncio.sleep(0.1)  # Инициализация
                self._initialized = True
    
    async def do_something(self):
        await self.initialize()
        return "Singleton work"

# 2. Factory для создания объектов
class AsyncObjectFactory:
    _creators: Dict[str, Callable] = {}
    
    @classmethod
    def register(cls, name: str, creator: Callable):
        cls._creators[name] = creator
    
    @classmethod
    async def create(cls, name: str, *args, **kwargs):
        if name not in cls._creators:
            raise ValueError(f"Unknown object type: {name}")
        return await cls._creators[name](*args, **kwargs)

# 3. Decorator для логирования
def async_logging(func):
    async def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args: {args}")
        try:
            result = await func(*args, **kwargs)
            print(f"{func.__name__} returned: {result}")
            return result
        except Exception as e:
            print(f"{func.__name__} raised: {e}")
            raise
    return wrapper

@async_logging
async def example_function(x, y):
    await asyncio.sleep(0.1)
    return x + y

# 4. Observer Pattern
class AsyncEventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._lock = asyncio.Lock()
    
    async def subscribe(self, event: str, callback: Callable):
        async with self._lock:
            if event not in self._subscribers:
                self._subscribers[event] = []
            self._subscribers[event].append(callback)
    
    async def publish(self, event: str, data: Any):
        async with self._lock:
            subscribers = self._subscribers.get(event, [])
        
        if subscribers:
            tasks = [callback(data) for callback in subscribers]
            await asyncio.gather(*tasks, return_exceptions=True)

# 5. Circuit Breaker
class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class AsyncCircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self._lock = asyncio.Lock()
    
    async def call(self, func: Callable, *args, **kwargs):
        async with self._lock:
            if self.state == CircuitState.OPEN:
                if time.time() - self.last_failure_time > self.recovery_timeout:
                    self.state = CircuitState.HALF_OPEN
                else:
                    raise Exception("Circuit breaker is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            await self._on_success()
            return result
        except Exception as e:
            await self._on_failure()
            raise e
    
    async def _on_success(self):
        async with self._lock:
            self.failure_count = 0
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
    
    async def _on_failure(self):
        async with self._lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
        """
    },

    "4. Отладка и мониторинг": {
        "question": "Как отлаживать и мониторить asyncio приложения?",
        "answer": """
Инструменты для отладки и мониторинга:

1. Встроенные инструменты:
   - asyncio.set_debug(True)
   - asyncio.get_event_loop().set_debug(True)
   - Логирование с asyncio

2. Внешние инструменты:
   - aiomonitor - мониторинг в реальном времени
   - asyncio-mqtt - для MQTT
   - prometheus_client - метрики

3. Профилирование:
   - cProfile с asyncio
   - py-spy для профилирования
   - memory_profiler для памяти

4. Логирование:
   - Структурированное логирование
   - Корреляция запросов
   - Трассировка выполнения
        """,
        "code_example": """
import asyncio
import logging
import time
from typing import Dict, Any
import functools

# Настройка логирования для asyncio
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Декоратор для трассировки
def async_trace(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        logger = logging.getLogger(func.__module__)
        
        logger.info(f"Starting {func.__name__}")
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"Completed {func.__name__} in {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Failed {func.__name__} after {duration:.2f}s: {e}")
            raise
    return wrapper

# Мониторинг задач
class TaskMonitor:
    def __init__(self):
        self.task_stats: Dict[str, Dict[str, Any]] = {}
        self._lock = asyncio.Lock()
    
    async def track_task(self, task_name: str):
        async with self._lock:
            if task_name not in self.task_stats:
                self.task_stats[task_name] = {
                    'count': 0,
                    'total_time': 0,
                    'errors': 0
                }
            
            self.task_stats[task_name]['count'] += 1
            return self.task_stats[task_name]
    
    async def record_success(self, task_name: str, duration: float):
        async with self._lock:
            if task_name in self.task_stats:
                self.task_stats[task_name]['total_time'] += duration
    
    async def record_error(self, task_name: str):
        async with self._lock:
            if task_name in self.task_stats:
                self.task_stats[task_name]['errors'] += 1
    
    async def get_stats(self) -> Dict[str, Dict[str, Any]]:
        async with self._lock:
            return self.task_stats.copy()

# Пример использования
monitor = TaskMonitor()

@async_trace
async def monitored_task(task_id: int):
    stats = await monitor.track_task('monitored_task')
    start_time = time.time()
    
    try:
        await asyncio.sleep(0.1)  # Имитация работы
        if task_id % 5 == 0:  # Имитация ошибки
            raise ValueError(f"Task {task_id} failed")
        
        duration = time.time() - start_time
        await monitor.record_success('monitored_task', duration)
        return f"Task {task_id} completed"
    
    except Exception as e:
        await monitor.record_error('monitored_task')
        raise

# Функция для отладки event loop
async def debug_event_loop():
    loop = asyncio.get_running_loop()
    
    # Включение отладочного режима
    loop.set_debug(True)
    
    # Настройка обработчика исключений
    def exception_handler(loop, context):
        print(f"Exception in event loop: {context}")
    
    loop.set_exception_handler(exception_handler)
    
    # Мониторинг активных задач
    async def monitor_tasks():
        while True:
            tasks = asyncio.all_tasks()
            print(f"Active tasks: {len(tasks)}")
            for task in tasks:
                print(f"  Task: {task.get_name()}, State: {task._state}")
            await asyncio.sleep(5)
    
    # Запуск мониторинга в фоне
    monitor_task = asyncio.create_task(monitor_tasks())
    
    try:
        # Ваш основной код здесь
        await asyncio.sleep(10)
    finally:
        monitor_task.cancel()
        try:
            await monitor_task
        except asyncio.CancelledError:
            pass

# Пример использования всех инструментов
async def comprehensive_monitoring_example():
    # Включение отладки
    asyncio.get_running_loop().set_debug(True)
    
    # Запуск задач с мониторингом
    tasks = [
        asyncio.create_task(monitored_task(i))
        for i in range(10)
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Получение статистики
    stats = await monitor.get_stats()
    print("Task Statistics:")
    for task_name, task_stats in stats.items():
        avg_time = task_stats['total_time'] / task_stats['count']
        error_rate = task_stats['errors'] / task_stats['count'] * 100
        print(f"  {task_name}: {task_stats['count']} calls, "
              f"avg {avg_time:.3f}s, {error_rate:.1f}% errors")
        """
    }
}

# ============================================================================
# ПРАКТИЧЕСКИЕ ЗАДАЧИ
# ============================================================================

PRACTICAL_TASKS = {
    "1. Асинхронный веб-скрапер": {
        "description": "Создайте асинхронный веб-скрапер с ограничением скорости",
        "requirements": [
            "Использовать aiohttp для HTTP запросов",
            "Ограничить количество одновременных запросов семафором",
            "Добавить обработку ошибок и повторные попытки",
            "Сохранить результаты в файл асинхронно"
        ],
        "hints": [
            "Используйте asyncio.Semaphore для ограничения конкурентности",
            "Примените декоратор @async_retry для повторных попыток",
            "Используйте aiofiles для асинхронной записи в файл"
        ]
    },

    "2. Асинхронный чат-сервер": {
        "description": "Реализуйте простой асинхронный чат-сервер",
        "requirements": [
            "Поддержка множественных клиентов",
            "Широковещательная рассылка сообщений",
            "Обработка отключений клиентов",
            "Команды для управления (join, leave, list)"
        ],
        "hints": [
            "Используйте asyncio.start_server()",
            "Храните клиентов в множестве (set)",
            "Используйте asyncio.Queue для сообщений",
            "Обрабатывайте исключения ConnectionResetError"
        ]
    },

    "3. Асинхронная очередь задач": {
        "description": "Создайте систему очередей задач с приоритетами",
        "requirements": [
            "Поддержка приоритетов задач",
            "Несколько воркеров для обработки",
            "Персистентность очереди",
            "Мониторинг состояния очереди"
        ],
        "hints": [
            "Используйте asyncio.PriorityQueue",
            "Реализуйте паттерн Producer-Consumer",
            "Добавьте метрики производительности",
            "Используйте asyncio.Event для координации"
        ]
    },

    "4. Асинхронный кэш с TTL": {
        "description": "Реализуйте распределенный кэш с временем жизни",
        "requirements": [
            "TTL для ключей",
            "Автоматическая очистка устаревших элементов",
            "Статистика попаданий/промахов",
            "Ограничение размера кэша"
        ],
        "hints": [
            "Используйте asyncio.Lock для thread-safety",
            "Реализуйте LRU eviction policy",
            "Добавьте фоновую задачу для очистки",
            "Используйте asyncio.Timer для TTL"
        ]
    }
}

# ============================================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С ВОПРОСАМИ
# ============================================================================

def get_question_by_level(level: str) -> Dict[str, Dict]:
    """Получить вопросы по уровню сложности"""
    levels = {
        "basic": BASIC_QUESTIONS,
        "intermediate": INTERMEDIATE_QUESTIONS,
        "advanced": ADVANCED_QUESTIONS
    }
    return levels.get(level, {})

def get_all_questions() -> Dict[str, Dict]:
    """Получить все вопросы"""
    all_questions = {}
    all_questions.update(BASIC_QUESTIONS)
    all_questions.update(INTERMEDIATE_QUESTIONS)
    all_questions.update(ADVANCED_QUESTIONS)
    return all_questions

def get_practical_tasks() -> Dict[str, Dict]:
    """Получить практические задачи"""
    return PRACTICAL_TASKS

def print_question(question_key: str, level: str = None):
    """Вывести вопрос с ответом"""
    if level:
        questions = get_question_by_level(level)
    else:
        questions = get_all_questions()
    
    if question_key not in questions:
        print(f"Вопрос '{question_key}' не найден")
        return
    
    question_data = questions[question_key]
    print(f"ВОПРОС: {question_data['question']}")
    print(f"ОТВЕТ: {question_data['answer']}")
    if 'code_example' in question_data:
        print(f"ПРИМЕР КОДА:\n{question_data['code_example']}")

def list_questions_by_level(level: str):
    """Вывести список вопросов по уровню"""
    questions = get_question_by_level(level)
    print(f"=== {level.upper()} QUESTIONS ===")
    for key, data in questions.items():
        print(f"{key}: {data['question']}")

if __name__ == "__main__":
    # Пример использования
    print("Доступные уровни: basic, intermediate, advanced")
    print("Доступные команды:")
    print("- list_questions_by_level('basic')")
    print("- print_question('1. Что такое asyncio и зачем он нужен?', 'basic')")
    print("- get_practical_tasks()")
    
    # Демонстрация
    list_questions_by_level("basic")
    print("\n" + "="*50 + "\n")
    print_question("1. Что такое asyncio и зачем он нужен?", "basic")
