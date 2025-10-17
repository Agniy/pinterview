# run_in_executor() - Шпаргалка

## 📋 Основной синтаксис

```python
loop = asyncio.get_event_loop()
result = await loop.run_in_executor(executor, func, *args)
```

## 🔧 Типы Executor

### 1. ThreadPoolExecutor (для I/O операций)
```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=5) as executor:
    result = await loop.run_in_executor(executor, blocking_io_func, arg1, arg2)
```

**Когда использовать:**
- Чтение/запись файлов
- Запросы к БД
- Сетевые запросы (если нет async версии)
- Любые блокирующие I/O операции

### 2. ProcessPoolExecutor (для CPU операций)
```python
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor(max_workers=2) as executor:
    result = await loop.run_in_executor(executor, cpu_intensive_func, arg)
```

**Когда использовать:**
- Тяжелые вычисления
- Обработка изображений
- Математические операции
- Все, что нагружает CPU

### 3. Default Executor (None)
```python
result = await loop.run_in_executor(None, func, arg)
```

**Особенности:**
- Использует встроенный ThreadPoolExecutor
- Обычно 5 потоков
- Удобно для простых случаев

## 🎯 Практические примеры

### Параллельная обработка
```python
async def process_multiple():
    loop = asyncio.get_event_loop()
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        tasks = [
            loop.run_in_executor(executor, blocking_func, item)
            for item in items
        ]
        results = await asyncio.gather(*tasks)
    
    return results
```

### С таймаутом
```python
async def with_timeout():
    loop = asyncio.get_event_loop()
    
    task = loop.run_in_executor(None, slow_func)
    try:
        result = await asyncio.wait_for(task, timeout=5.0)
    except asyncio.TimeoutError:
        print("Превышен таймаут!")
```

### Ограничение конкурентности
```python
async def limited_concurrency():
    semaphore = asyncio.Semaphore(3)  # Макс 3 одновременно
    loop = asyncio.get_event_loop()
    
    async def limited_call(item):
        async with semaphore:
            return await loop.run_in_executor(None, blocking_func, item)
    
    tasks = [limited_call(item) for item in items]
    results = await asyncio.gather(*tasks)
```

### Обработка ошибок
```python
async def error_handling():
    loop = asyncio.get_event_loop()
    
    tasks = [
        loop.run_in_executor(None, risky_func, i)
        for i in range(5)
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Ошибка в задаче {i}: {result}")
```

## ⚡ Сравнение производительности

| Тип | Overhead | GIL | Use Case | Макс Workers |
|-----|----------|-----|----------|--------------|
| ThreadPool | Низкий | Да | I/O операции | ~10-50 |
| ProcessPool | Высокий | Нет | CPU операции | ~CPU cores |
| Default | Низкий | Да | Простые случаи | ~5 |

## ⚠️ Типичные ошибки

### ❌ НЕ ДЕЛАЙ ТАК:

```python
# 1. Запуск async функции в executor
async def async_func():
    await asyncio.sleep(1)

# НЕПРАВИЛЬНО!
await loop.run_in_executor(None, async_func)  # Ошибка!

# 2. Забывание про GIL
# НЕПРАВИЛЬНО для CPU-задач!
with ThreadPoolExecutor() as executor:  # Не поможет с CPU!
    await loop.run_in_executor(executor, heavy_cpu_task)

# 3. Слишком много workers
# НЕПРАВИЛЬНО!
with ThreadPoolExecutor(max_workers=1000) as executor:  # Слишком много!
    ...
```

### ✅ ДЕЛАЙ ТАК:

```python
# 1. Только sync функции в executor
def sync_func():
    time.sleep(1)
    return "done"

await loop.run_in_executor(None, sync_func)  # Правильно!

# 2. ProcessPool для CPU
with ProcessPoolExecutor() as executor:
    await loop.run_in_executor(executor, heavy_cpu_task)  # Правильно!

# 3. Разумное количество workers
with ThreadPoolExecutor(max_workers=10) as executor:  # Правильно!
    ...
```

## 🎓 Вопросы для интервью

### Базовые:
1. **Q: Что делает `run_in_executor()`?**
   - A: Запускает синхронную функцию в отдельном потоке или процессе, возвращая awaitable

2. **Q: В чем разница между ThreadPool и ProcessPool?**
   - A: ThreadPool для I/O (общая память, GIL), ProcessPool для CPU (изоляция, без GIL)

3. **Q: Что происходит при executor=None?**
   - A: Используется default ThreadPoolExecutor с ограниченным количеством потоков

### Продвинутые:
1. **Q: Как ограничить количество одновременных вызовов?**
   - A: Используйте Semaphore или ограничьте max_workers в executor

2. **Q: Можно ли отменить задачу в executor?**
   - A: Отмена task не останавливает выполнение в executor, функция продолжит работу

3. **Q: Как обработать таймаут для executor?**
   - A: Используйте `asyncio.wait_for()` вокруг вызова run_in_executor

## 🔍 Best Practices

1. **Всегда используйте context manager**
   ```python
   with ThreadPoolExecutor() as executor:
       await loop.run_in_executor(executor, func)
   ```

2. **Устанавливайте таймауты**
   ```python
   await asyncio.wait_for(
       loop.run_in_executor(None, func),
       timeout=5.0
   )
   ```

3. **Ограничивайте конкурентность**
   ```python
   semaphore = asyncio.Semaphore(10)
   async with semaphore:
       await loop.run_in_executor(None, func)
   ```

4. **Обрабатывайте исключения**
   ```python
   results = await asyncio.gather(
       *tasks, 
       return_exceptions=True
   )
   ```

5. **Правильно завершайте executor**
   ```python
   executor.shutdown(wait=True)
   ```

## 📊 Когда использовать что

```
Блокирующий код?
├── Да → Используй run_in_executor
│   ├── I/O операция? → ThreadPoolExecutor
│   ├── CPU операция? → ProcessPoolExecutor
│   └── Простой случай? → Default (None)
└── Нет → Используй обычный async/await
```

## 🚀 Примеры из реальной жизни

### Обработка изображений
```python
from PIL import Image

def process_image(path):
    img = Image.open(path)
    img.thumbnail((200, 200))
    img.save(f"thumb_{path}")

async def process_all_images(paths):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        tasks = [
            loop.run_in_executor(executor, process_image, path)
            for path in paths
        ]
        await asyncio.gather(*tasks)
```

### Запросы к БД
```python
import sqlite3

def db_query(query):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

async def fetch_data(queries):
    loop = asyncio.get_event_loop()
    semaphore = asyncio.Semaphore(5)  # Макс 5 подключений
    
    async def limited_query(q):
        async with semaphore:
            return await loop.run_in_executor(None, db_query, q)
    
    tasks = [limited_query(q) for q in queries]
    return await asyncio.gather(*tasks)
```

## 📚 Дополнительные ресурсы

- [asyncio docs](https://docs.python.org/3/library/asyncio.html)
- [concurrent.futures docs](https://docs.python.org/3/library/concurrent.futures.html)
- [Understanding GIL](https://realpython.com/python-gil/)

