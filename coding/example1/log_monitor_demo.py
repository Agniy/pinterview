#!/usr/bin/env python3
"""
Демонстрация real-time мониторинга логов (как tail -f)

Этот скрипт показывает, как отслеживать новые записи в лог-файле
в реальном времени и реагировать на события.

Запуск:
    python3 log_monitor_demo.py [log_file]
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

from log_analyzer import LogEntry
from log_analyzer_advanced import LogMonitor, AlertManager, AlertRule


def create_alert_rules() -> AlertManager:
    """
    Создает менеджер алертов с предопределенными правилами.
    
    Returns:
        Настроенный AlertManager
    """
    alert_mgr = AlertManager()
    
    # Правило 1: Критические ошибки сервера
    def critical_error(entry: LogEntry):
        print(f"\n🔴 КРИТИЧНО: Ошибка сервера!")
        print(f"   Статус: {entry.status}")
        print(f"   URL: {entry.path}")
        print(f"   IP: {entry.ip}")
        print(f"   Время: {entry.timestamp}")
    
    alert_mgr.add_rule(AlertRule(
        name="critical_errors",
        condition=lambda e: e.status >= 500,
        action=critical_error,
        cooldown=10.0
    ))
    
    # Правило 2: Неавторизованный доступ
    def unauthorized_access(entry: LogEntry):
        print(f"\n⚠️  ПРЕДУПРЕЖДЕНИЕ: Неавторизованный доступ")
        print(f"   IP: {entry.ip}")
        print(f"   URL: {entry.path}")
    
    alert_mgr.add_rule(AlertRule(
        name="unauthorized",
        condition=lambda e: e.status == 401,
        action=unauthorized_access,
        cooldown=30.0
    ))
    
    # Правило 3: 404 ошибки (возможные попытки сканирования)
    def not_found_alert(entry: LogEntry):
        print(f"\n⚠️  404: {entry.path} от {entry.ip}")
    
    alert_mgr.add_rule(AlertRule(
        name="not_found",
        condition=lambda e: e.status == 404,
        action=not_found_alert,
        cooldown=60.0
    ))
    
    # Правило 4: Большие ответы (возможная утечка данных)
    def large_response(entry: LogEntry):
        print(f"\n📊 ИНФО: Большой ответ")
        print(f"   Размер: {entry.size:,} байт")
        print(f"   URL: {entry.path}")
    
    alert_mgr.add_rule(AlertRule(
        name="large_response",
        condition=lambda e: e.size > 100000,  # > 100KB
        action=large_response,
        cooldown=120.0
    ))
    
    return alert_mgr


class RealTimeAnalyzer:
    """
    Анализатор в реальном времени.
    
    Собирает статистику и периодически выводит отчеты.
    """
    
    def __init__(self):
        self.total_requests = 0
        self.status_counts = {}
        self.method_counts = {}
        self.total_bytes = 0
        self.start_time = datetime.now()
    
    def process_entry(self, entry: LogEntry):
        """Обрабатывает новую запись."""
        self.total_requests += 1
        
        # Статус коды
        self.status_counts[entry.status] = \
            self.status_counts.get(entry.status, 0) + 1
        
        # HTTP методы
        self.method_counts[entry.method] = \
            self.method_counts.get(entry.method, 0) + 1
        
        # Размер
        self.total_bytes += entry.size
    
    def get_stats(self) -> str:
        """Возвращает текущую статистику."""
        uptime = datetime.now() - self.start_time
        
        stats = f"""
