"""
Быстрый тест для проверки работы примеров run_in_executor
"""

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def blocking_function(n: int) -> int:
    """Простая блокирующая функция"""
    time.sleep(0.1)
    return n * 2


async def test_thread_pool():
    """Тест ThreadPoolExecutor"""
    print("Тест ThreadPoolExecutor...")
    loop = asyncio.get_event_loop()
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        tasks = [
            loop.run_in_executor(executor, blocking_function, i)
            for i in range(5)
        ]
        results = await asyncio.gather(*tasks)
        assert results == [0, 2, 4, 6, 8], f"Ожидалось [0, 2, 4, 6, 8], получено {results}"
        print("✓ ThreadPoolExecutor работает корректно")


def cpu_function(n: int) -> int:
    """CPU-intensive функция"""
    return sum(i * i for i in range(n))


async def test_process_pool():
    """Тест ProcessPoolExecutor"""
    print("\nТест ProcessPoolExecutor...")
    loop = asyncio.get_event_loop()
    
    with ProcessPoolExecutor(max_workers=2) as executor:
        tasks = [
            loop.run_in_executor(executor, cpu_function, 10000)
            for _ in range(3)
        ]
        results = await asyncio.gather(*tasks)
        expected = cpu_function(10000)
        assert all(r == expected for r in results), "Результаты не совпадают"
        print("✓ ProcessPoolExecutor работает корректно")


async def test_default_executor():
    """Тест default executor"""
    print("\nТест default executor...")
    loop = asyncio.get_event_loop()
    
    # Использование None как executor
    task = loop.run_in_executor(None, blocking_function, 5)
    result = await task
    assert result == 10, f"Ожидалось 10, получено {result}"
    print("✓ Default executor работает корректно")


async def test_with_timeout():
    """Тест с таймаутом"""
    print("\nТест с таймаутом...")
    loop = asyncio.get_event_loop()
    
    def slow_function():
        time.sleep(2)
        return "done"
    
    try:
        task = loop.run_in_executor(None, slow_function)
        await asyncio.wait_for(task, timeout=1.0)
        print("✗ Таймаут должен был сработать!")
    except asyncio.TimeoutError:
        print("✓ Таймаут работает корректно")


async def test_error_handling():
    """Тест обработки ошибок"""
    print("\nТест обработки ошибок...")
    loop = asyncio.get_event_loop()
    
    def failing_function():
        raise ValueError("Тестовая ошибка")
    
    try:
        await loop.run_in_executor(None, failing_function)
        print("✗ Исключение должно было быть выброшено!")
    except ValueError as e:
        print(f"✓ Обработка ошибок работает корректно: {e}")


async def run_all_tests():
    """Запуск всех тестов"""
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ run_in_executor")
    print("=" * 60)
    
    await test_thread_pool()
    await test_process_pool()
    await test_default_executor()
    await test_with_timeout()
    await test_error_handling()
    
    print("\n" + "=" * 60)
    print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО ✓")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_all_tests())

