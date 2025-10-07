"""
Продвинутые примеры asyncio для интервью
Демонстрирует сложные паттерны и техники
"""

import asyncio
import time
import random
from typing import List, Dict, Any, Optional, Callable, AsyncGenerator
from dataclasses import dataclass
from contextlib import asynccontextmanager
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 1. Асинхронный пул соединений
class ConnectionPool:
    """Пул асинхронных соединений"""
    
    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self._pool = asyncio.Queue(maxsize=max_connections)
        self._created_connections = 0
        self._lock = asyncio.Lock()
    
    async def _create_connection(self):
        """Создание нового соединения"""
        await asyncio.sleep(0.1)  # Имитация создания соединения
        connection_id = f"conn_{self._created_connections}"
        self._created_connections += 1
        logger.info(f"Создано соединение: {connection_id}")
        return connection_id
    
    async def get_connection(self):
        """Получение соединения из пула"""
        try:
            # Пытаемся получить существующее соединение
            connection = self._pool.get_nowait()
            logger.info(f"Получено существующее соединение: {connection}")
            return connection
        except asyncio.QueueEmpty:
            # Создаем новое соединение, если не превышен лимит
            async with self._lock:
                if self._created_connections < self.max_connections:
                    connection = await self._create_connection()
                    return connection
                else:
                    # Ждем освобождения соединения
                    logger.info("Ожидание освобождения соединения...")
                    connection = await self._pool.get()
                    logger.info(f"Получено освобожденное соединение: {connection}")
                    return connection
    
    async def return_connection(self, connection: str):
        """Возврат соединения в пул"""
        try:
            self._pool.put_nowait(connection)
            logger.info(f"Соединение возвращено в пул: {connection}")
        except asyncio.QueueFull:
            logger.warning(f"Пул переполнен, соединение закрыто: {connection}")


