# 🟡 Алгоритмы и структуры данных

Коллекция алгоритмов с временной и пространственной сложностью для подготовки к собеседованиям.

## 📚 Содержание

- [Рекурсия](#рекурсия)
- [Поиск](#поиск)
- [Сортировка](#сортировка)
- [Вычисления](#вычисления)

## 📁 Структура файлов

Каждый алгоритм находится в отдельном файле с подробным описанием, пошаговым исполнением и примерами использования.

```
algorithms/
├── sorting/              # Алгоритмы сортировки
│   ├── bubble_sort.py    # Пузырьковая сортировка
│   ├── selection_sort.py # Сортировка выбором
│   ├── insertion_sort.py # Сортировка вставками
│   ├── merge_sort.py     # Сортировка слиянием
│   └── quick_sort.py     # Быстрая сортировка
├── searching/            # Алгоритмы поиска
│   ├── linear_search.py  # Линейный поиск
│   ├── binary_search.py  # Бинарный поиск
│   ├── dfs.py           # Поиск в глубину
│   └── bfs.py           # Поиск в ширину
├── recursion/            # Рекурсивные алгоритмы
│   ├── factorial.py     # Факториал
│   └── fibonacci.py     # Числа Фибоначчи
└── calculating/          # Вычислительные алгоритмы
    ├── max_consecutive.py # Максимальная последовательность
    └── subarray_sum.py    # Поиск подмассива с заданной суммой
```

---

## 🔄 Рекурсия

### Факториал (`factorial.py`)
| Алгоритм | Временная сложность | Пространственная сложность | Уровень |
|----------|---------------------|----------------------------|---------|
| `factorial` | O(n) | O(n) стек | 🟢 Junior |
| `factorial_iterative` | O(n) | O(1) | 🟢 Junior |
| `factorial_memoized` | O(n) | O(n) | 🟡 Middle |
| `factorial_big_int` | O(n) | O(1) | 🟡 Middle |

**Пошаговое исполнение:**
```
factorial(4):
  factorial(4) → 4 * factorial(3)
    factorial(3) → 3 * factorial(2)
      factorial(2) → 2 * factorial(1)
        factorial(1) → 1 (базовый случай)
      factorial(2) → 2 * 1 = 2
    factorial(3) → 3 * 2 = 6
  factorial(4) → 4 * 6 = 24
```

### Числа Фибоначчи (`fibonacci.py`)
| Алгоритм | Временная сложность | Пространственная сложность | Уровень |
|----------|---------------------|----------------------------|---------|
| `fibonacci_naive` | O(2^n) | O(n) стек | 🟢 Junior |
| `fibonacci_memoized` | O(n) | O(n) | 🟡 Middle |
| `fibonacci_iterative` | O(n) | O(1) | 🟡 Middle |
| `fibonacci_matrix` | O(log n) | O(log n) | 🔴 Senior |

**Пошаговое исполнение:**
```
fibonacci(5) с мемоизацией:
  fibonacci(5) → fibonacci(4) + fibonacci(3)
    fibonacci(4) → fibonacci(3) + fibonacci(2)
      fibonacci(3) → fibonacci(2) + fibonacci(1)
        fibonacci(2) → fibonacci(1) + fibonacci(0)
          fibonacci(1) → 1
          fibonacci(0) → 0
        fibonacci(2) → 1 + 0 = 1
      fibonacci(3) → 1 + 1 = 2
    fibonacci(4) → 2 + 1 = 3
  fibonacci(5) → 3 + 2 = 5
```

### Ключевые концепции:
- Базовый случай (base case)
- Хвостовая рекурсия
- Мемоизация
- Backtracking
- Динамическое программирование

---

## 🔍 Поиск

### Линейный поиск (`linear_search.py`)
| Алгоритм | Временная сложность | Пространственная сложность | Уровень |
|----------|---------------------|----------------------------|---------|
| `linear_search` | O(n) | O(1) | 🟢 Junior |
| `linear_search_all_occurrences` | O(n) | O(k) | 🟡 Middle |
| `linear_search_with_sentinel` | O(n) | O(1) | 🟡 Middle |

**Пошаговое исполнение:**
```
linear_search([1, 3, 5, 7, 9], 5):
  Шаг 1: Проверяем arr[0] = 1 ≠ 5
  Шаг 2: Проверяем arr[1] = 3 ≠ 5  
  Шаг 3: Проверяем arr[2] = 5 = 5 ✓
  Результат: индекс 2
```

### Бинарный поиск (`binary_search.py`)
| Алгоритм | Временная сложность | Пространственная сложность | Уровень |
|----------|---------------------|----------------------------|---------|
| `binary_search` | O(log n) | O(1) | 🟢 Junior |
| `binary_search_recursive` | O(log n) | O(log n) стек | 🟡 Middle |
| `find_first_occurrence` | O(log n) | O(1) | 🟡 Middle |
| `find_last_occurrence` | O(log n) | O(1) | 🟡 Middle |
| `search_rotated_array` | O(log n) | O(1) | 🔴 Senior |

**Пошаговое исполнение:**
```
binary_search([1, 3, 5, 7, 9, 11], 7):
  Шаг 1: left=0, right=5, mid=2, arr[2]=5 < 7
  Шаг 2: left=3, right=5, mid=4, arr[4]=9 > 7
  Шаг 3: left=3, right=3, mid=3, arr[3]=7 = 7 ✓
  Результат: индекс 3
```

### DFS (`dfs.py`)
| Алгоритм | Временная сложность | Пространственная сложность | Уровень |
|----------|---------------------|----------------------------|---------|
| `dfs_recursive` | O(V + E) | O(V) | 🟡 Middle |
| `dfs_iterative` | O(V + E) | O(V) | 🟡 Middle |
| `dfs_path` | O(V + E) | O(V) | 🟡 Middle |
| `dfs_cycle_detection` | O(V + E) | O(V) | 🟡 Middle |

### BFS (`bfs.py`)
| Алгоритм | Временная сложность | Пространственная сложность | Уровень |
|----------|---------------------|----------------------------|---------|
| `bfs` | O(V + E) | O(V) | 🟡 Middle |
| `shortest_path` | O(V + E) | O(V) | 🟡 Middle |
| `bfs_levels` | O(V + E) | O(V) | 🟡 Middle |
| `bfs_bidirectional` | O(V + E) | O(V) | 🔴 Senior |

**V** - количество вершин, **E** - количество рёбер

### Ключевые концепции:
- Линейный vs Бинарный поиск
- DFS (Depth-First Search) - поиск в глубину
- BFS (Breadth-First Search) - поиск в ширину
- Бинарный поиск в модифицированных структурах

---

## 📊 Сортировка

### Bubble Sort (`bubble_sort.py`)
| Алгоритм | Временная сложность | Пространственная сложность | Стабильность | Уровень |
|----------|---------------------|----------------------------|--------------|---------|
| `bubble_sort` | O(n²) | O(1) | ✅ Да | 🟢 Junior |

**Пошаговое исполнение:**
```
bubble_sort([5, 2, 8, 1, 9]):
  Проход 1: [5,2,8,1,9] → [2,5,1,8,9] → [2,1,5,8,9] → [1,2,5,8,9]
  Проход 2: [1,2,5,8,9] → без изменений
  Результат: [1, 2, 5, 8, 9]
```

### Selection Sort (`selection_sort.py`)
| Алгоритм | Временная сложность | Пространственная сложность | Стабильность | Уровень |
|----------|---------------------|----------------------------|--------------|---------|
| `selection_sort` | O(n²) | O(1) | ❌ Нет | 🟢 Junior |

**Пошаговое исполнение:**
```
selection_sort([5, 2, 8, 1, 9]):
  Итерация 1: min=1, меняем с arr[0], результат: [1, 2, 8, 5, 9]
  Итерация 2: min=2, уже на месте, результат: [1, 2, 8, 5, 9]
  Итерация 3: min=5, меняем с arr[2], результат: [1, 2, 5, 8, 9]
  Итерация 4: min=8, уже на месте, результат: [1, 2, 5, 8, 9]
```

### Insertion Sort (`insertion_sort.py`)
| Алгоритм | Временная сложность | Пространственная сложность | Стабильность | Уровень |
|----------|---------------------|----------------------------|--------------|---------|
| `insertion_sort` | O(n²) | O(1) | ✅ Да | 🟢 Junior |

### Merge Sort (`merge_sort.py`)
| Алгоритм | Временная сложность | Пространственная сложность | Стабильность | Уровень |
|----------|---------------------|----------------------------|--------------|---------|
| `merge_sort` | O(n log n) | O(n) | ✅ Да | 🟡 Middle |

**Пошаговое исполнение:**
```
merge_sort([6, 3, 8, 1]):
  Разделяем: [6,3] и [8,1]
    Разделяем [6,3]: [6] и [3]
      Сливаем: [3,6]
    Разделяем [8,1]: [8] и [1]  
      Сливаем: [1,8]
  Сливаем [3,6] и [1,8]: [1,3,6,8]
```

### Quick Sort (`quick_sort.py`)
| Алгоритм | Временная сложность | Пространственная сложность | Стабильность | Уровень |
|----------|---------------------|----------------------------|--------------|---------|
| `quick_sort` | O(n log n) сред., O(n²) худ. | O(log n) стек | ❌ Нет | 🟡 Middle |

**Пошаговое исполнение:**
```
quick_sort([5, 2, 8, 1, 9], pivot=9):
  Разделение: [5,2,8,1] | 9 → [1,2] | 5 | [8] | 9
  Рекурсивно: [1,2] и [8]
  Результат: [1, 2, 5, 8, 9]
```

### Ключевые концепции:
- Стабильная vs Нестабильная сортировка
- In-place vs Not in-place
- Алгоритмы разделяй и властвуй
- Адаптивные алгоритмы

---

## 🧮 Вычисления

### Максимальная последовательность (`calculating/max_consecutive.py`)
| Алгоритм | Временная сложность | Пространственная сложность | Уровень |
|----------|---------------------|----------------------------|---------|
| `max_consecutive_elements` | O(n) | O(1) | 🟡 Middle |
| `max_consecutive_with_char` | O(n) | O(1) | 🟡 Middle |
| `all_consecutive_sequences` | O(n) | O(k) | 🟡 Middle |

**k** - количество различных последовательностей

**Пошаговое исполнение:**
```
max_consecutive_elements("aaabbbcc"):
  cur_idx=0: next_idx=3, длина=3
  cur_idx=3: next_idx=6, длина=3  
  cur_idx=6: next_idx=8, длина=2
  Результат: max(3,3,2) = 3
```

### Поиск подмассива с заданной суммой (`calculating/subarray_sum.py`)
| Алгоритм | Временная сложность | Пространственная сложность | Уровень |
|----------|---------------------|----------------------------|---------|
| `subarray_sum` (вариант 1) | O(n) | O(1) | 🟡 Middle |
| `subarray_sum_prefix_sums` (вариант 2) | O(n) | O(n) | 🟡 Middle |
| `subarray_sum_with_indices` | O(n) | O(1) | 🟡 Middle |
| `subarray_sum_all_occurrences` | O(n) | O(k) | 🟡 Middle |
| `subarray_sum_with_negative` | O(n) | O(n) | 🟡 Middle |

**k** - количество найденных подмассивов

**Вариант 1 (Скользящее окно):**
```
subarray_sum([1, 4, 20, 3, 10, 5], 33):
  left=0: right=0→3, сумма=0→28→31, окно=[1,4,20,3]
  left=1: right=3→5, сумма=31→34, окно=[20,3,10]  
  left=2: right=5, сумма=34→33, окно=[20,3,10] ✓
  Результат: True
```

**Вариант 2 (Префиксные суммы):**
```
subarray_sum_prefix_sums([1, 4, 20, 3, 10, 5], 33):
  i=0: current_sum=1, ищем -32, сохраняем {1:0}
  i=1: current_sum=5, ищем -28, сохраняем {5:1}
  i=2: current_sum=25, ищем -8, сохраняем {25:2}
  i=3: current_sum=28, ищем -5, найдено! подмассив[1:4] ✓
  Результат: True
```

---

## 📈 Сравнение сложностей

### От лучшей к худшей:

1. **O(1)** - константная
2. **O(log n)** - логарифмическая (бинарный поиск)
3. **O(n)** - линейная
4. **O(n log n)** - линеарифмическая (эффективная сортировка)
5. **O(n²)** - квадратичная (простые сортировки)
6. **O(2^n)** - экспоненциальная (подмножества)
7. **O(n!)** - факториальная (перестановки)

---

## 🎯 Рекомендации по выбору алгоритма

### Сортировка:
- **Малые массивы (n < 50)**: Insertion Sort
- **Большие массивы**: Merge Sort, Quick Sort, Heap Sort
- **Почти отсортированные**: Insertion Sort, Bubble Sort
- **Ограничения по памяти**: Heap Sort, Quick Sort (in-place)
- **Стабильность важна**: Merge Sort, Timsort
- **Целые числа в диапазоне**: Counting Sort

### Поиск:
- **Неотсортированный массив**: Linear Search - O(n)
- **Отсортированный массив**: Binary Search - O(log n)
- **Граф (кратчайший путь)**: BFS
- **Граф (все вершины)**: DFS или BFS
- **Дерево (поиск)**: DFS

---

## 🔧 Как использовать

### Запуск примеров:

```bash
# Активировать виртуальное окружение
source .venv/bin/activate

# Запустить примеры отдельных алгоритмов
python algorithms/recursion/factorial.py
python algorithms/recursion/fibonacci.py
python algorithms/searching/linear_search.py
python algorithms/searching/binary_search.py
python algorithms/searching/dfs.py
python algorithms/searching/bfs.py
python algorithms/sorting/bubble_sort.py
python algorithms/sorting/selection_sort.py
python algorithms/sorting/insertion_sort.py
python algorithms/sorting/merge_sort.py
python algorithms/sorting/quick_sort.py
python algorithms/calculating/max_consecutive.py
python algorithms/calculating/subarray_sum.py
```

### Импорт в свой код:

```python
# Импорт отдельных алгоритмов
from algorithms.recursion.factorial import factorial, factorial_iterative
from algorithms.recursion.fibonacci import fibonacci_memoized, fibonacci_iterative
from algorithms.searching.linear_search import linear_search
from algorithms.searching.binary_search import binary_search, find_first_occurrence
from algorithms.searching.dfs import dfs_recursive, dfs_iterative
from algorithms.searching.bfs import bfs, shortest_path
from algorithms.sorting.bubble_sort import bubble_sort
from algorithms.sorting.selection_sort import selection_sort
from algorithms.sorting.insertion_sort import insertion_sort
from algorithms.sorting.merge_sort import merge_sort
from algorithms.sorting.quick_sort import quick_sort
from algorithms.calculating.max_consecutive import max_consecutive_elements
from algorithms.calculating.subarray_sum import subarray_sum, subarray_sum_prefix_sums, subarray_sum_with_indices

# Или импорт из модулей
from algorithms.recursion import factorial, fibonacci_memoized
from algorithms.searching import binary_search, bfs, dfs_recursive
from algorithms.sorting import merge_sort, quick_sort, bubble_sort
from algorithms.calculating import max_consecutive_elements, subarray_sum, subarray_sum_prefix_sums

# Использование
result = binary_search([1, 2, 3, 4, 5], 3)
sorted_arr = merge_sort([3, 1, 4, 1, 5, 9])
max_seq = max_consecutive_elements("aaabbbcc")
subarray_found = subarray_sum([1, 4, 20, 3, 10, 5], 33)
subarray_found_v2 = subarray_sum_prefix_sums([1, 4, 20, 3, 10, 5], 33)
fib_num = fibonacci_memoized(10)
```

### Тестирование с пошаговым исполнением:

```python
# Включить пошаговое исполнение
from algorithms.sorting.bubble_sort import bubble_sort_with_steps
from algorithms.searching.binary_search import binary_search_with_steps
from algorithms.recursion.factorial import factorial_with_steps
from algorithms.calculating.subarray_sum import subarray_sum_with_steps, subarray_sum_prefix_sums_with_steps

# Запустить с выводом шагов
bubble_sort_with_steps([5, 2, 8, 1, 9])
binary_search_with_steps([1, 3, 5, 7, 9, 11], 7)
factorial_with_steps(5)
subarray_sum_with_steps([1, 4, 20, 3, 10, 5], 33)
subarray_sum_prefix_sums_with_steps([1, 4, 20, 3, 10, 5], 33)
```

---

## 📝 Легенда

- 🟢 **Junior** - базовые алгоритмы, необходимые на начальном уровне
- 🟡 **Middle** - алгоритмы среднего уровня сложности
- 🔴 **Senior** - сложные алгоритмы для продвинутого уровня

---

## 🎓 Дополнительные ресурсы

### Теория:
- Введение в алгоритмы (Кормен)
- Грокаем алгоритмы (Адитья Бхаргава)
- LeetCode, HackerRank, CodeWars

### Сложность алгоритмов:
- [Big O Cheat Sheet](https://www.bigocheatsheet.com/)
- [Time Complexity Visualization](https://www.cs.usfca.edu/~galles/visualization/Algorithms.html)

---

**Последнее обновление:** 2025

**Автор:** agniy

