"""
Продвинутые тесты, демонстрирующие:
- Работу с моками и патчами
- Асинхронное тестирование
- Тестирование баз данных
- Тестирование файловых операций
- Параметризацию фикстур
"""

import pytest
import asyncio
import time
from unittest.mock import Mock, MagicMock, patch, mock_open
from .advanced_examples import (
    Database, Cache, APIClient, EventManager,
    async_fetch_data, async_process_batch,
    FileProcessor, RateLimiter, Validator
)


# ============= Тесты базы данных =============

class TestDatabase:
    """Тесты для класса Database"""
    
    def test_connect_disconnect(self):
        """Тест подключения и отключения"""
        db = Database()
        assert db.connected is False
        
        db.connect()
        assert db.connected is True
        
        db.disconnect()
        assert db.connected is False
    
    def test_insert_without_connection(self):
        """Тест вставки без подключения"""
        db = Database()
        with pytest.raises(RuntimeError, match="не подключена"):
            db.insert('users', {'name': 'John'})
    
    def test_insert_and_select(self):
        """Тест вставки и выборки данных"""
        db = Database().connect()
        
        db.insert('users', {'id': 1, 'name': 'John'})
        db.insert('users', {'id': 2, 'name': 'Jane'})
        
        results = db.select('users')
        assert len(results) == 2
        assert results[0]['name'] == 'John'
    
    def test_select_with_filter(self):
        """Тест выборки с фильтром"""
        db = Database().connect()
        
        db.insert('users', {'id': 1, 'name': 'John', 'age': 25})
        db.insert('users', {'id': 2, 'name': 'Jane', 'age': 30})
        
        results = db.select('users', filter_by={'age': 30})
        assert len(results) == 1
        assert results[0]['name'] == 'Jane'
    
    def test_clear_data(self):
        """Тест очистки данных"""
        db = Database().connect()
        db.insert('users', {'id': 1, 'name': 'John'})
        
        db.clear()
        results = db.select('users')
        assert len(results) == 0


# ============= Тесты кеша =============

class TestCache:
    """Тесты для класса Cache"""
    
    def test_set_and_get(self):
        """Тест сохранения и получения значения"""
        cache = Cache()
        cache.set('key1', 'value1')
        
        assert cache.get('key1') == 'value1'
    
    def test_get_nonexistent_key(self):
        """Тест получения несуществующего ключа"""
        cache = Cache()
        assert cache.get('nonexistent') is None
    
    def test_expiry(self):
        """Тест истечения срока действия"""
        cache = Cache()
        cache.set('key1', 'value1', ttl=1)  # 1 секунда
        
        assert cache.get('key1') == 'value1'
        
        time.sleep(1.1)  # Ждем истечения TTL
        assert cache.get('key1') is None
    
    def test_delete(self):
        """Тест удаления ключа"""
        cache = Cache()
        cache.set('key1', 'value1')
        cache.delete('key1')
        
        assert cache.get('key1') is None
    
    def test_clear(self):
        """Тест очистки всего кеша"""
        cache = Cache()
        cache.set('key1', 'value1')
        cache.set('key2', 'value2')
        
        cache.clear()
        assert cache.size() == 0
    
    def test_size(self):
        """Тест размера кеша"""
        cache = Cache()
        assert cache.size() == 0
        
        cache.set('key1', 'value1')
        cache.set('key2', 'value2')
        assert cache.size() == 2


# ============= Тесты с моками =============

class TestAPIClient:
    """Тесты для APIClient с использованием моков"""
    
    def test_fetch_user(self):
        """Тест получения пользователя"""
        client = APIClient("https://api.example.com")
        user = client.fetch_user(1)
        
        assert user['id'] == 1
        assert 'name' in user
        assert 'email' in user
    
    @patch.object(APIClient, 'fetch_user')
    def test_fetch_user_with_mock(self, mock_fetch):
        """Тест с мокированием метода"""
        # Настраиваем мок
        mock_fetch.return_value = {
            'id': 99,
            'name': 'Mocked User',
            'email': 'mock@example.com'
        }
        
        client = APIClient("https://api.example.com")
        user = client.fetch_user(99)
        
        assert user['name'] == 'Mocked User'
        mock_fetch.assert_called_once_with(99)
    
    def test_create_user(self):
        """Тест создания пользователя"""
        client = APIClient("https://api.example.com")
        user_data = {'name': 'New User', 'email': 'new@example.com'}
        
        result = client.create_user(user_data)
        
        assert result['id'] == 123
        assert result['name'] == 'New User'
        assert 'created_at' in result


# ============= Тесты событий =============

class TestEventManager:
    """Тесты для EventManager"""
    
    def test_subscribe_and_emit(self):
        """Тест подписки и вызова события"""
        manager = EventManager()
        mock_callback = Mock()
        
        manager.subscribe('user_created', mock_callback)
        manager.emit('user_created', {'user_id': 1})
        
        mock_callback.assert_called_once_with({'user_id': 1})
    
    def test_multiple_listeners(self):
        """Тест нескольких слушателей"""
        manager = EventManager()
        callback1 = Mock()
        callback2 = Mock()
        
        manager.subscribe('event', callback1)
        manager.subscribe('event', callback2)
        manager.emit('event', 'data')
        
        callback1.assert_called_once_with('data')
        callback2.assert_called_once_with('data')
    
    def test_unsubscribe(self):
        """Тест отписки от события"""
        manager = EventManager()
        callback = Mock()
        
        manager.subscribe('event', callback)
        manager.unsubscribe('event', callback)
        manager.emit('event', 'data')
        
        callback.assert_not_called()