# 2. Асинхронный декоратор с повторными попытками
def async_retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Декоратор для повторных попыток выполнения асинхронных функций"""
    def decorator(func: Callable):
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        wait_time = delay * (backoff ** attempt)
                        logger.warning(f"Попытка {attempt + 1} неудачна: {e}. Повтор через {wait_time:.2f}с")
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(f"Все {max_attempts} попыток неудачны")
            
            raise last_exception
        return wrapper
    return decorator


@async_retry(max_attempts=3, delay=0.5)
async def unreliable_operation(success_rate: float = 0.3):
    """Ненадежная операция для демонстрации retry"""
    if random.random() < success_rate:
        return "Успех!"
    else:
        raise Exception("Временная ошибка")


# 3. Асинхронный паттерн Producer-Consumer
@dataclass
class Task:
    """Задача для обработки"""
    id: int
    data: str
    priority: int = 1


class AsyncTaskQueue:
    """Асинхронная очередь задач с приоритетами"""
    
    def __init__(self, max_size: int = 100):
        self._queue = asyncio.PriorityQueue(maxsize=max_size)
        self._consumers = []
        self._running = False
    
    async def put_task(self, task: Task):
        """Добавление задачи в очередь"""
        # Приоритет инвертирован (меньше = выше приоритет)
        await self._queue.put((task.priority, task.id, task))
        logger.info(f"Задача {task.id} добавлена в очередь")
    
    async def get_task(self) -> Task:
        """Получение задачи из очереди"""
        _, _, task = await self._queue.get()
        return task
    
    async def process_task(self, task: Task):
        """Обработка задачи"""
        logger.info(f"Обработка задачи {task.id}: {task.data}")
        await asyncio.sleep(random.uniform(0.1, 0.5))  # Имитация работы
        logger.info(f"Задача {task.id} обработана")
    
    async def consumer(self, consumer_id: int):
        """Потребитель задач"""
        logger.info(f"Запуск потребителя {consumer_id}")
        while self._running:
            try:
                task = await asyncio.wait_for(self.get_task(), timeout=1.0)
                await self.process_task(task)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Ошибка в потребителе {consumer_id}: {e}")
    
    async def start_consumers(self, num_consumers: int = 3):
        """Запуск потребителей"""
        self._running = True
        self._consumers = [
            asyncio.create_task(self.consumer(i))
            for i in range(num_consumers)
        ]
    
    async def stop_consumers(self):
        """Остановка потребителей"""
        self._running = False
        if self._consumers:
            await asyncio.gather(*self._consumers, return_exceptions=True)


# 4. Асинхронный кэш с TTL
class AsyncCache:
    """Асинхронный кэш с временем жизни"""
    
    def __init__(self):
        self._cache = {}
        self._timestamps = {}
        self._lock = asyncio.Lock()
    
    async def get(self, key: str, ttl: float = 60.0) -> Optional[Any]:
        """Получение значения из кэша"""
        async with self._lock:
            if key in self._cache:
                if time.time() - self._timestamps[key] < ttl:
                    logger.info(f"Кэш попадание для ключа: {key}")
                    return self._cache[key]
                else:
                    # Удаляем устаревший элемент
                    del self._cache[key]
                    del self._timestamps[key]
                    logger.info(f"Кэш промах (TTL истек) для ключа: {key}")
            else:
                logger.info(f"Кэш промах для ключа: {key}")
            return None
    
    async def set(self, key: str, value: Any):
        """Установка значения в кэш"""
        async with self._lock:
            self._cache[key] = value
            self._timestamps[key] = time.time()
            logger.info(f"Значение установлено в кэш для ключа: {key}")
    
    async def clear_expired(self):
        """Очистка устаревших элементов"""
        current_time = time.time()
        async with self._lock:
            expired_keys = [
                key for key, timestamp in self._timestamps.items()
                if current_time - timestamp > 60.0
            ]
            for key in expired_keys:
                del self._cache[key]
                del self._timestamps[key]
            if expired_keys:
                logger.info(f"Удалено {len(expired_keys)} устаревших элементов из кэша")


# 5. Асинхронный контекстный менеджер с таймаутом
@asynccontextmanager
async def timeout_context(timeout: float):
    """Контекстный менеджер с таймаутом"""
    task = asyncio.current_task()
    timeout_task = asyncio.create_task(asyncio.sleep(timeout))
    
    try:
        yield
    finally:
        timeout_task.cancel()
        try:
            await timeout_task
        except asyncio.CancelledError:
            pass


# 6. Асинхронный итератор с батчингом
class AsyncBatchIterator:
    """Асинхронный итератор, который группирует элементы в батчи"""
    
    def __init__(self, items: List[Any], batch_size: int = 10):
        self.items = items
        self.batch_size = batch_size
        self.index = 0
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.index >= len(self.items):
            raise StopAsyncIteration
        
        batch = self.items[self.index:self.index + self.batch_size]
        self.index += self.batch_size
        
        # Имитация асинхронной обработки батча
        await asyncio.sleep(0.1)
        return batch


# 7. Асинхронный паттерн Circuit Breaker
class CircuitBreaker:
    """Circuit Breaker для защиты от каскадных сбоев"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self._lock = asyncio.Lock()
    
    async def call(self, func: Callable, *args, **kwargs):
        """Вызов функции через Circuit Breaker"""
        async with self._lock:
            if self.state == "OPEN":
                if time.time() - self.last_failure_time > self.recovery_timeout:
                    self.state = "HALF_OPEN"
                    logger.info("Circuit Breaker переходит в состояние HALF_OPEN")
                else:
                    raise Exception("Circuit Breaker OPEN - вызов заблокирован")
        
        try:
            result = await func(*args, **kwargs)
            await self._on_success()
            return result
        except Exception as e:
            await self._on_failure()
            raise e
    
    async def _on_success(self):
        """Обработка успешного вызова"""
        async with self._lock:
            self.failure_count = 0
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                logger.info("Circuit Breaker переходит в состояние CLOSED")
    
    async def _on_failure(self):
        """Обработка неудачного вызова"""
        async with self._lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                logger.warning("Circuit Breaker переходит в состояние OPEN")


# 8. Асинхронный паттерн Observer
class AsyncEventBus:
    """Асинхронная шина событий"""
    
    def __init__(self):
        self._subscribers = {}
        self._lock = asyncio.Lock()
    
    async def subscribe(self, event_type: str, callback: Callable):
        """Подписка на событие"""
        async with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(callback)
            logger.info(f"Добавлен подписчик на событие: {event_type}")
    
    async def unsubscribe(self, event_type: str, callback: Callable):
        """Отписка от события"""
        async with self._lock:
            if event_type in self._subscribers:
                try:
                    self._subscribers[event_type].remove(callback)
                    logger.info(f"Удален подписчик от события: {event_type}")
                except ValueError:
                    pass
    
    async def publish(self, event_type: str, data: Any):
        """Публикация события"""
        async with self._lock:
            subscribers = self._subscribers.get(event_type, [])
        
        if subscribers:
            logger.info(f"Публикация события {event_type} для {len(subscribers)} подписчиков")
            tasks = [callback(data) for callback in subscribers]
            await asyncio.gather(*tasks, return_exceptions=True)
        else:
            logger.info(f"Нет подписчиков на событие: {event_type}")


