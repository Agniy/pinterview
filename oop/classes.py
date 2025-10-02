"""
🟡 КЛАССЫ И НАСЛЕДОВАНИЕ - Вопросы и задачи для собеседований

Основные темы:
- Классы и объекты
- Наследование
- Полиморфизм
- Инкапсуляция
- Множественное наследование и MRO
- Абстрактные классы
"""

from abc import ABC, abstractmethod


# ============================================================================
# ТЕОРЕТИЧЕСКИЕ ВОПРОСЫ
# ============================================================================

"""
Q1: Что такое класс и объект?
A:
- Класс - шаблон для создания объектов
- Объект - экземпляр класса

Q2: Что такое self?
A: Ссылка на текущий экземпляр класса

Q3: В чем разница между __init__ и __new__?
A:
- __new__ - создает экземпляр (вызывается первым)
- __init__ - инициализирует экземпляр

Q4: Что такое наследование?
A: Механизм создания нового класса на основе существующего,
наследуя его атрибуты и методы.

Q5: Что такое MRO (Method Resolution Order)?
A: Порядок поиска методов в иерархии классов.
Можно посмотреть через ClassName.__mro__ или ClassName.mro()

Q6: Какие виды атрибутов есть в Python?
A:
- Атрибуты экземпляра (instance attributes)
- Атрибуты класса (class attributes)
"""


# ============================================================================
# ЗАДАЧА 1: Простой класс - Точка
# ============================================================================

class Point:
    """
    🟢 Junior level
    Класс для представления точки в 2D пространстве
    """
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def distance_from_origin(self):
        """Расстояние от начала координат"""
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def distance_to(self, other):
        """Расстояние до другой точки"""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    
    def __str__(self):
        return f"Point({self.x}, {self.y})"


def demo_point():
    p1 = Point(3, 4)
    p2 = Point(0, 0)
    
    print(f"Точка: {p1}")
    print(f"Расстояние от начала: {p1.distance_from_origin()}")
    print(f"Расстояние до {p2}: {p1.distance_to(p2)}")


# ============================================================================
# ЗАДАЧА 2: Наследование - Геометрические фигуры
# ============================================================================

class Shape(ABC):
    """
    🟡 Middle level
    Абстрактный базовый класс для фигур
    """
    
    @abstractmethod
    def area(self):
        """Площадь фигуры"""
        pass
    
    @abstractmethod
    def perimeter(self):
        """Периметр фигуры"""
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
    
    def __str__(self):
        return f"Rectangle({self.width}x{self.height})"


class Circle(Shape):
    """Круг"""
    
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        import math
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        import math
        return 2 * math.pi * self.radius
    
    def __str__(self):
        return f"Circle(r={self.radius})"


def demo_shapes():
    shapes = [
        Rectangle(5, 3),
        Circle(4),
        Rectangle(2, 2)
    ]
    
    for shape in shapes:
        print(f"{shape}: Area={shape.area():.2f}, Perimeter={shape.perimeter():.2f}")


# ============================================================================
# ЗАДАЧА 3: Атрибуты класса vs атрибуты экземпляра
# ============================================================================

class Employee:
    """
    🟡 Middle level
    Демонстрация атрибутов класса и экземпляра
    """
    
    company = "TechCorp"  # Атрибут класса
    employee_count = 0     # Атрибут класса
    
    def __init__(self, name, salary):
        self.name = name       # Атрибут экземпляра
        self.salary = salary   # Атрибут экземпляра
        Employee.employee_count += 1
    
    @classmethod
    def get_employee_count(cls):
        """Метод класса"""
        return cls.employee_count
    
    @staticmethod
    def is_valid_salary(salary):
        """Статический метод"""
        return salary > 0
    
    def __str__(self):
        return f"{self.name} (${self.salary})"


def demo_employee():
    emp1 = Employee("Alice", 50000)
    emp2 = Employee("Bob", 60000)
    
    print(f"Компания: {Employee.company}")
    print(f"Сотрудников: {Employee.get_employee_count()}")
    print(f"emp1: {emp1}")
    print(f"emp2: {emp2}")
    print(f"Зарплата валидна: {Employee.is_valid_salary(50000)}")


# ============================================================================
# ЗАДАЧА 4: Множественное наследование
# ============================================================================

class Flyable:
    """Миксин для летающих объектов"""
    
    def fly(self):
        return f"{self.__class__.__name__} летит"


class Swimmable:
    """Миксин для плавающих объектов"""
    
    def swim(self):
        return f"{self.__class__.__name__} плывет"


class Animal:
    """Базовый класс животного"""
    
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        return f"{self.name} издает звук"


class Duck(Animal, Flyable, Swimmable):
    """
    🔴 Senior level
    Утка - летает и плавает
    """
    
    def speak(self):
        return f"{self.name} говорит: Кря-кря!"


def demo_multiple_inheritance():
    duck = Duck("Дональд")
    
    print(duck.speak())
    print(duck.fly())
    print(duck.swim())
    
    print(f"\nMRO: {[c.__name__ for c in Duck.__mro__]}")


# ============================================================================
# ЗАДАЧА 5: Property декоратор
# ============================================================================

class Temperature:
    """
    🟡 Middle level
    Класс с property для геттеров и сеттеров
    """
    
    def __init__(self, celsius=0):
        self._celsius = celsius
    
    @property
    def celsius(self):
        """Геттер для Цельсия"""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        """Сеттер для Цельсия"""
        if value < -273.15:
            raise ValueError("Температура ниже абсолютного нуля!")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        """Фаренгейт (только для чтения)"""
        return self._celsius * 9/5 + 32
    
    @property
    def kelvin(self):
        """Кельвин (только для чтения)"""
        return self._celsius + 273.15


