"""
Демонстрация работы с фикстурами из conftest.py
"""

import pytest
import time


# ============= Использование фикстур БД =============

def test_db_fixture(db):
    """Тест использования фикстуры db"""
    db.insert('products', {'id': 1, 'name': 'Laptop', 'price': 1000})
    
    products = db.select('products')
    assert len(products) == 1
    assert products[0]['name'] == 'Laptop'


def test_db_with_users_fixture(db_with_users):
    """Тест использования фикстуры с предзаполненными данными"""
    users = db_with_users.select('users')
    
    assert len(users) == 3
    assert users[0]['name'] == 'John'
    assert users[1]['name'] == 'Jane'
    assert users[2]['name'] == 'Bob'


def test_db_isolation(db):
    """
    Тест изоляции БД между тестами
    Каждый тест получает чистую БД
    """
    # В этом тесте БД должна быть пустой
    users = db.select('users')
    assert len(users) == 0


# ============= Использование фикстур кеша =============

def test_cache_fixture(cache):
    """Тест использования фикстуры cache"""
    cache.set('test_key', 'test_value')
    
    assert cache.get('test_key') == 'test_value'
    assert cache.size() == 1


def test_cache_with_data_fixture(cache_with_data):
    """Тест использования фикстуры с предзаполненным кешем"""
    assert cache_with_data.get('key1') == 'value1'
    assert cache_with_data.get('key2') == 'value2'
    assert cache_with_data.get('key3') == {'nested': 'data'}
    assert cache_with_data.size() == 3


# ============= Использование фикстур для файлов =============

def test_temp_file_fixture(temp_file):
    """Тест использования временного файла"""
    # Записываем в файл
    with open(temp_file, 'w') as f:
        f.write('Test content')
    
    # Читаем из файла
    with open(temp_file, 'r') as f:
        content = f.read()
    
    assert content == 'Test content'


def test_temp_dir_fixture(temp_dir):
    """Тест использования временной директории"""
    import os
    
    # Создаем файл в временной директории
    filepath = os.path.join(temp_dir, 'test.txt')
    with open(filepath, 'w') as f:
        f.write('Hello')
    
    # Проверяем, что файл существует
    assert os.path.exists(filepath)


# ============= Использование фикстур с тестовыми данными =============

def test_sample_users_fixture(sample_users):
    """Тест использования фикстуры с примерами пользователей"""
    assert len(sample_users) == 3
    assert sample_users[0]['name'] == 'Alice'
    assert all('email' in user for user in sample_users)


def test_sample_numbers_fixture(sample_numbers):
    """Тест использования фикстуры с примерами чисел"""
    assert sum(sample_numbers) == 191
    assert min(sample_numbers) == 1
    assert max(sample_numbers) == 100


# ============= Использование параметризованных фикстур =============

def test_cache_with_different_ttl(cache_ttl):
    """
    Тест будет запущен 3 раза с разными значениями TTL
    (10, 20, 30 - как указано в фикстуре)
    """
    from advanced_examples import Cache
    
    cache = Cache(default_ttl=cache_ttl)
    assert cache.default_ttl == cache_ttl


# ============= Комбинирование нескольких фикстур =============

def test_multiple_fixtures(db, cache, sample_users):
    """Тест использования нескольких фикстур одновременно"""
    # Добавляем пользователей в БД
    for user in sample_users:
        db.insert('users', user)
    
    # Кешируем первого пользователя
    first_user = db.select('users')[0]
    cache.set('first_user', first_user)
    
    # Проверяем
    cached_user = cache.get('first_user')
    assert cached_user['name'] == 'Alice'


# ============= Использование фикстуры для захвата вывода =============

def test_captured_output_fixture(captured_output):
    """Тест захвата stdout"""
    stdout, stderr = captured_output
    
    print("Hello, World!")
    print("Testing output")
    
    output = stdout.getvalue()
    assert "Hello, World!" in output
    assert "Testing output" in output


# ============= Использование фикстуры для переменных окружения =============

def test_mock_env_vars_fixture(mock_env_vars):
    """Тест мокирования переменных окружения"""
    import os
    
    mock_env_vars(
        DATABASE_URL='postgresql://localhost/test',
        API_KEY='test_key_123'
    )
    
    assert os.getenv('DATABASE_URL') == 'postgresql://localhost/test'
    assert os.getenv('API_KEY') == 'test_key_123'


# ============= Использование фикстуры таймера =============

def test_timer_fixture(timer):
    """Тест измерения времени выполнения"""
    timer.start()
    
    # Имитация какой-то работы
    time.sleep(0.1)
    
    timer.stop()
    
    elapsed = timer.elapsed()
    assert elapsed >= 0.1
    assert elapsed < 0.2  # Проверяем, что не заняло слишком много времени


# ============= Вложенные фикстуры =============

@pytest.fixture
def user_service(db):
    """
    Пример фикстуры, которая зависит от другой фикстуры
    Фикстура db будет автоматически создана и передана
    """
    class UserService:
        def __init__(self, database):
            self.db = database
        
        def create_user(self, name, email):
            user = {'name': name, 'email': email}
            self.db.insert('users', user)
            return user
        
        def get_all_users(self):
            return self.db.select('users')
    
    return UserService(db)


def test_user_service(user_service):
    """Тест использования вложенной фикстуры"""
    user_service.create_user('Test User', 'test@example.com')
    
    users = user_service.get_all_users()
    assert len(users) == 1
    assert users[0]['name'] == 'Test User'


# ============= Использование scope фикстур =============

def test_module_scoped_db(db_module):
    """
    Тест использования фикстуры с scope='module'
    Эта фикстура создается один раз для всего модуля
    """
    db_module.insert('logs', {'message': 'Test log'})
    
    logs = db_module.select('logs')
    assert len(logs) >= 1  # >= потому что могут быть данные из других тестов в модуле


# ============= Демонстрация autouse фикстуры =============

def test_autouse_fixture_demo():
    """
    Фикстура reset_environment из conftest.py
    автоматически выполняется перед этим тестом
    (и перед всеми другими тестами)
    """
    # Просто проверяем, что тест работает
    assert True


# ============= Использование monkeypatch =============

def test_monkeypatch_example(monkeypatch):
    """
    Пример использования встроенной фикстуры monkeypatch
    для изменения поведения кода
    """
    def mock_function():
        return "mocked value"
    
    # Заменяем функцию
    import advanced_examples
    monkeypatch.setattr(advanced_examples, 'Validator', mock_function)
    
    # Теперь вызов вернет замоканное значение
    result = advanced_examples.Validator()
    assert result == "mocked value"


# ============= Использование capsys для захвата вывода =============

def test_capsys_example(capsys):
    """
    Пример использования встроенной фикстуры capsys
    для захвата stdout/stderr
    """
    print("Standard output")
    print("Error output", file=__import__('sys').stderr)
    
    captured = capsys.readouterr()
    assert "Standard output" in captured.out
    assert "Error output" in captured.err


# ============= Использование tmpdir (устаревшая, но все еще работает) =============

def test_tmpdir_example(tmp_path):
    """
    Пример использования встроенной фикстуры tmp_path
    для создания временной директории
    """
    # tmp_path - это объект Path из pathlib
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")
    
    assert test_file.read_text() == "test content"

