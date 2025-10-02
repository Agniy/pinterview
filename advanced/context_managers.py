"""
🔴 КОНТЕКСТНЫЕ МЕНЕДЖЕРЫ - Вопросы и задачи для собеседований

Основные темы:
- __enter__ и __exit__
- with statement
- contextlib
- Обработка исключений в контекстных менеджерах
"""

from contextlib import contextmanager, closing, suppress, redirect_stdout, ExitStack
import time
import sys
from io import StringIO


# ============================================================================
# ТЕОРЕТИЧЕСКИЕ ВОПРОСЫ
# ============================================================================

"""
Q1: Что такое контекстный менеджер?
A: Объект, определяющий контекст выполнения (with statement)
через методы __enter__ и __exit__

Q2: Зачем нужны контекстные менеджеры?
A:
- Гарантируют очистку ресурсов
- Упрощают обработку ошибок
- Делают код более читаемым

Q3: Что возвращает __enter__?
A: Значение, которое присваивается переменной после as

Q4: Параметры метода __exit__?
A: exc_type, exc_val, exc_tb - информация об исключении
Если вернуть True, исключение будет подавлено

Q5: Что такое contextlib?
A: Модуль с утилитами для создания контекстных менеджеров
"""


# ============================================================================
# ЗАДАЧА 1: Простой контекстный менеджер
# ============================================================================

class Timer:
    """
    🟡 Middle level
    Контекстный менеджер для измерения времени
    """
    
    def __enter__(self):
        self.start = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        self.elapsed = self.end - self.start
        print(f"Время выполнения: {self.elapsed:.4f}с")
        return False  # Не подавляем исключения


def demo_timer():
    print("Контекстный менеджер Timer:")
    with Timer():
        time.sleep(0.1)
        sum(range(1000000))


# ============================================================================
# ЗАДАЧА 2: Управление файлами
# ============================================================================

class FileManager:
    """
    🟡 Middle level
    Контекстный менеджер для работы с файлами
    """
    
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        print(f"Открытие файла: {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Закрытие файла: {self.filename}")
        if self.file:
            self.file.close()
        
        if exc_type is not None:
            print(f"Произошла ошибка: {exc_val}")
        
        return False


# ============================================================================
# ЗАДАЧА 3: Подавление исключений
# ============================================================================

class SuppressException:
    """
    🟡 Middle level
    Подавляет указанные типы исключений
    """
    
    def __init__(self, *exceptions):
        self.exceptions = exceptions
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and issubclass(exc_type, self.exceptions):
            print(f"Подавлено исключение: {exc_type.__name__}")
            return True  # Подавляем исключение
        return False


def demo_suppress():
    print("\nПодавление исключений:")
    
    with SuppressException(ValueError, TypeError):
        print("Вызываем ошибку...")
        raise ValueError("Эта ошибка будет подавлена")
    
    print("Код продолжает работать")


# ============================================================================
# ЗАДАЧА 4: Временное изменение атрибута
# ============================================================================

class TemporaryAttribute:
    """
    🔴 Senior level
    Временно изменяет атрибут объекта
    """
    
    def __init__(self, obj, attr, new_value):
        self.obj = obj
        self.attr = attr
        self.new_value = new_value
        self.old_value = None
    
    def __enter__(self):
        self.old_value = getattr(self.obj, self.attr)
        setattr(self.obj, self.attr, self.new_value)
        return self.new_value
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        setattr(self.obj, self.attr, self.old_value)
        return False


class Config:
    debug = False


def demo_temp_attr():
    print("\nВременное изменение атрибута:")
    config = Config()
    
    print(f"Debug mode: {config.debug}")
    
    with TemporaryAttribute(config, 'debug', True):
        print(f"В контексте: {config.debug}")
    
    print(f"После контекста: {config.debug}")


# ============================================================================
# ЗАДАЧА 5: Декоратор @contextmanager
# ============================================================================

@contextmanager
def timer_context():
    """
    🟡 Middle level
    Контекстный менеджер через декоратор
    """
    start = time.time()
    print("Таймер запущен...")
    
    try:
        yield  # Выполнение кода в with блоке
    finally:
        end = time.time()
        print(f"Таймер: {end - start:.4f}с")


@contextmanager
def managed_resource(name):
    """Управление ресурсом"""
    print(f"Захват ресурса: {name}")
    
    try:
        yield name
    finally:
        print(f"Освобождение ресурса: {name}")


def demo_contextmanager():
    print("\n@contextmanager декоратор:")
    
    with timer_context():
        time.sleep(0.1)
    
    with managed_resource("Database") as resource:
        print(f"Работаем с: {resource}")


# ============================================================================
# ЗАДАЧА 6: Транзакция базы данных
# ============================================================================

class DatabaseTransaction:
    """
    🔴 Senior level
    Контекстный менеджер для транзакций БД
    """
    
    def __init__(self, connection):
        self.connection = connection
        self.transaction = None
    
    def __enter__(self):
        print("Начало транзакции...")
        self.transaction = "Transaction started"
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            print("Commit транзакции")
            # self.connection.commit()
        else:
            print(f"Rollback транзакции из-за: {exc_val}")
            # self.connection.rollback()
        
        return False


