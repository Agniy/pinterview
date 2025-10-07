"""
Практические задачи по asyncio для интервью
Реализации различных паттернов и решений
"""

import asyncio
import aiohttp
import aiofiles
import time
import json
import random
from typing import List, Dict, Any, Optional, Callable, Set
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from contextlib import asynccontextmanager

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# ЗАДАЧА 1: АСИНХРОННЫЙ ВЕБ-СКРАПЕР
# ============================================================================

@dataclass
class ScrapedData:
    """Структура данных для скрапинга"""
    url: str
    title: str
    content: str
    timestamp: float
    status_code: int


class AsyncWebScraper:
    """Асинхронный веб-скрапер с ограничением скорости"""
    
    def __init__(self, max_concurrent: int = 10, delay: float = 1.0):
        self.max_concurrent = max_concurrent
        self.delay = delay
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.session = None
        self.results = []
        self.errors = []
    
    async def __aenter__(self):
        """Асинхронный контекстный менеджер - вход"""
        connector = aiohttp.TCPConnector(
            limit=100,
            limit_per_host=30,
            ttl_dns_cache=300
        )
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Асинхронный контекстный менеджер - выход"""
        if self.session:
            await self.session.close()
    
    async def scrape_url(self, url: str) -> Optional[ScrapedData]:
        """Скрапинг одного URL с повторными попытками"""
        async with self.semaphore:
            for attempt in range(3):  # 3 попытки
                try:
                    await asyncio.sleep(self.delay)  # Ограничение скорости
                    
                    async with self.session.get(url) as response:
                        if response.status == 200:
                            text = await response.text()
                            # Простое извлечение заголовка
                            title = self._extract_title(text)
                            content = self._extract_content(text)
                            
                            return ScrapedData(
                                url=url,
                                title=title,
                                content=content,
                                timestamp=time.time(),
                                status_code=response.status
                            )
                        else:
                            logger.warning(f"HTTP {response.status} for {url}")
                            
                except Exception as e:
                    logger.error(f"Attempt {attempt + 1} failed for {url}: {e}")
                    if attempt == 2:  # Последняя попытка
                        self.errors.append({"url": url, "error": str(e)})
                    else:
                        await asyncio.sleep(2 ** attempt)  # Exponential backoff
            
            return None
    
    def _extract_title(self, html: str) -> str:
        """Извлечение заголовка из HTML"""
        import re
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        return title_match.group(1) if title_match else "No title"
    
    def _extract_content(self, html: str) -> str:
        """Извлечение контента из HTML"""
        import re
        # Удаляем HTML теги
        content = re.sub(r'<[^>]+>', '', html)
        # Берем первые 500 символов
        return content.strip()[:500]
    
    async def scrape_urls(self, urls: List[str]) -> List[ScrapedData]:
        """Скрапинг множества URL"""
        logger.info(f"Starting to scrape {len(urls)} URLs")
        
        tasks = [self.scrape_url(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Фильтруем успешные результаты
        successful_results = [
            result for result in results 
            if isinstance(result, ScrapedData)
        ]
        
        logger.info(f"Successfully scraped {len(successful_results)} URLs")
        logger.info(f"Errors: {len(self.errors)}")
        
        return successful_results
    
    async def save_results(self, filename: str, results: List[ScrapedData]):
        """Асинхронное сохранение результатов"""
        async with aiofiles.open(filename, 'w', encoding='utf-8') as f:
            data = {
                'results': [asdict(result) for result in results],
                'errors': self.errors,
                'summary': {
                    'total_urls': len(results) + len(self.errors),
                    'successful': len(results),
                    'failed': len(self.errors)
                }
            }
            await f.write(json.dumps(data, indent=2, ensure_ascii=False))


# ============================================================================
# ЗАДАЧА 2: АСИНХРОННЫЙ ЧАТ-СЕРВЕР
# ============================================================================

@dataclass
class ChatMessage:
    """Сообщение в чате"""
    sender: str
    content: str
    timestamp: float
    message_type: str = "message"  # message, system, command


class ChatClient:
    """Клиент чата"""
    
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.reader = reader
        self.writer = writer
        self.username = None
        self.address = writer.get_extra_info('peername')
    
    async def send_message(self, message: str):
        """Отправка сообщения клиенту"""
        try:
            self.writer.write(f"{message}\n".encode())
            await self.writer.drain()
        except Exception as e:
            logger.error(f"Error sending message to {self.username}: {e}")
    
    async def receive_message(self) -> Optional[str]:
        """Получение сообщения от клиента"""
        try:
            data = await self.reader.readline()
            return data.decode().strip()
        except Exception as e:
            logger.error(f"Error receiving message from {self.username}: {e}")
            return None
    
    def close(self):
        """Закрытие соединения"""
        if self.writer:
            self.writer.close()


class AsyncChatServer:
    """Асинхронный чат-сервер"""
    
    def __init__(self, host: str = 'localhost', port: int = 8888):
        self.host = host
        self.port = port
        self.clients: Set[ChatClient] = set()
        self.message_queue = asyncio.Queue()
        self.running = False
    
    async def handle_client(self, client: ChatClient):
        """Обработка клиента"""
        try:
            # Получение имени пользователя
            await client.send_message("Введите ваше имя:")
            username = await client.receive_message()
            if not username:
                return
            
            client.username = username
            self.clients.add(client)
            
            # Уведомление о подключении
            await self.broadcast_message(
                f"{username} присоединился к чату",
                sender="system"
            )
            
            logger.info(f"Client {username} connected from {client.address}")
            
            # Обработка сообщений
            while self.running:
                message = await client.receive_message()
                if not message:
                    break
                
                # Обработка команд
                if message.startswith('/'):
                    await self.handle_command(client, message)
                else:
                    # Обычное сообщение
                    chat_message = ChatMessage(
                        sender=username,
                        content=message,
                        timestamp=time.time()
                    )
                    await self.broadcast_message(
                        f"{username}: {message}",
                        sender=username
                    )
        
        except Exception as e:
            logger.error(f"Error handling client {client.username}: {e}")
        
        finally:
            # Отключение клиента
            if client.username:
                self.clients.discard(client)
                await self.broadcast_message(
                    f"{client.username} покинул чат",
                    sender="system"
                )
                logger.info(f"Client {client.username} disconnected")
            
            client.close()
    
    async def handle_command(self, client: ChatClient, command: str):
        """Обработка команд"""
        cmd_parts = command[1:].split()
        cmd = cmd_parts[0].lower() if cmd_parts else ""
        
        if cmd == "list":
            # Список пользователей
            usernames = [c.username for c in self.clients if c.username]
            await client.send_message(f"Пользователи онлайн: {', '.join(usernames)}")
        
        elif cmd == "help":
            # Справка
            help_text = """
