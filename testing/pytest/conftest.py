"""
conftest.py - Файл с общими фикстурами для всех тестов

Этот файл автоматически загружается pytest и содержит фикстуры,
которые доступны во всех тестовых файлах без явного импорта.
"""

import pytest
import tempfile
import os
from .advanced_examples import Database, Cache


# ============= Фикстуры для базы данных =============

@pytest.fixture
def db():
    """Фикстура для создания подключенной БД"""
    database = Database()
    database.connect()
    
    yield database
    
    # Cleanup
    database.clear()
    database.disconnect()


@pytest.fixture(scope="module")
def db_module():
    """Фикстура БД на уровне модуля (создается один раз для всего модуля)"""
    database = Database()
    database.connect()
    
    yield database
    
    database.clear()
    database.disconnect()


@pytest.fixture
def db_with_users(db):
    """Фикстура БД с предзаполненными пользователями"""
    users = [
        {'id': 1, 'name': 'John', 'email': 'john@example.com', 'age': 25},
        {'id': 2, 'name': 'Jane', 'email': 'jane@example.com', 'age': 30},
        {'id': 3, 'name': 'Bob', 'email': 'bob@example.com', 'age': 35},
    ]
    
    for user in users:
        db.insert('users', user)
    
    return db


# ============= Фикстуры для кеша =============

@pytest.fixture
def cache():
    """Фикстура для создания кеша"""
    cache_instance = Cache(default_ttl=3600)
    
    yield cache_instance
    
    # Cleanup
    cache_instance.clear()


@pytest.fixture
def cache_with_data(cache):
    """Фикстура кеша с предзаполненными данными"""
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    cache.set('key3', {'nested': 'data'})
    
    return cache


# ============= Фикстуры для работы с файлами =============

@pytest.fixture
def temp_file():
    """Фикстура для создания временного файла"""
    # Создаем временный файл
    fd, filepath = tempfile.mkstemp(suffix='.txt')
    os.close(fd)
    
    yield filepath
    
    # Удаляем файл после теста
    if os.path.exists(filepath):
        os.remove(filepath)


@pytest.fixture
def temp_dir():
    """Фикстура для создания временной директории"""
    dirpath = tempfile.mkdtemp()
    
    yield dirpath
    
    # Удаляем директорию после теста
    import shutil
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)


# ============= Фикстуры для тестовых данных =============

@pytest.fixture
def sample_users():
    """Фикстура с примерами пользователей"""
    return [
        {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
        {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
        {'id': 3, 'name': 'Charlie', 'email': 'charlie@example.com'},
    ]


@pytest.fixture
def sample_numbers():
    """Фикстура с примерами чисел"""
    return [1, 2, 3, 4, 5, 10, 20, 50, 100]


# ============= Параметризованные фикстуры =============

@pytest.fixture(params=[10, 20, 30])
def cache_ttl(request):
    """Параметризованная фикстура для разных TTL"""
    return request.param


@pytest.fixture(params=['sqlite', 'postgres', 'mysql'])
def db_type(request):
    """Параметризованная фикстура для разных типов БД"""
    return request.param


# ============= Автоиспользуемые фикстуры =============

@pytest.fixture(autouse=True)
def reset_environment():
    """
    Автоматически выполняется перед каждым тестом
    Используется для сброса глобального состояния
    """
    # Setup - выполняется перед тестом
    print("\n[SETUP] Подготовка окружения")
    
    yield
    
    # Teardown - выполняется после теста
    print("[TEARDOWN] Очистка окружения")


# ============= Фикстуры для маркировки тестов =============

def pytest_configure(config):
    """Регистрация кастомных маркеров"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "smoke: marks tests as smoke tests"
    )


# ============= Хуки для настройки pytest =============

def pytest_collection_modifyitems(config, items):
    """
    Модификация собранных тестов
    Например, добавление маркеров на основе имени файла
    """
    for item in items:
        # Добавляем маркер 'unit' для всех тестов в файлах test_unit_*.py
        if 'test_unit_' in item.nodeid:
            item.add_marker(pytest.mark.unit)
        
        # Добавляем маркер 'integration' для всех тестов в файлах test_integration_*.py
        if 'test_integration_' in item.nodeid:
            item.add_marker(pytest.mark.integration)


# ============= Фикстуры для захвата вывода =============

@pytest.fixture
def captured_output():
    """Фикстура для захвата stdout/stderr"""
    import io
    import sys
    
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()
    
    yield sys.stdout, sys.stderr
    
    sys.stdout = old_stdout
    sys.stderr = old_stderr


# ============= Фикстуры для работы с окружением =============

@pytest.fixture
def mock_env_vars(monkeypatch):
    """Фикстура для мокирования переменных окружения"""
    def _set_env(**kwargs):
        for key, value in kwargs.items():
            monkeypatch.setenv(key, value)
    
    return _set_env


# ============= Фикстура для измерения времени выполнения =============

@pytest.fixture
def timer():
    """Фикстура для измерения времени выполнения"""
    import time
    
    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
        
        def start(self):
            self.start_time = time.time()
        
        def stop(self):
            self.end_time = time.time()
        
        def elapsed(self):
            if self.start_time and self.end_time:
                return self.end_time - self.start_time
            return None
    
    return Timer()