def demo_transaction():
    print("\nТранзакция БД:")
    
    # Успешная транзакция
    with DatabaseTransaction("connection") as trans:
        print("  Выполняем операции...")
    
    # Транзакция с ошибкой
    try:
        with DatabaseTransaction("connection") as trans:
            print("  Выполняем операции...")
            raise ValueError("Ошибка в транзакции")
    except ValueError:
        print("  Ошибка обработана")


# ============================================================================
# ЗАДАЧА 7: Изменение директории
# ============================================================================

import os

@contextmanager
def change_directory(path):
    """
    🟡 Middle level
    Временно меняет рабочую директорию
    """
    original = os.getcwd()
    
    try:
        os.chdir(path)
        yield path
    finally:
        os.chdir(original)


# ============================================================================
# ЗАДАЧА 8: Множественные контекстные менеджеры
# ============================================================================

class ResourceManager:
    """
    🔴 Senior level
    Управление несколькими ресурсами
    """
    
    def __init__(self, name):
        self.name = name
    
    def __enter__(self):
        print(f"  Открыт: {self.name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"  Закрыт: {self.name}")
        return False


def demo_multiple_context():
    print("\nМножественные контекстные менеджеры:")
    
    # Классический способ
    with ResourceManager("Resource 1"), ResourceManager("Resource 2"):
        print("  Работа с ресурсами")
    
    # ExitStack для динамического количества
    print("\nExitStack:")
    with ExitStack() as stack:
        resources = []
        for i in range(3):
            res = stack.enter_context(ResourceManager(f"Res{i+1}"))
            resources.append(res)
        
        print("  Все ресурсы открыты")


# ============================================================================
# ЗАДАЧА 9: Захват вывода
# ============================================================================

@contextmanager
def capture_stdout():
    """
    🟡 Middle level
    Захватывает вывод в stdout
    """
    old_stdout = sys.stdout
    sys.stdout = captured = StringIO()
    
    try:
        yield captured
    finally:
        sys.stdout = old_stdout


def demo_capture():
    print("\nЗахват вывода:")
    
    with capture_stdout() as output:
        print("Это будет захвачено")
        print("И это тоже")
    
    print(f"Захваченный вывод: {output.getvalue()}")
    
    # Встроенный redirect_stdout
    print("\nredirect_stdout:")
    f = StringIO()
    with redirect_stdout(f):
        print("Перенаправленный вывод")
    
    print(f"Результат: {f.getvalue()}")


# ============================================================================
# ЗАДАЧА 10: Retry контекстный менеджер
# ============================================================================

@contextmanager
def retry(max_attempts=3, delay=1):
    """
    🔴 Senior level
    Повторяет операции при ошибке
    """
    for attempt in range(max_attempts):
        try:
            yield attempt + 1
            break  # Успех
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            print(f"Попытка {attempt + 1} провалилась: {e}")
            time.sleep(delay)


def demo_retry():
    print("\nRetry контекстный менеджер:")
    
    counter = {'value': 0}
    
    with retry(max_attempts=3, delay=0.1):
        counter['value'] += 1
        print(f"  Попытка {counter['value']}")
        if counter['value'] < 2:
            raise ValueError("Ошибка!")
        print("  Успех!")


# ============================================================================
# ЗАДАЧА 11: Lock контекстный менеджер
# ============================================================================

class Lock:
    """
    🔴 Senior level
    Простая реализация блокировки
    """
    
    def __init__(self):
        self.locked = False
    
    def __enter__(self):
        while self.locked:
            time.sleep(0.01)
        self.locked = True
        print("Lock acquired")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.locked = False
        print("Lock released")
        return False


def demo_lock():
    print("\nLock:")
    lock = Lock()
    
    with lock:
        print("  Критическая секция")


# ============================================================================
# ЗАДАЧА 12: closing из contextlib
# ============================================================================

class Resource:
    """Ресурс с методом close()"""
    
    def __init__(self, name):
        self.name = name
        print(f"Создан ресурс: {name}")
    
    def close(self):
        print(f"Закрыт ресурс: {self.name}")


def demo_closing():
    print("\nclosing:")
    
    with closing(Resource("TestResource")) as res:
        print(f"  Используем {res.name}")


# ============================================================================
# ЗАДАЧА 13: suppress из contextlib
# ============================================================================

def demo_suppress_contextlib():
    print("\nsuppress из contextlib:")
    
    with suppress(FileNotFoundError):
        with open('nonexistent_file.txt') as f:
            content = f.read()
    
    print("Код продолжает работу после подавленного исключения")


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("КОНТЕКСТНЫЕ МЕНЕДЖЕРЫ - Примеры и тесты")
    print("=" * 60)
    
    # Тест 1: Timer
    demo_timer()
    
    # Тест 2: Подавление исключений
    demo_suppress()
    
    # Тест 3: Временное изменение атрибута
    demo_temp_attr()
    
    # Тест 4: @contextmanager
    demo_contextmanager()
    
    # Тест 5: Транзакция
    demo_transaction()
    
    # Тест 6: Множественные контекстные менеджеры
    demo_multiple_context()
    
    # Тест 7: Захват вывода
    demo_capture()
    
    # Тест 8: Retry
    demo_retry()
    
    # Тест 9: Lock
    demo_lock()
    
    # Тест 10: closing
    demo_closing()
    
    # Тест 11: suppress
    demo_suppress_contextlib()
    
    print("\n" + "=" * 60)

