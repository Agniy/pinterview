"""
Базовые примеры asyncio для интервью
Демонстрирует основные концепции и паттерны
"""

import asyncio
import time
import aiohttp
from typing import List, Dict, Any


# 1. Базовый async/await
async def basic_async_function():
    """Простейший пример асинхронной функции"""
    print("Начало выполнения")
    await asyncio.sleep(1)  # Имитация I/O операции
    print("Конец выполнения")
    return "Результат"


# 2. Запуск асинхронных функций
async def run_basic_example():
    """Демонстрация запуска асинхронной функции"""
    result = await basic_async_function()
    print(f"Получен результат: {result}")


# 3. Параллельное выполнение с asyncio.gather()
async def fetch_data(url: str, delay: float) -> Dict[str, Any]:
    """Имитация получения данных с задержкой"""
    await asyncio.sleep(delay)
    return {"url": url, "data": f"Данные с {url}", "timestamp": time.time()}


async def parallel_execution_example():
    """Демонстрация параллельного выполнения"""
    urls = [
        ("https://api.example.com/users", 1.0),
        ("https://api.example.com/posts", 1.5),
        ("https://api.example.com/comments", 0.8)
    ]
    
    # Последовательное выполнение
    start_time = time.time()
    sequential_results = []
    for url, delay in urls:
        result = await fetch_data(url, delay)
        sequential_results.append(result)
    sequential_time = time.time() - start_time
    
    # Параллельное выполнение
    start_time = time.time()
    tasks = [fetch_data(url, delay) for url, delay in urls]
    parallel_results = await asyncio.gather(*tasks)
    parallel_time = time.time() - start_time
    
    print(f"Последовательное выполнение: {sequential_time:.2f}с")
    print(f"Параллельное выполнение: {parallel_time:.2f}с")
    print(f"Ускорение: {sequential_time/parallel_time:.2f}x")


# 4. Работа с asyncio.create_task()
async def background_task(task_id: int, duration: float):
    """Фоновая задача"""
    print(f"Задача {task_id} началась")
    await asyncio.sleep(duration)
    print(f"Задача {task_id} завершена")
    return f"Результат задачи {task_id}"


async def task_management_example():
    """Демонстрация управления задачами"""
    # Создание задач
    task1 = asyncio.create_task(background_task(1, 2.0))
    task2 = asyncio.create_task(background_task(2, 1.5))
    task3 = asyncio.create_task(background_task(3, 1.0))
    
    # Ожидание завершения всех задач
    results = await asyncio.gather(task1, task2, task3)
    print("Все задачи завершены:", results)


# 5. Обработка исключений в asyncio
async def risky_operation(should_fail: bool):
    """Операция, которая может завершиться ошибкой"""
    await asyncio.sleep(0.5)
    if should_fail:
        raise ValueError("Что-то пошло не так!")
    return "Успех!"


async def exception_handling_example():
    """Демонстрация обработки исключений"""
    tasks = [
        asyncio.create_task(risky_operation(False)),
        asyncio.create_task(risky_operation(True)),
        asyncio.create_task(risky_operation(False))
    ]
    
    # Обработка с return_exceptions=True
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Задача {i+1} завершилась ошибкой: {result}")
        else:
            print(f"Задача {i+1} успешно: {result}")


# 6. asyncio.wait() с различными условиями
async def wait_example():
    """Демонстрация asyncio.wait()"""
    tasks = [
        asyncio.create_task(background_task(i, i * 0.5)) 
        for i in range(1, 6)
    ]
    
    # Ожидание завершения первой задачи
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    print(f"Завершено: {len(done)}, ожидает: {len(pending)}")
    
    # Отмена оставшихся задач
    for task in pending:
        task.cancel()
    
    # Ожидание отмены
    await asyncio.gather(*pending, return_exceptions=True)


# 7. Асинхронный контекстный менеджер
class AsyncResource:
    """Пример асинхронного ресурса"""
    
    async def __aenter__(self):
        print("Инициализация ресурса")
        await asyncio.sleep(0.1)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Освобождение ресурса")
        await asyncio.sleep(0.1)
    
    async def do_work(self):
        """Работа с ресурсом"""
        print("Выполнение работы")
        await asyncio.sleep(1)


async def async_context_manager_example():
    """Демонстрация асинхронного контекстного менеджера"""
    async with AsyncResource() as resource:
        await resource.do_work()


# 8. Асинхронный генератор
async def async_generator(n: int):
    """Асинхронный генератор"""
    for i in range(n):
        await asyncio.sleep(0.1)  # Имитация асинхронной операции
        yield i * i


async def async_generator_example():
    """Демонстрация асинхронного генератора"""
    async for value in async_generator(5):
        print(f"Получено значение: {value}")


# 9. Семафор для ограничения конкурентности
async def limited_concurrent_operation(semaphore: asyncio.Semaphore, task_id: int):
    """Операция с ограничением конкурентности"""
    async with semaphore:
        print(f"Задача {task_id} получила доступ к ресурсу")
        await asyncio.sleep(1)  # Имитация работы
        print(f"Задача {task_id} освободила ресурс")


async def semaphore_example():
    """Демонстрация использования семафора"""
    # Максимум 3 одновременных операции
    semaphore = asyncio.Semaphore(3)
    
    tasks = [
        asyncio.create_task(limited_concurrent_operation(semaphore, i))
        for i in range(10)
    ]
    
    await asyncio.gather(*tasks)


# 10. Event для координации задач
async def waiter(event: asyncio.Event, task_id: int):
    """Задача, ожидающая события"""
    print(f"Задача {task_id} ожидает события")
    await event.wait()
    print(f"Задача {task_id} получила событие!")


async def event_example():
    """Демонстрация использования Event"""
    event = asyncio.Event()
    
    # Создаем задачи-ожидатели
    waiters = [
        asyncio.create_task(waiter(event, i))
        for i in range(3)
    ]
    
    # Ждем немного, затем устанавливаем событие
    await asyncio.sleep(1)
    print("Устанавливаем событие!")
    event.set()
    
    await asyncio.gather(*waiters)


# Функция для запуска всех примеров
async def run_all_examples():
    """Запуск всех базовых примеров"""
    print("=== Базовые примеры asyncio ===\n")
    
    print("1. Базовый async/await:")
    await run_basic_example()
    print()
    
    print("2. Параллельное выполнение:")
    await parallel_execution_example()
    print()
    
    print("3. Управление задачами:")
    await task_management_example()
    print()
    
    print("4. Обработка исключений:")
    await exception_handling_example()
    print()
    
    print("5. asyncio.wait():")
    await wait_example()
    print()
    
    print("6. Асинхронный контекстный менеджер:")
    await async_context_manager_example()
    print()
    
    print("7. Асинхронный генератор:")
    await async_generator_example()
    print()
    
    print("8. Семафор:")
    await semaphore_example()
    print()
    
    print("9. Event:")
    await event_example()
    print()


if __name__ == "__main__":
    # Запуск всех примеров
    asyncio.run(run_all_examples())