╔══════════════════════════════════════════════════════╗
║           СТАТИСТИКА В РЕАЛЬНОМ ВРЕМЕНИ              ║
╠══════════════════════════════════════════════════════╣
║ Время работы: {str(uptime).split('.')[0]:>37} ║
║ Всего запросов: {self.total_requests:>35} ║
║ Передано данных: {self.total_bytes:>34,} ║
╠══════════════════════════════════════════════════════╣
║ Статус коды:                                         ║
"""
        
        for status in sorted(self.status_counts.keys()):
            count = self.status_counts[status]
            stats += f"║   {status}: {count:>47} ║\n"
        
        stats += "╠══════════════════════════════════════════════════════╣\n"
        stats += "║ HTTP методы:                                         ║\n"
        
        for method, count in sorted(self.method_counts.items()):
            stats += f"║   {method}: {count:>47} ║\n"
        
        stats += "╚══════════════════════════════════════════════════════╝"
        
        return stats


async def monitor_with_stats(
    log_file: str,
    stats_interval: int = 10
):
    """
    Мониторинг с периодическим выводом статистики.
    
    Args:
        log_file: Путь к лог-файлу
        stats_interval: Интервал вывода статистики (секунды)
    """
    # Создаем анализаторы
    alert_mgr = create_alert_rules()
    analyzer = RealTimeAnalyzer()
    
    # Callback для обработки каждой записи
    def process_log(entry: LogEntry):
        # Показываем запись
        timestamp = entry.timestamp.strftime("%H:%M:%S")
        status_emoji = "✅" if entry.status < 400 else "❌"
        
        print(f"{status_emoji} [{timestamp}] {entry.method:6s} {entry.status} {entry.path:30s} {entry.size:>8,}b")
        
        # Обновляем статистику
        analyzer.process_entry(entry)
        
        # Проверяем алерты
        alert_mgr.check_entry(entry)
    
    # Создаем монитор
    monitor = LogMonitor(log_file, process_log, poll_interval=0.5)
    
    # Запускаем задачу вывода статистики
    async def print_stats_periodically():
        while True:
            await asyncio.sleep(stats_interval)
            print("\n" + analyzer.get_stats())
    
    # Запускаем обе задачи
    try:
        await asyncio.gather(
            monitor.start(),
            print_stats_periodically()
        )
    except KeyboardInterrupt:
        monitor.stop()
        print("\n\n" + analyzer.get_stats())
        print("\n✅ Мониторинг остановлен")


async def simulate_log_generation(log_file: str, duration: int = 30):
    """
    Генерирует тестовые логи для демонстрации.
    
    Args:
        log_file: Путь к файлу для записи
        duration: Длительность генерации (секунды)
    """
    import random
    from datetime import datetime, timezone
    
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    paths = [
        '/api/users', '/api/products', '/api/orders',
        '/api/login', '/api/logout', '/admin/dashboard',
        '/api/stats', '/health', '/'
    ]
    statuses = [200, 200, 200, 201, 204, 400, 401, 404, 500]
    ips = ['127.0.0.1', '192.168.1.1', '10.0.0.1', '172.16.0.1']
    
    print(f"🔄 Генерация тестовых логов в {log_file}")
    print(f"   Длительность: {duration} секунд")
    print(f"   Нажмите Ctrl+C для остановки\n")
    
    start_time = asyncio.get_event_loop().time()
    
    with open(log_file, 'a', encoding='utf-8') as f:
        while asyncio.get_event_loop().time() - start_time < duration:
            # Генерируем случайную запись
            ip = random.choice(ips)
            timestamp = datetime.now(timezone.utc)
            method = random.choice(methods)
            path = random.choice(paths)
            status = random.choice(statuses)
            size = random.randint(50, 10000)
            
            # Форматируем строку лога
            log_line = f'{ip} - - [{timestamp.strftime("%d/%b/%Y:%H:%M:%S %z")}] "{method} {path} HTTP/1.1" {status} {size}\n'
            
            f.write(log_line)
            f.flush()  # Сразу сбрасываем в файл
            
            # Случайная задержка
            await asyncio.sleep(random.uniform(0.1, 2.0))
    
    print(f"\n✅ Генерация логов завершена")


async def main():
    """Главная функция."""
    
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
    else:
        log_file = 'sample_logs.txt'
    
    # Проверяем существование файла
    if not Path(log_file).exists():
        print(f"⚠️  Файл {log_file} не найден")
        print(f"\nСоздать тестовый файл? (y/n): ", end='')
        
        response = input().lower()
        if response == 'y':
            # Создаем базовый файл
            with open(log_file, 'w') as f:
                f.write('127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /api/users HTTP/1.1" 200 1234\n')
            print(f"✅ Создан {log_file}")
        else:
            return
    
    print("=" * 60)
    print("🔍 REAL-TIME МОНИТОРИНГ ЛОГОВ")
    print("=" * 60)
    print(f"\n📁 Файл: {log_file}")
    print("\n💡 Выберите режим:")
    print("  1. Мониторинг существующего файла")
    print("  2. Генерация тестовых данных + мониторинг")
    print("\nВыбор (1/2): ", end='')
    
    choice = input().strip()
    
    if choice == '2':
        # Режим с генерацией данных
        print("\n🎬 Запуск в режиме демонстрации...")
        print("   Будут генерироваться случайные логи")
        print("   Нажмите Ctrl+C для остановки\n")
        
        await asyncio.sleep(1)
        
        # Запускаем генератор и монитор параллельно
        try:
            await asyncio.gather(
                simulate_log_generation(log_file, duration=60),
                monitor_with_stats(log_file, stats_interval=15)
            )
        except KeyboardInterrupt:
            print("\n\n⚠️  Остановлено пользователем")
    
    else:
        # Обычный мониторинг
        print("\n🎬 Запуск мониторинга...")
        print("   Ожидание новых записей в файле")
        print("   Нажмите Ctrl+C для остановки\n")
        
        await asyncio.sleep(1)
        
        try:
            await monitor_with_stats(log_file, stats_interval=30)
        except KeyboardInterrupt:
            print("\n\n⚠️  Мониторинг остановлен")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n✅ Программа завершена")
