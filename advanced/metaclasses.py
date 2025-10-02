"""
🔴 МЕТАКЛАССЫ - Вопросы и задачи для собеседований

Основные темы:
- Метаклассы и type
- __new__ и __init__ метаклассов
- __init_subclass__
- ABCMeta
"""


# ============================================================================
# ТЕОРЕТИЧЕСКИЕ ВОПРОСЫ
# ============================================================================

"""
Q1: Что такое метакласс?
A: Класс класса. Определяет поведение класса, как класс определяет поведение объектов.

Q2: Какой метакласс по умолчанию?
A: type

Q3: Зачем нужны метаклассы?
A:
- Валидация классов
- Автоматическая регистрация
- Модификация атрибутов класса
- API frameworks (Django ORM, SQLAlchemy)

Q4: Когда НЕ использовать метаклассы?
A: Почти всегда! Есть более простые альтернативы:
- Декораторы классов
- __init_subclass__
- Дескрипторы

Q5: Как создать класс через type?
A: type(name, bases, dict)
"""


# ============================================================================
# ЗАДАЧА 1: Создание класса через type
# ============================================================================

def demo_type_creation():
    """
    🟡 Middle level
    Создание класса динамически через type
    """
    
    # Классический способ
    class MyClass:
        x = 10
        
        def method(self):
            return "Hello"
    
    # Через type
    MyClassDynamic = type(
        'MyClassDynamic',
        (),
        {
            'x': 10,
            'method': lambda self: "Hello"
        }
    )
    
    print("Класс через type:")
    obj = MyClassDynamic()
    print(f"  obj.x = {obj.x}")
    print(f"  obj.method() = {obj.method()}")
    print(f"  type(obj) = {type(obj)}")
    print(f"  type(MyClassDynamic) = {type(MyClassDynamic)}")


# ============================================================================
# ЗАДАЧА 2: Простой метакласс
# ============================================================================

class SimpleMeta(type):
    """
    🟡 Middle level
    Простой метакласс, который выводит информацию при создании класса
    """
    
    def __new__(mcs, name, bases, attrs):
        print(f"Создается класс: {name}")
        print(f"  Базовые классы: {bases}")
        print(f"  Атрибуты: {list(attrs.keys())}")
        
        # Создаем класс
        cls = super().__new__(mcs, name, bases, attrs)
        return cls


class MyClass(metaclass=SimpleMeta):
    """Класс с метаклассом"""
    x = 10
    
    def method(self):
        return "test"


# ============================================================================
# ЗАДАЧА 3: Метакласс для валидации
# ============================================================================

class ValidatedMeta(type):
    """
    🔴 Senior level
    Метакласс, проверяющий наличие обязательных методов
    """
    
    def __new__(mcs, name, bases, attrs):
        # Пропускаем базовый класс
        if name == 'ValidatedBase':
            return super().__new__(mcs, name, bases, attrs)
        
        # Проверяем наличие required методов
        required_methods = attrs.get('_required_methods', [])
        
        for method_name in required_methods:
            if method_name not in attrs:
                raise TypeError(
                    f"Класс {name} должен реализовать метод {method_name}"
                )
        
        return super().__new__(mcs, name, bases, attrs)


class ValidatedBase(metaclass=ValidatedMeta):
    """Базовый класс с валидацией"""
    _required_methods = []


class Plugin(ValidatedBase):
    """Плагин должен иметь методы initialize и execute"""
    _required_methods = ['initialize', 'execute']
    
    def initialize(self):
        print("Plugin initialized")
    
    def execute(self):
        print("Plugin executed")


def demo_validation():
    print("\nМетакласс с валидацией:")
    plugin = Plugin()
    plugin.initialize()
    plugin.execute()
    
    # Попытка создать невалидный класс
    try:
        class InvalidPlugin(ValidatedBase):
            _required_methods = ['required_method']
            pass
    except TypeError as e:
        print(f"Ошибка валидации: {e}")


# ============================================================================
# ЗАДАЧА 4: Singleton через метакласс
# ============================================================================

class SingletonMeta(type):
    """
    🔴 Senior level
    Метакласс для паттерна Singleton
    """
    
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    """Класс базы данных - синглтон"""
    
    def __init__(self):
        print("Инициализация Database")
        self.connection = "DB Connection"


def demo_singleton():
    print("\nSingleton через метакласс:")
    db1 = Database()
    db2 = Database()
    
    print(f"db1 is db2: {db1 is db2}")


# ============================================================================
# ЗАДАЧА 5: Автоматическая регистрация классов
# ============================================================================

class RegistryMeta(type):
    """
    🔴 Senior level
    Метакласс для автоматической регистрации классов
    """
    
    registry = {}
    
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        
        # Регистрируем класс, если есть имя для регистрации
        if 'registry_name' in attrs:
            mcs.registry[attrs['registry_name']] = cls
        
        return cls


class Command(metaclass=RegistryMeta):
    """Базовый класс команды"""
    pass


class StartCommand(Command):
    """Команда запуска"""
    registry_name = 'start'
    
    def execute(self):
        return "Starting..."


class StopCommand(Command):
    """Команда остановки"""
    registry_name = 'stop'
    
    def execute(self):
        return "Stopping..."


