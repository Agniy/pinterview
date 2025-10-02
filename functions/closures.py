"""
🟡 ЗАМЫКАНИЯ (Closures) - Вопросы и задачи для собеседований

Основные темы:
- Область видимости (scope)
- Замыкания
- nonlocal
- Фабрики функций
"""


# ============================================================================
# ТЕОРЕТИЧЕСКИЕ ВОПРОСЫ
# ============================================================================

"""
Q1: Что такое замыкание (closure)?
A: Функция, которая "запоминает" значения из окружающей области видимости,
даже после того, как внешняя функция завершилась.

Q2: Когда используются замыкания?
A:
- Создание функций-фабрик
- Инкапсуляция данных
- Реализация декораторов
- Создание callback-функций

Q3: В чем разница между global и nonlocal?
A:
- global - доступ к переменной глобальной области
- nonlocal - доступ к переменной внешней функции (не глобальной)

Q4: Что такое LEGB правило?
A: Порядок поиска переменных:
- Local (локальная)
- Enclosing (во внешних функциях)
- Global (глобальная)
- Built-in (встроенная)
"""


# ============================================================================
# ЗАДАЧА 1: Простое замыкание - счетчик
# ============================================================================

def make_counter():
    """
    🟢 Junior level
    Создает функцию-счетчик
    """
    count = 0
    
    def counter():
        nonlocal count
        count += 1
        return count
    
    return counter


def demo_counter():
    counter1 = make_counter()
    counter2 = make_counter()
    
    print(f"counter1: {counter1()}")  # 1
    print(f"counter1: {counter1()}")  # 2
    print(f"counter2: {counter2()}")  # 1
    print(f"counter1: {counter1()}")  # 3


# ============================================================================
# ЗАДАЧА 2: Счетчик с reset
# ============================================================================

def make_counter_with_reset():
    """
    🟡 Middle level
    Счетчик с возможностью сброса
    """
    count = 0
    
    def counter():
        nonlocal count
        count += 1
        return count
    
    def reset():
        nonlocal count
        count = 0
    
    def get_count():
        return count
    
    # Возвращаем несколько функций
    counter.reset = reset
    counter.get_count = get_count
    
    return counter


def demo_counter_reset():
    counter = make_counter_with_reset()
    
    print(f"Вызов 1: {counter()}")
    print(f"Вызов 2: {counter()}")
    print(f"Текущее значение: {counter.get_count()}")
    counter.reset()
    print(f"После reset: {counter.get_count()}")


# ============================================================================
# ЗАДАЧА 3: Фабрика функций умножения
# ============================================================================

def make_multiplier(factor):
    """
    🟢 Junior level
    Создает функцию умножения на заданное число
    """
    def multiplier(number):
        return number * factor
    
    return multiplier


def demo_multiplier():
    double = make_multiplier(2)
    triple = make_multiplier(3)
    
    print(f"double(5) = {double(5)}")    # 10
    print(f"triple(5) = {triple(5)}")    # 15


# ============================================================================
# ЗАДАЧА 4: Фабрика функций-валидаторов
# ============================================================================

def make_validator(min_val, max_val):
    """
    🟡 Middle level
    Создает функцию валидации диапазона
    """
    def validator(value):
        if value < min_val:
            return f"Значение {value} меньше {min_val}"
        elif value > max_val:
            return f"Значение {value} больше {max_val}"
        else:
            return f"Значение {value} в диапазоне"
    
    return validator


def demo_validator():
    age_validator = make_validator(0, 120)
    percent_validator = make_validator(0, 100)
    
    print(age_validator(25))
    print(age_validator(150))
    print(percent_validator(50))
    print(percent_validator(101))


# ============================================================================
# ЗАДАЧА 5: Аккумулятор
# ============================================================================

def make_accumulator(initial=0):
    """
    🟡 Middle level
    Создает функцию-аккумулятор
    """
    total = initial
    
    def accumulator(value=0):
        nonlocal total
        total += value
        return total
    
    return accumulator