# Примеры использования продвинутых паттернов
async def connection_pool_example():
    """Демонстрация пула соединений"""
    pool = ConnectionPool(max_connections=3)
    
    async def use_connection(connection_id: str):
        connection = await pool.get_connection()
        logger.info(f"Использование соединения {connection} для задачи {connection_id}")
        await asyncio.sleep(0.5)  # Имитация работы
        await pool.return_connection(connection)
    
    tasks = [asyncio.create_task(use_connection(f"task_{i}")) for i in range(10)]
    await asyncio.gather(*tasks)


async def task_queue_example():
    """Демонстрация очереди задач"""
    queue = AsyncTaskQueue(max_size=50)
    
    # Запускаем потребителей
    await queue.start_consumers(num_consumers=2)
    
    # Добавляем задачи
    for i in range(20):
        priority = random.randint(1, 5)
        task = Task(id=i, data=f"Данные задачи {i}", priority=priority)
        await queue.put_task(task)
        await asyncio.sleep(0.1)
    
    # Ждем обработки всех задач
    await asyncio.sleep(5)
    await queue.stop_consumers()


async def cache_example():
    """Демонстрация асинхронного кэша"""
    cache = AsyncCache()
    
    async def expensive_operation(key: str):
        """Дорогая операция"""
        await asyncio.sleep(1)  # Имитация долгой операции
        return f"Результат для {key}"
    
    async def get_cached_data(key: str):
        """Получение данных с кэшированием"""
        # Проверяем кэш
        cached_value = await cache.get(key)
        if cached_value is not None:
            return cached_value
        
        # Выполняем дорогую операцию
        value = await expensive_operation(key)
        await cache.set(key, value)
        return value
    
    # Первый вызов - кэш промах
    start_time = time.time()
    result1 = await get_cached_data("test_key")
    first_call_time = time.time() - start_time
    
    # Второй вызов - кэш попадание
    start_time = time.time()
    result2 = await get_cached_data("test_key")
    second_call_time = time.time() - start_time
    
    logger.info(f"Первый вызов: {first_call_time:.2f}с")
    logger.info(f"Второй вызов: {second_call_time:.2f}с")
    logger.info(f"Ускорение: {first_call_time/second_call_time:.1f}x")


async def circuit_breaker_example():
    """Демонстрация Circuit Breaker"""
    breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=5.0)
    
    async def unreliable_service():
        if random.random() < 0.7:  # 70% вероятность ошибки
            raise Exception("Сервис недоступен")
        return "Успешный ответ"
    
    # Попытки вызова через Circuit Breaker
    for i in range(10):
        try:
            result = await breaker.call(unreliable_service)
            logger.info(f"Вызов {i+1}: {result}")
        except Exception as e:
            logger.error(f"Вызов {i+1}: {e}")
        await asyncio.sleep(1)


async def event_bus_example():
    """Демонстрация шины событий"""
    event_bus = AsyncEventBus()
    
    async def user_created_handler(data):
        logger.info(f"Обработчик создания пользователя: {data}")
        await asyncio.sleep(0.1)
    
    async def user_updated_handler(data):
        logger.info(f"Обработчик обновления пользователя: {data}")
        await asyncio.sleep(0.1)
    
    # Подписываемся на события
    await event_bus.subscribe("user.created", user_created_handler)
    await event_bus.subscribe("user.updated", user_updated_handler)
    
    # Публикуем события
    await event_bus.publish("user.created", {"user_id": 1, "name": "John"})
    await event_bus.publish("user.updated", {"user_id": 1, "name": "John Doe"})


async def batch_iterator_example():
    """Демонстрация батчевого итератора"""
    items = list(range(25))  # 25 элементов
    
    async for batch in AsyncBatchIterator(items, batch_size=5):
        logger.info(f"Обработка батча: {batch}")


# Функция для запуска всех продвинутых примеров
async def run_advanced_examples():
    """Запуск всех продвинутых примеров"""
    print("=== Продвинутые примеры asyncio ===\n")
    
    print("1. Пул соединений:")
    await connection_pool_example()
    print()
    
    print("2. Очередь задач:")
    await task_queue_example()
    print()
    
    print("3. Асинхронный кэш:")
    await cache_example()
    print()
    
    print("4. Retry декоратор:")
    try:
        result = await unreliable_operation(success_rate=0.2)
        logger.info(f"Результат: {result}")
    except Exception as e:
        logger.error(f"Все попытки неудачны: {e}")
    print()
    
    print("5. Circuit Breaker:")
    await circuit_breaker_example()
    print()
    
    print("6. Шина событий:")
    await event_bus_example()
    print()
    
    print("7. Батчевый итератор:")
    await batch_iterator_example()
    print()


if __name__ == "__main__":
    # Запуск всех продвинутых примеров
    asyncio.run(run_advanced_examples())
