"""
Продвинутые примеры для тестирования
"""

import time
import asyncio
from typing import List, Dict, Optional


class Database:
    """Имитация базы данных"""
    
    def __init__(self):
        self.connected = False
        self.data = {}
    
    def connect(self):
        """Подключение к базе данных"""
        self.connected = True
        return self
    
    def disconnect(self):
        """Отключение от базы данных"""
        self.connected = False
    
    def insert(self, table: str, record: dict):
        """Вставка записи"""
        if not self.connected:
            raise RuntimeError("База данных не подключена")
        
        if table not in self.data:
            self.data[table] = []
        
        self.data[table].append(record)
    
    def select(self, table: str, filter_by: Optional[dict] = None):
        """Выборка записей"""
        if not self.connected:
            raise RuntimeError("База данных не подключена")
        
        if table not in self.data:
            return []
        
        if filter_by is None:
            return self.data[table]
        
        results = []
        for record in self.data[table]:
            match = all(record.get(k) == v for k, v in filter_by.items())
            if match:
                results.append(record)
        
        return results
    
    def clear(self):
        """Очистка всех данных"""
        self.data = {}


class Cache:
    """Простой кеш с TTL (time to live)"""
    
    def __init__(self, default_ttl: int = 60):
        self.storage = {}
        self.default_ttl = default_ttl
    
    def set(self, key: str, value: any, ttl: Optional[int] = None):
        """Сохранить значение в кеше"""
        ttl = ttl or self.default_ttl
        expiry = time.time() + ttl
        self.storage[key] = {'value': value, 'expiry': expiry}
    
    def get(self, key: str) -> Optional[any]:
        """Получить значение из кеша"""
        if key not in self.storage:
            return None
        
        item = self.storage[key]
        if time.time() > item['expiry']:
            del self.storage[key]
            return None
        
        return item['value']
    
    def delete(self, key: str):
        """Удалить значение из кеша"""
        if key in self.storage:
            del self.storage[key]
    
    def clear(self):
        """Очистить весь кеш"""
        self.storage = {}
    
    def size(self) -> int:
        """Получить размер кеша"""
        return len(self.storage)


class APIClient:
    """Клиент для работы с API"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    def fetch_user(self, user_id: int) -> dict:
        """Получить пользователя по ID"""
        # В реальности здесь был бы HTTP запрос
        # Для примера просто имитируем ответ
        return {
            'id': user_id,
            'name': f'User {user_id}',
            'email': f'user{user_id}@example.com'
        }
    
    def create_user(self, user_data: dict) -> dict:
        """Создать нового пользователя"""
        # Имитация создания пользователя
        return {
            'id': 123,
            **user_data,
            'created_at': '2025-01-01T00:00:00Z'
        }
    
    def update_user(self, user_id: int, user_data: dict) -> dict:
        """Обновить пользователя"""
        return {
            'id': user_id,
            **user_data,
            'updated_at': '2025-01-01T00:00:00Z'
        }


class EventManager:
    """Менеджер событий (паттерн Observer)"""
    
    def __init__(self):
        self.listeners = {}
    
    def subscribe(self, event_type: str, callback):
        """Подписаться на событие"""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback):
        """Отписаться от события"""
        if event_type in self.listeners:
            self.listeners[event_type].remove(callback)
    
    def emit(self, event_type: str, data=None):
        """Вызвать событие"""
        if event_type in self.listeners:
            for callback in self.listeners[event_type]:
                callback(data)


async def async_fetch_data(url: str, delay: float = 0.1) -> dict:
    """Асинхронная функция для получения данных"""
    await asyncio.sleep(delay)
    return {'url': url, 'status': 'success'}


async def async_process_batch(items: List[str]) -> List[dict]:
    """Асинхронная обработка списка элементов"""
    tasks = [async_fetch_data(item) for item in items]
    return await asyncio.gather(*tasks)


class FileProcessor:
    """Обработчик файлов"""
    
    def read_file(self, filepath: str) -> str:
        """Прочитать файл"""
        with open(filepath, 'r') as f:
            return f.read()
    
    def write_file(self, filepath: str, content: str):
        """Записать в файл"""
        with open(filepath, 'w') as f:
            f.write(content)
    
    def process_csv(self, filepath: str) -> List[dict]:
        """Обработать CSV файл"""
        # Упрощенная реализация
        content = self.read_file(filepath)
        lines = content.strip().split('\n')
        
        if not lines:
            return []
        
        headers = lines[0].split(',')
        results = []
        
        for line in lines[1:]:
            values = line.split(',')
            record = dict(zip(headers, values))
            results.append(record)
        
        return results


class RateLimiter:
    """Ограничитель частоты запросов"""
    
    def __init__(self, max_calls: int, time_window: int):
        """
        max_calls: максимальное количество вызовов
        time_window: временное окно в секундах
        """
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
    
    def is_allowed(self) -> bool:
        """Проверить, разрешен ли вызов"""
        now = time.time()
        
        # Удаляем старые вызовы
        self.calls = [call_time for call_time in self.calls 
                      if now - call_time < self.time_window]
        
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        
        return False
    
    def reset(self):
        """Сбросить счетчик"""
        self.calls = []


class Validator:
    """Валидатор данных"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Проверка email"""
        if not email or '@' not in email:
            return False
        
        parts = email.split('@')
        if len(parts) != 2:
            return False
        
        local, domain = parts
        if not local or not domain:
            return False
        
        if '.' not in domain:
            return False
        
        return True
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Проверка телефона (упрощенная)"""
        digits = ''.join(c for c in phone if c.isdigit())
        return len(digits) >= 10
    
    @staticmethod
    def validate_age(age: int) -> bool:
        """Проверка возраста"""
        return 0 <= age <= 150