Доступные команды:
/list - список пользователей онлайн
/help - эта справка
/quit - выход из чата
            """
            await client.send_message(help_text)
        
        elif cmd == "quit":
            # Выход
            await client.send_message("До свидания!")
            return
        
        else:
            await client.send_message(f"Неизвестная команда: {cmd}")
    
    async def broadcast_message(self, message: str, sender: str = "system"):
        """Широковещательная рассылка сообщения"""
        if not self.clients:
            return
        
        # Создаем задачи для отправки всем клиентам
        tasks = []
        for client in self.clients.copy():  # Копируем для безопасности
            if client.username != sender:  # Не отправляем отправителю
                tasks.append(client.send_message(message))
        
        if tasks:
            # Отправляем всем параллельно
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def start_server(self):
        """Запуск сервера"""
        self.running = True
        
        server = await asyncio.start_server(
            self.handle_client,
            self.host,
            self.port
        )
        
        logger.info(f"Chat server started on {self.host}:{self.port}")
        
        async with server:
            await server.serve_forever()
    
    async def stop_server(self):
        """Остановка сервера"""
        self.running = False
        
        # Уведомляем всех клиентов
        await self.broadcast_message("Сервер останавливается", "system")
        
        # Закрываем все соединения
        for client in self.clients.copy():
            client.close()
        
        logger.info("Chat server stopped")


# ============================================================================
# ЗАДАЧА 3: АСИНХРОННАЯ ОЧЕРЕДЬ ЗАДАЧ
# ============================================================================

class TaskPriority(Enum):
    """Приоритеты задач"""
    LOW = 3
    MEDIUM = 2
    HIGH = 1
    CRITICAL = 0


@dataclass
class Task:
    """Задача для обработки"""
    id: str
    data: Dict[str, Any]
    priority: TaskPriority
    created_at: float
    max_retries: int = 3
    retry_count: int = 0


class AsyncTaskQueue:
    """Асинхронная очередь задач с приоритетами"""
    
    def __init__(self, max_size: int = 1000):
        self.queue = asyncio.PriorityQueue(maxsize=max_size)
        self.workers = []
        self.running = False
        self.processed_tasks = 0
        self.failed_tasks = 0
        self.stats = {
            'total_processed': 0,
            'total_failed': 0,
            'queue_size': 0,
            'active_workers': 0
        }
    
    async def add_task(self, task: Task):
        """Добавление задачи в очередь"""
        try:
            # Приоритет = (приоритет, время создания) для стабильной сортировки
            priority_tuple = (task.priority.value, task.created_at, task.id)
            await self.queue.put((priority_tuple, task))
            logger.info(f"Task {task.id} added to queue with priority {task.priority.name}")
        except asyncio.QueueFull:
            logger.error(f"Queue is full, cannot add task {task.id}")
            raise
    
    async def get_task(self) -> Task:
        """Получение задачи из очереди"""
        _, task = await self.queue.get()
        return task
    
    async def process_task(self, task: Task) -> bool:
        """Обработка задачи (переопределить в наследниках)"""
        # Имитация обработки
        await asyncio.sleep(random.uniform(0.1, 1.0))
        
        # Имитация случайных ошибок
        if random.random() < 0.1:  # 10% вероятность ошибки
            raise Exception(f"Random error in task {task.id}")
        
        logger.info(f"Task {task.id} processed successfully")
        return True
    
    async def worker(self, worker_id: int):
        """Воркер для обработки задач"""
        logger.info(f"Worker {worker_id} started")
        
        while self.running:
            try:
                # Получаем задачу с таймаутом
                task = await asyncio.wait_for(self.get_task(), timeout=1.0)
                
                try:
                    # Обрабатываем задачу
                    success = await self.process_task(task)
                    if success:
                        self.processed_tasks += 1
                        self.stats['total_processed'] += 1
                    else:
                        await self._handle_task_failure(task)
                
                except Exception as e:
                    logger.error(f"Error processing task {task.id}: {e}")
                    await self._handle_task_failure(task)
            
            except asyncio.TimeoutError:
                # Таймаут - продолжаем работу
                continue
            
            except Exception as e:
                logger.error(f"Worker {worker_id} error: {e}")
        
        logger.info(f"Worker {worker_id} stopped")
    
    async def _handle_task_failure(self, task: Task):
        """Обработка неудачной задачи"""
        task.retry_count += 1
        
        if task.retry_count < task.max_retries:
            # Повторная попытка
            logger.info(f"Retrying task {task.id} (attempt {task.retry_count + 1})")
            await asyncio.sleep(2 ** task.retry_count)  # Exponential backoff
            await self.add_task(task)
        else:
            # Задача провалилась окончательно
            logger.error(f"Task {task.id} failed after {task.max_retries} attempts")
            self.failed_tasks += 1
            self.stats['total_failed'] += 1
    
    async def start_workers(self, num_workers: int = 3):
        """Запуск воркеров"""
        self.running = True
        self.workers = [
            asyncio.create_task(self.worker(i))
            for i in range(num_workers)
        ]
        self.stats['active_workers'] = num_workers
        logger.info(f"Started {num_workers} workers")
    
    async def stop_workers(self):
        """Остановка воркеров"""
        self.running = False
        
        if self.workers:
            await asyncio.gather(*self.workers, return_exceptions=True)
            self.workers = []
            self.stats['active_workers'] = 0
        
        logger.info("All workers stopped")
    
    async def get_stats(self) -> Dict[str, Any]:
        """Получение статистики"""
        self.stats.update({
            'queue_size': self.queue.qsize(),
            'processed_tasks': self.processed_tasks,
            'failed_tasks': self.failed_tasks
        })
        return self.stats.copy()
    
    async def clear_queue(self):
        """Очистка очереди"""
        while not self.queue.empty():
            try:
                self.queue.get_nowait()
            except asyncio.QueueEmpty:
                break
        logger.info("Queue cleared")


# ============================================================================
# ЗАДАЧА 4: АСИНХРОННЫЙ КЭШ С TTL
# ============================================================================

@dataclass
class CacheEntry:
    """Запись в кэше"""
    key: str
    value: Any
    created_at: float
    ttl: float
    access_count: int = 0
    last_accessed: float = 0
    
    def is_expired(self) -> bool:
        """Проверка истечения TTL"""
        return time.time() - self.created_at > self.ttl
    
    def touch(self):
        """Обновление времени последнего доступа"""
        self.access_count += 1
        self.last_accessed = time.time()


class AsyncTTLCache:
    """Асинхронный кэш с TTL и LRU eviction"""
    
    def __init__(self, max_size: int = 1000, default_ttl: float = 3600):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = asyncio.Lock()
        self._cleanup_task = None
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'size': 0
        }
    
    async def get(self, key: str) -> Optional[Any]:
        """Получение значения из кэша"""
        async with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                
                if entry.is_expired():
                    # Удаляем устаревшую запись
                    del self._cache[key]
                    self.stats['misses'] += 1
                    logger.debug(f"Cache miss (expired): {key}")
                    return None
                
                # Обновляем статистику доступа
                entry.touch()
                self.stats['hits'] += 1
                logger.debug(f"Cache hit: {key}")
                return entry.value
            
            self.stats['misses'] += 1
            logger.debug(f"Cache miss: {key}")
            return None
    
    async def set(self, key: str, value: Any, ttl: Optional[float] = None):
        """Установка значения в кэш"""
        async with self._lock:
            ttl = ttl or self.default_ttl
            current_time = time.time()
            
            # Создаем новую запись
            entry = CacheEntry(
                key=key,
                value=value,
                created_at=current_time,
                ttl=ttl,
                last_accessed=current_time
            )
            
            # Проверяем, нужно ли освободить место
            if len(self._cache) >= self.max_size and key not in self._cache:
                await self._evict_lru()
            
            self._cache[key] = entry
            self.stats['size'] = len(self._cache)
            logger.debug(f"Cache set: {key}")
    
    async def delete(self, key: str) -> bool:
        """Удаление значения из кэша"""
        async with self._lock:
            if key in self._cache:
                del self._cache[key]
                self.stats['size'] = len(self._cache)
                logger.debug(f"Cache delete: {key}")
                return True
            return False
    
    async def clear(self):
        """Очистка кэша"""
        async with self._lock:
            self._cache.clear()
            self.stats['size'] = 0
            logger.info("Cache cleared")
    
    async def _evict_lru(self):
        """Удаление наименее используемого элемента"""
        if not self._cache:
            return
        
        # Находим элемент с наименьшим last_accessed
        lru_key = min(
            self._cache.keys(),
            key=lambda k: self._cache[k].last_accessed
        )
        
        del self._cache[lru_key]
        self.stats['evictions'] += 1
        logger.debug(f"LRU eviction: {lru_key}")
    
    async def cleanup_expired(self):
        """Очистка устаревших элементов"""
        async with self._lock:
            expired_keys = [
                key for key, entry in self._cache.items()
                if entry.is_expired()
            ]
            
            for key in expired_keys:
                del self._cache[key]
            
            if expired_keys:
                self.stats['size'] = len(self._cache)
                logger.info(f"Cleaned up {len(expired_keys)} expired entries")
    
    async def start_cleanup_task(self, interval: float = 60.0):
        """Запуск фоновой задачи очистки"""
        async def cleanup_loop():
            while True:
                try:
                    await asyncio.sleep(interval)
                    await self.cleanup_expired()
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.error(f"Error in cleanup task: {e}")
        
        self._cleanup_task = asyncio.create_task(cleanup_loop())
        logger.info(f"Cleanup task started with interval {interval}s")
    
    async def stop_cleanup_task(self):
        """Остановка фоновой задачи очистки"""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
            self._cleanup_task = None
            logger.info("Cleanup task stopped")
    
    async def get_stats(self) -> Dict[str, Any]:
        """Получение статистики кэша"""
        async with self._lock:
            total_requests = self.stats['hits'] + self.stats['misses']
            hit_rate = (self.stats['hits'] / total_requests * 100) if total_requests > 0 else 0
            
            return {
                **self.stats,
                'hit_rate': round(hit_rate, 2),
                'total_requests': total_requests
            }
    
    async def get_keys(self) -> List[str]:
        """Получение списка ключей"""
        async with self._lock:
            return list(self._cache.keys())


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

async def web_scraper_example():
    """Пример использования веб-скрапера"""
    urls = [
        "https://httpbin.org/html",
        "https://httpbin.org/json",
        "https://httpbin.org/xml",
        "https://httpbin.org/robots.txt",
        "https://httpbin.org/user-agent"
    ]
    
    async with AsyncWebScraper(max_concurrent=3, delay=0.5) as scraper:
        results = await scraper.scrape_urls(urls)
        await scraper.save_results("scraped_data.json", results)
    
    print(f"Scraped {len(results)} URLs successfully")

async def chat_server_example():
    """Пример запуска чат-сервера"""
    server = AsyncChatServer(host='localhost', port=8888)
    
    try:
        await server.start_server()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        await server.stop_server()

async def task_queue_example():
    """Пример использования очереди задач"""
    queue = AsyncTaskQueue(max_size=100)
    
    # Запускаем воркеров
    await queue.start_workers(num_workers=2)
    
    # Добавляем задачи
    for i in range(20):
        priority = random.choice(list(TaskPriority))
        task = Task(
            id=f"task_{i}",
            data={"number": i, "message": f"Task {i} data"},
            priority=priority,
            created_at=time.time()
        )
        await queue.add_task(task)
        await asyncio.sleep(0.1)
    
    # Ждем обработки
    await asyncio.sleep(10)
    
    # Получаем статистику
    stats = await queue.get_stats()
    print(f"Task queue stats: {stats}")
    
    # Останавливаем воркеров
    await queue.stop_workers()

async def cache_example():
    """Пример использования кэша с TTL"""
    cache = AsyncTTLCache(max_size=10, default_ttl=5.0)
    
    # Запускаем очистку
    await cache.start_cleanup_task(interval=2.0)
    
    # Добавляем данные
    for i in range(15):
        await cache.set(f"key_{i}", f"value_{i}", ttl=3.0)
        await asyncio.sleep(0.1)
    
    # Читаем данные
    for i in range(15):
        value = await cache.get(f"key_{i}")
        print(f"key_{i}: {value}")
    
    # Ждем истечения TTL
    await asyncio.sleep(4)
    
    # Проверяем после истечения TTL
    print("\nAfter TTL expiration:")
    for i in range(15):
        value = await cache.get(f"key_{i}")
        print(f"key_{i}: {value}")
    
    # Получаем статистику
    stats = await cache.get_stats()
    print(f"\nCache stats: {stats}")
    
    # Останавливаем очистку
    await cache.stop_cleanup_task()

# ============================================================================
# ТЕСТИРОВАНИЕ
# ============================================================================

async def run_all_examples():
    """Запуск всех примеров"""
    print("=== Практические задачи asyncio ===\n")
    
    print("1. Веб-скрапер:")
    await web_scraper_example()
    print()
    
    print("2. Очередь задач:")
    await task_queue_example()
    print()
    
    print("3. Кэш с TTL:")
    await cache_example()
    print()
    
    print("4. Чат-сервер (запустите отдельно):")
    print("   python -c 'import asyncio; from practical_tasks import chat_server_example; asyncio.run(chat_server_example())'")
    print()

if __name__ == "__main__":
    # Запуск всех примеров
    asyncio.run(run_all_examples())