def demo_accumulator():
    acc = make_accumulator(100)
    
    print(f"Начальное: {acc()}")      # 100
    print(f"+ 10: {acc(10)}")         # 110
    print(f"+ 5: {acc(5)}")           # 115
    print(f"Текущее: {acc()}")        # 115


# ============================================================================
# ЗАДАЧА 6: Функция-генератор ID
# ============================================================================

def make_id_generator(prefix="ID"):
    """
    🟡 Middle level
    Создает генератор уникальных ID
    """
    counter = 0
    
    def generate():
        nonlocal counter
        counter += 1
        return f"{prefix}_{counter:04d}"
    
    return generate


def demo_id_generator():
    user_id = make_id_generator("USER")
    order_id = make_id_generator("ORDER")
    
    print(user_id())   # USER_0001
    print(user_id())   # USER_0002
    print(order_id())  # ORDER_0001


# ============================================================================
# ЗАДАЧА 7: Запоминание последнего вызова
# ============================================================================

def make_remembering_function(func):
    """
    🟡 Middle level
    Создает функцию, которая помнит последний вызов
    """
    last_args = None
    last_kwargs = None
    last_result = None
    
    def wrapper(*args, **kwargs):
        nonlocal last_args, last_kwargs, last_result
        
        last_args = args
        last_kwargs = kwargs
        last_result = func(*args, **kwargs)
        
        return last_result
    
    def get_last_call():
        return {
            'args': last_args,
            'kwargs': last_kwargs,
            'result': last_result
        }
    
    wrapper.get_last_call = get_last_call
    return wrapper


def demo_remembering():
    @make_remembering_function
    def add(a, b):
        return a + b
    
    add(5, 3)
    add(10, 20)
    
    last = add.get_last_call()
    print(f"Последний вызов: add{last['args']} = {last['result']}")


# ============================================================================
# ЗАДАЧА 8: Банковский счет
# ============================================================================

def make_bank_account(initial_balance=0):
    """
    🔴 Senior level
    Создает банковский счет с инкапсуляцией
    """
    balance = initial_balance
    transaction_history = []
    
    def deposit(amount):
        nonlocal balance
        if amount > 0:
            balance += amount
            transaction_history.append(('deposit', amount))
            return f"Депозит: {amount}. Баланс: {balance}"
        return "Сумма должна быть положительной"
    
    def withdraw(amount):
        nonlocal balance
        if amount > balance:
            return f"Недостаточно средств. Баланс: {balance}"
        if amount > 0:
            balance -= amount
            transaction_history.append(('withdraw', amount))
            return f"Снятие: {amount}. Баланс: {balance}"
        return "Сумма должна быть положительной"
    
    def get_balance():
        return balance
    
    def get_history():
        return transaction_history.copy()
    
    return {
        'deposit': deposit,
        'withdraw': withdraw,
        'balance': get_balance,
        'history': get_history
    }


def demo_bank_account():
    account = make_bank_account(1000)
    
    print(account['deposit'](500))
    print(account['withdraw'](200))
    print(account['withdraw'](2000))
    print(f"Баланс: {account['balance']()}")
    print(f"История: {account['history']()}")


# ============================================================================
# ЗАДАЧА 9: Частичное применение функции (partial)
# ============================================================================

def make_partial(func, *fixed_args, **fixed_kwargs):
    """
    🔴 Senior level
    Создает частично примененную функцию
    """
    def partial(*args, **kwargs):
        combined_args = fixed_args + args
        combined_kwargs = {**fixed_kwargs, **kwargs}
        return func(*combined_args, **combined_kwargs)
    
    return partial


def demo_partial():
    def power(base, exponent):
        return base ** exponent
    
    # Создаем функцию для квадрата
    square = make_partial(power, exponent=2)
    # Создаем функцию для куба
    cube = make_partial(power, exponent=3)
    
    print(f"square(5) = {square(5)}")  # 25
    print(f"cube(3) = {cube(3)}")      # 27


# ============================================================================
# ЗАДАЧА 10: Функция с приватным состоянием
# ============================================================================