def demo_property():
    temp = Temperature(25)
    
    print(f"Цельсий: {temp.celsius}°C")
    print(f"Фаренгейт: {temp.fahrenheit}°F")
    print(f"Кельвин: {temp.kelvin}K")
    
    temp.celsius = 0
    print(f"\nПосле изменения: {temp.celsius}°C = {temp.fahrenheit}°F")


# ============================================================================
# ЗАДАЧА 6: Композиция vs Наследование
# ============================================================================

class Engine:
    """Двигатель (композиция)"""
    
    def __init__(self, horsepower):
        self.horsepower = horsepower
    
    def start(self):
        return f"Двигатель {self.horsepower}HP запущен"


class Car:
    """
    🟡 Middle level
    Автомобиль использует композицию (has-a relationship)
    """
    
    def __init__(self, brand, engine):
        self.brand = brand
        self.engine = engine  # Композиция
    
    def start(self):
        return f"{self.brand}: {self.engine.start()}"


def demo_composition():
    engine = Engine(200)
    car = Car("Toyota", engine)
    
    print(car.start())


# ============================================================================
# ЗАДАЧА 7: Паттерн Синглтон через класс
# ============================================================================

class Singleton:
    """
    🔴 Senior level
    Реализация паттерна Singleton через __new__
    """
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, value=None):
        if not hasattr(self, 'initialized'):
            self.value = value
            self.initialized = True


def demo_singleton():
    s1 = Singleton("first")
    s2 = Singleton("second")
    
    print(f"s1.value: {s1.value}")
    print(f"s2.value: {s2.value}")
    print(f"s1 is s2: {s1 is s2}")


# ============================================================================
# ЗАДАЧА 8: Дескрипторы
# ============================================================================

class PositiveNumber:
    """
    🔴 Senior level
    Дескриптор для проверки положительных чисел
    """
    
    def __init__(self, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, 0)
    
    def __set__(self, obj, value):
        if value < 0:
            raise ValueError(f"{self.name} должно быть положительным")
        obj.__dict__[self.name] = value


class Product:
    """Товар с дескрипторами"""
    
    price = PositiveNumber('price')
    quantity = PositiveNumber('quantity')
    
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def total_cost(self):
        return self.price * self.quantity


def demo_descriptor():
    product = Product("Laptop", 1000, 5)
    print(f"{product.name}: ${product.total_cost()}")
    
    try:
        product.price = -100
    except ValueError as e:
        print(f"Ошибка: {e}")


# ============================================================================
# ЗАДАЧА 9: Счетчик экземпляров
# ============================================================================

class CountedClass:
    """
    🟡 Middle level
    Класс, подсчитывающий количество экземпляров
    """
    
    instance_count = 0
    
    def __init__(self, name):
        self.name = name
        CountedClass.instance_count += 1
        self.instance_number = CountedClass.instance_count
    
    def __del__(self):
        CountedClass.instance_count -= 1
    
    def __str__(self):
        return f"Instance #{self.instance_number}: {self.name}"


def demo_counted():
    obj1 = CountedClass("First")
    obj2 = CountedClass("Second")
    obj3 = CountedClass("Third")
    
    print(f"Всего экземпляров: {CountedClass.instance_count}")
    print(obj1)
    print(obj2)
    print(obj3)


# ============================================================================
# ЗАДАЧА 10: Фабричный метод
# ============================================================================

class Pizza(ABC):
    """Базовый класс пиццы"""
    
    @abstractmethod
    def prepare(self):
        pass


class MargheritaPizza(Pizza):
    def prepare(self):
        return "Готовим Маргариту: тесто, томаты, моцарелла, базилик"


class PepperoniPizza(Pizza):
    def prepare(self):
        return "Готовим Пепперони: тесто, томаты, моцарелла, пепперони"


class PizzaFactory:
    """
    🟡 Middle level
    Фабрика для создания пицц
    """
    
    @staticmethod
    def create_pizza(pizza_type):
        if pizza_type == "margherita":
            return MargheritaPizza()
        elif pizza_type == "pepperoni":
            return PepperoniPizza()
        else:
            raise ValueError(f"Неизвестный тип пиццы: {pizza_type}")


def demo_factory():
    factory = PizzaFactory()
    
    pizza1 = factory.create_pizza("margherita")
    pizza2 = factory.create_pizza("pepperoni")
    
    print(pizza1.prepare())
    print(pizza2.prepare())


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("КЛАССЫ И НАСЛЕДОВАНИЕ - Примеры и тесты")
    print("=" * 60)
    
    # Тест 1: Простой класс
    print("\n1. Класс Point:")
    demo_point()
    
    # Тест 2: Наследование
    print("\n2. Наследование (фигуры):")
    demo_shapes()
    
    # Тест 3: Атрибуты класса
    print("\n3. Атрибуты класса и экземпляра:")
    demo_employee()
    
    # Тест 4: Множественное наследование
    print("\n4. Множественное наследование:")
    demo_multiple_inheritance()
    
    # Тест 5: Property
    print("\n5. Property декоратор:")
    demo_property()
    
    # Тест 6: Композиция
    print("\n6. Композиция:")
    demo_composition()
    
    # Тест 7: Синглтон
    print("\n7. Singleton:")
    demo_singleton()
    
    # Тест 8: Дескрипторы
    print("\n8. Дескрипторы:")
    demo_descriptor()
    
    # Тест 9: Счетчик экземпляров
    print("\n9. Счетчик экземпляров:")
    demo_counted()
    
    # Тест 10: Фабричный метод
    print("\n10. Фабричный метод:")
    demo_factory()
    
    print("\n" + "=" * 60)