def demo_registry():
    print("\nАвтоматическая регистрация:")
    print(f"Зарегистрированные команды: {list(RegistryMeta.registry.keys())}")
    
    # Получаем команду по имени
    start_cmd = RegistryMeta.registry['start']()
    print(f"start: {start_cmd.execute()}")


# ============================================================================
# ЗАДАЧА 6: __init_subclass__ (альтернатива метаклассам)
# ============================================================================

class PluginBase:
    """
    🟡 Middle level
    Использование __init_subclass__ вместо метакласса
    """
    
    plugins = {}
    
    def __init_subclass__(cls, plugin_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if plugin_name:
            cls.plugins[plugin_name] = cls


class ImagePlugin(PluginBase, plugin_name='image'):
    """Плагин для изображений"""
    
    def process(self):
        return "Processing image"


class VideoPlugin(PluginBase, plugin_name='video'):
    """Плагин для видео"""
    
    def process(self):
        return "Processing video"


def demo_init_subclass():
    print("\n__init_subclass__ (альтернатива метаклассам):")
    print(f"Плагины: {list(PluginBase.plugins.keys())}")
    
    for name, plugin_cls in PluginBase.plugins.items():
        plugin = plugin_cls()
        print(f"  {name}: {plugin.process()}")


# ============================================================================
# ЗАДАЧА 7: Метакласс для добавления атрибутов
# ============================================================================

class AttributeAdderMeta(type):
    """
    🟡 Middle level
    Добавляет автоматические атрибуты ко всем классам
    """
    
    def __new__(mcs, name, bases, attrs):
        # Добавляем timestamp создания
        import time
        attrs['_created_at'] = time.time()
        
        # Добавляем метод для получения всех методов
        def get_methods(self):
            return [m for m in dir(self) if not m.startswith('_')]
        
        attrs['get_methods'] = get_methods
        
        return super().__new__(mcs, name, bases, attrs)


class MyService(metaclass=AttributeAdderMeta):
    """Сервис с автоматическими атрибутами"""
    
    def start(self):
        pass
    
    def stop(self):
        pass


def demo_attribute_adder():
    print("\nДобавление атрибутов через метакласс:")
    service = MyService()
    
    print(f"Создан в: {service._created_at}")
    print(f"Методы: {service.get_methods()}")


# ============================================================================
# ЗАДАЧА 8: Метакласс для логирования
# ============================================================================

class LoggingMeta(type):
    """
    🔴 Senior level
    Метакласс, добавляющий логирование ко всем методам
    """
    
    def __new__(mcs, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and not attr_name.startswith('_'):
                attrs[attr_name] = mcs.log_method(attr_value)
        
        return super().__new__(mcs, name, bases, attrs)
    
    @staticmethod
    def log_method(method):
        """Обертка для логирования"""
        def wrapper(*args, **kwargs):
            print(f"Вызов метода: {method.__name__}")
            result = method(*args, **kwargs)
            print(f"Метод {method.__name__} вернул: {result}")
            return result
        return wrapper


class Calculator(metaclass=LoggingMeta):
    """Калькулятор с автоматическим логированием"""
    
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b


def demo_logging():
    print("\nАвтоматическое логирование:")
    calc = Calculator()
    calc.add(2, 3)
    calc.multiply(4, 5)


# ============================================================================
# ЗАДАЧА 9: ABCMeta (абстрактные классы)
# ============================================================================

from abc import ABCMeta, abstractmethod

class Shape(metaclass=ABCMeta):
    """
    🟡 Middle level
    Абстрактный класс через ABCMeta
    """
    
    @abstractmethod
    def area(self):
        """Должен быть реализован в подклассах"""
        pass
    
    @abstractmethod
    def perimeter(self):
        """Должен быть реализован в подклассах"""
        pass


class Rectangle(Shape):
    """Прямоугольник"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)


def demo_abc():
    print("\nABCMeta (абстрактные классы):")
    
    # Нельзя создать экземпляр абстрактного класса
    try:
        shape = Shape()
    except TypeError as e:
        print(f"Ошибка: {e}")
    
    # Можно создать конкретный класс
    rect = Rectangle(5, 3)
    print(f"Площадь: {rect.area()}")
    print(f"Периметр: {rect.perimeter()}")


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("МЕТАКЛАССЫ - Примеры и тесты")
    print("=" * 60)
    
    # Тест 1: Создание через type
    print("\n1. Создание класса через type:")
    demo_type_creation()
    
    # Тест 2: Простой метакласс
    print("\n2. Простой метакласс:")
    print("(вывод при определении класса MyClass выше)")
    
    # Тест 3: Валидация
    demo_validation()
    
    # Тест 4: Singleton
    demo_singleton()
    
    # Тест 5: Регистрация
    demo_registry()
    
    # Тест 6: __init_subclass__
    demo_init_subclass()
    
    # Тест 7: Добавление атрибутов
    demo_attribute_adder()
    
    # Тест 8: Логирование
    demo_logging()
    
    # Тест 9: ABCMeta
    demo_abc()
    
    print("\n" + "=" * 60)
    print("\nВАЖНО: Метаклассы - мощный, но сложный инструмент.")
    print("В большинстве случаев лучше использовать:")
    print("  - Декораторы классов")
    print("  - __init_subclass__")
    print("  - Дескрипторы")
    print("=" * 60)