def make_stateful_function():
    """
    🟡 Middle level
    Функция с приватным состоянием (список вызовов)
    """
    calls = []
    
    def function(value):
        calls.append(value)
        return sum(calls) / len(calls)  # Среднее всех вызовов
    
    def get_calls():
        return calls.copy()
    
    def clear():
        calls.clear()
    
    function.get_calls = get_calls
    function.clear = clear
    
    return function


def demo_stateful():
    avg = make_stateful_function()
    
    print(f"avg(10) = {avg(10)}")     # 10
    print(f"avg(20) = {avg(20)}")     # 15
    print(f"avg(30) = {avg(30)}")     # 20
    print(f"Вызовы: {avg.get_calls()}")


# ============================================================================
# ЗАДАЧА 11: Композиция функций через замыкания
# ============================================================================

def compose(*functions):
    """
    🔴 Senior level
    Создает композицию функций
    """
    def composed(x):
        result = x
        for func in reversed(functions):
            result = func(result)
        return result
    
    return composed


def demo_compose():
    def add_one(x):
        return x + 1
    
    def double(x):
        return x * 2
    
    def square(x):
        return x ** 2
    
    # (x + 1) * 2 ** 2
    f = compose(square, double, add_one)
    
    print(f"f(3) = {f(3)}")  # ((3 + 1) * 2) ** 2 = 64


# ============================================================================
# ЗАДАЧА 12: Кеш с TTL (Time To Live)
# ============================================================================

import time

def make_cache_with_ttl(ttl_seconds):
    """
    🔴 Senior level
    Создает кеш с временем жизни записей
    """
    cache = {}
    
    def get(key):
        if key in cache:
            value, timestamp = cache[key]
            if time.time() - timestamp < ttl_seconds:
                return value
            else:
                del cache[key]
        return None
    
    def set(key, value):
        cache[key] = (value, time.time())
    
    def clear():
        cache.clear()
    
    def size():
        # Удаляем устаревшие и возвращаем размер
        current_time = time.time()
        expired = [k for k, (_, ts) in cache.items() 
                   if current_time - ts >= ttl_seconds]
        for k in expired:
            del cache[k]
        return len(cache)
    
    return {
        'get': get,
        'set': set,
        'clear': clear,
        'size': size
    }


def demo_cache_ttl():
    cache = make_cache_with_ttl(ttl_seconds=2)
    
    cache['set']('key1', 'value1')
    print(f"Сразу: {cache['get']('key1')}")
    
    time.sleep(1)
    print(f"Через 1с: {cache['get']('key1')}")
    
    time.sleep(1.5)
    print(f"Через 2.5с: {cache['get']('key1')}")  # None


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("ЗАМЫКАНИЯ - Примеры и тесты")
    print("=" * 60)
    
    # Тест 1: Простой счетчик
    print("\n1. Простой счетчик:")
    demo_counter()
    
    # Тест 2: Счетчик с reset
    print("\n2. Счетчик с reset:")
    demo_counter_reset()
    
    # Тест 3: Фабрика множителей
    print("\n3. Фабрика функций умножения:")
    demo_multiplier()
    
    # Тест 4: Валидаторы
    print("\n4. Фабрика валидаторов:")
    demo_validator()
    
    # Тест 5: Аккумулятор
    print("\n5. Аккумулятор:")
    demo_accumulator()
    
    # Тест 6: Генератор ID
    print("\n6. Генератор ID:")
    demo_id_generator()
    
    # Тест 7: Запоминание вызова
    print("\n7. Запоминание последнего вызова:")
    demo_remembering()
    
    # Тест 8: Банковский счет
    print("\n8. Банковский счет:")
    demo_bank_account()
    
    # Тест 9: Частичное применение
    print("\n9. Частичное применение функции:")
    demo_partial()
    
    # Тест 10: Состояние
    print("\n10. Функция с состоянием:")
    demo_stateful()
    
    # Тест 11: Композиция
    print("\n11. Композиция функций:")
    demo_compose()
    
    # Тест 12: Кеш с TTL
    print("\n12. Кеш с TTL:")
    demo_cache_ttl()
    
    print("\n" + "=" * 60)

