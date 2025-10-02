# Заметки для собеседований по Python

## 🎯 Общие советы

### Подготовка к собеседованию
1. **Понимание основ** - убедитесь, что знаете фундаментальные концепции
2. **Практика** - решайте задачи на платформах (LeetCode, HackerRank)
3. **Объяснение** - учитесь объяснять свой код вслух
4. **Сложность** - всегда думайте о временной и пространственной сложности

### Структура ответа на технический вопрос
1. **Уточните** требования и граничные случаи
2. **Подумайте вслух** - покажите свой мыслительный процесс
3. **Начните с простого** решения, затем оптимизируйте
4. **Тестируйте** код на примерах
5. **Обсудите** альтернативные решения

## 📊 Сложность алгоритмов (Big O)

### Основные сложности (от лучшей к худшей):
- O(1) - константная (доступ по индексу)
- O(log n) - логарифмическая (бинарный поиск)
- O(n) - линейная (проход по массиву)
- O(n log n) - линейно-логарифмическая (эффективная сортировка)
- O(n²) - квадратичная (вложенные циклы)
- O(2ⁿ) - экспоненциальная (рекурсивный Фибоначчи)
- O(n!) - факториальная (перебор всех перестановок)

### Сложность операций в Python:

**List:**
- Доступ: O(1)
- Поиск: O(n)
- Append: O(1) амортизированно
- Insert/Delete в начале: O(n)
- Insert/Delete в конце: O(1)

**Dict/Set:**
- Доступ/Поиск: O(1) в среднем
- Вставка/Удаление: O(1) в среднем
- Худший случай: O(n) при коллизиях

**Tuple:**
- Все операции как у list, но неизменяемый

## 🔑 Ключевые различия

### Mutable vs Immutable
**Mutable (изменяемые):**
- list, dict, set, user-defined classes

**Immutable (неизменяемые):**
- int, float, str, tuple, frozenset, bool

### Shallow Copy vs Deep Copy
```python
import copy

# Shallow copy - копирует только верхний уровень
shallow = list.copy() или list[:]

# Deep copy - рекурсивно копирует все вложенные объекты
deep = copy.deepcopy(list)
```

### `==` vs `is`
- `==` сравнивает значения
- `is` сравнивает идентичность (один и тот же объект в памяти)

## 🎨 Паттерны проектирования в Python

### Creational (Порождающие)
- **Singleton** - один экземпляр класса
- **Factory** - создание объектов без указания класса
- **Builder** - пошаговое создание сложных объектов

### Structural (Структурные)
- **Decorator** - добавление функциональности
- **Adapter** - согласование интерфейсов
- **Facade** - упрощенный интерфейс

### Behavioral (Поведенческие)
- **Iterator** - последовательный доступ к элементам
- **Observer** - уведомление об изменениях
- **Strategy** - выбор алгоритма во время выполнения

## 💡 Идиомы Python (Pythonic way)

### List Comprehensions
```python
# Вместо:
squares = []
for x in range(10):
    squares.append(x**2)

# Лучше:
squares = [x**2 for x in range(10)]
```

### Context Managers
```python
# Вместо:
f = open('file.txt')
try:
    content = f.read()
finally:
    f.close()

# Лучше:
with open('file.txt') as f:
    content = f.read()
```

### Enumerate
```python
# Вместо:
for i in range(len(items)):
    print(i, items[i])

# Лучше:
for i, item in enumerate(items):
    print(i, item)
```

### Zip
```python
# Вместо:
for i in range(len(names)):
    print(names[i], ages[i])

# Лучше:
for name, age in zip(names, ages):
    print(name, age)
```

## 🐍 Python-специфичные вопросы

### GIL (Global Interpreter Lock)
- Ограничивает выполнение только одного потока Python за раз
- Не проблема для I/O-bound задач
- Проблема для CPU-bound многопоточных программ
- Решение: multiprocessing вместо threading

### Duck Typing
"Если это ходит как утка и крякает как утка, то это утка"
- Python не проверяет тип, а проверяет наличие нужных методов

### EAFP vs LBYL
**EAFP** (Easier to Ask for Forgiveness than Permission):
```python
try:
    value = my_dict[key]
except KeyError:
    value = None
```

**LBYL** (Look Before You Leap):
```python
if key in my_dict:
    value = my_dict[key]
else:
    value = None
```

Python предпочитает EAFP!

## 📚 Популярные вопросы на собеседованиях

### Junior уровень
1. Разница между list и tuple?
2. Что такое list comprehension?
3. Как работает словарь?
4. Что такое lambda функция?
5. Разница между `==` и `is`?

### Middle уровень
1. Что такое декоратор и как его написать?
2. Что такое генератор и зачем он нужен?
3. Объясните GIL
4. В чем разница между `@staticmethod` и `@classmethod`?
5. Что такое замыкание?

### Senior уровень
1. Что такое метаклассы?
2. Как работает дескриптор?
3. Объясните MRO (Method Resolution Order)
4. Как реализовать свой контекстный менеджер?
5. Асинхронное программирование в Python

## 🔍 Частые алгоритмические задачи

1. **Two Sum** - найти два числа, дающие сумму
2. **Reverse String** - развернуть строку
3. **Valid Palindrome** - проверка палиндрома
4. **Merge Sorted Lists** - слить отсортированные списки
5. **Binary Search** - бинарный поиск
6. **Longest Substring** - самая длинная подстрока без повторений
7. **Maximum Subarray** - подмассив с максимальной суммой
8. **Valid Parentheses** - проверка скобочной последовательности
9. **LRU Cache** - реализация LRU кеша
10. **Tree Traversal** - обход дерева

## 🛠️ Полезные встроенные модули

- **collections** - Counter, defaultdict, deque, namedtuple
- **itertools** - chain, cycle, combinations, permutations
- **functools** - lru_cache, partial, wraps, reduce
- **heapq** - приоритетная очередь
- **bisect** - бинарный поиск в отсортированном списке
- **operator** - функции для операторов
- **copy** - shallow и deep copy
- **dataclasses** - удобные классы данных (Python 3.7+)

## 📖 Рекомендуемая литература

1. **"Fluent Python"** by Luciano Ramalho
2. **"Effective Python"** by Brett Slatkin
3. **"Python Cookbook"** by David Beazley
4. **"Cracking the Coding Interview"** by Gayle McDowell
5. **Official Python Documentation** - docs.python.org

## 🌐 Полезные ресурсы

- **LeetCode** - leetcode.com
- **HackerRank** - hackerrank.com
- **CodeWars** - codewars.com
- **Python Official Docs** - docs.python.org
- **Real Python** - realpython.com
- **Python Weekly** - pythonweekly.com

## ⚡ Советы для live-coding

1. **Читайте задачу внимательно** - уточните неясные моменты
2. **Обсудите подход** перед написанием кода
3. **Начните с примеров** - разберите входные/выходные данные
4. **Думайте о граничных случаях** - пустые входы, None, негативные числа
5. **Пишите читаемый код** - понятные имена переменных
6. **Тестируйте** - проверьте код на примерах
7. **Анализируйте сложность** - обсудите Big O
8. **Не паникуйте** - если застряли, объясните свои мысли

Удачи на собеседованиях! 🚀