# ============= Асинхронные тесты =============

@pytest.mark.asyncio
async def test_async_fetch_data():
    """Тест асинхронной функции"""
    result = await async_fetch_data('https://example.com', delay=0.01)
    
    assert result['url'] == 'https://example.com'
    assert result['status'] == 'success'


@pytest.mark.asyncio
async def test_async_process_batch():
    """Тест асинхронной обработки списка"""
    urls = ['url1', 'url2', 'url3']
    results = await async_process_batch(urls)
    
    assert len(results) == 3
    assert all(r['status'] == 'success' for r in results)


# ============= Тесты файловых операций =============

class TestFileProcessor:
    """Тесты для FileProcessor с мокированием файловой системы"""
    
    def test_read_file(self):
        """Тест чтения файла"""
        processor = FileProcessor()
        
        # Мокируем функцию open
        with patch('builtins.open', mock_open(read_data='Hello, World!')):
            content = processor.read_file('test.txt')
            assert content == 'Hello, World!'
    
    def test_write_file(self):
        """Тест записи в файл"""
        processor = FileProcessor()
        
        m = mock_open()
        with patch('builtins.open', m):
            processor.write_file('test.txt', 'Test content')
            m.assert_called_once_with('test.txt', 'w')
            m().write.assert_called_once_with('Test content')
    
    def test_process_csv(self):
        """Тест обработки CSV файла"""
        processor = FileProcessor()
        
        csv_content = "name,age,city\nJohn,25,NYC\nJane,30,LA"
        
        with patch('builtins.open', mock_open(read_data=csv_content)):
            results = processor.process_csv('test.csv')
            
            assert len(results) == 2
            assert results[0] == {'name': 'John', 'age': '25', 'city': 'NYC'}
            assert results[1] == {'name': 'Jane', 'age': '30', 'city': 'LA'}


# ============= Тесты RateLimiter =============

class TestRateLimiter:
    """Тесты для RateLimiter"""
    
    def test_allows_within_limit(self):
        """Тест разрешения в пределах лимита"""
        limiter = RateLimiter(max_calls=3, time_window=60)
        
        assert limiter.is_allowed() is True
        assert limiter.is_allowed() is True
        assert limiter.is_allowed() is True
    
    def test_blocks_over_limit(self):
        """Тест блокировки при превышении лимита"""
        limiter = RateLimiter(max_calls=2, time_window=60)
        
        assert limiter.is_allowed() is True
        assert limiter.is_allowed() is True
        assert limiter.is_allowed() is False  # Превышен лимит
    
    def test_reset(self):
        """Тест сброса лимита"""
        limiter = RateLimiter(max_calls=2, time_window=60)
        
        limiter.is_allowed()
        limiter.is_allowed()
        
        limiter.reset()
        assert limiter.is_allowed() is True


# ============= Тесты валидатора =============

class TestValidator:
    """Тесты для Validator"""
    
    @pytest.mark.parametrize("email, expected", [
        ("test@example.com", True),
        ("user@domain.co.uk", True),
        ("invalid", False),
        ("@example.com", False),
        ("test@", False),
        ("", False),
    ])
    def test_validate_email(self, email, expected):
        """Параметризованный тест валидации email"""
        assert Validator.validate_email(email) == expected
    
    @pytest.mark.parametrize("phone, expected", [
        ("+1234567890", True),
        ("123-456-7890", True),
        ("12345", False),
        ("", False),
    ])
    def test_validate_phone(self, phone, expected):
        """Параметризованный тест валидации телефона"""
        assert Validator.validate_phone(phone) == expected
    
    @pytest.mark.parametrize("age, expected", [
        (0, True),
        (25, True),
        (150, True),
        (-1, False),
        (151, False),
    ])
    def test_validate_age(self, age, expected):
        """Параметризованный тест валидации возраста"""
        assert Validator.validate_age(age) == expected


# ============= Тесты с использованием time.time() =============

def test_with_time_mock():
    """Тест с мокированием времени"""
    with patch('time.time', return_value=1000.0):
        assert time.time() == 1000.0


# ============= Комплексный тест =============

def test_complex_scenario():
    """Комплексный сценарий с несколькими компонентами"""
    # Создаем БД и кеш
    db = Database().connect()
    cache = Cache()
    
    # Добавляем пользователя в БД
    user_data = {'id': 1, 'name': 'John', 'email': 'john@example.com'}
    db.insert('users', user_data)
    
    # Кешируем результат
    cache.set('user:1', user_data, ttl=60)
    
    # Проверяем, что данные одинаковые
    db_user = db.select('users', filter_by={'id': 1})[0]
    cached_user = cache.get('user:1')
    
    assert db_user == cached_user
    assert db_user['name'] == 'John'

