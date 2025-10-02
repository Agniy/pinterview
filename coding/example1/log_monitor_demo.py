#!/usr/bin/env python3
"""
Демонстрация real-time мониторинга логов.

Запуск:
    python3 log_monitor_demo.py <log_file>
"""

import asyncio
import sys
from datetime import datetime
from log_analyzer_advanced import LogMonitor, AlertManager, AlertRule
from log_analyzer import LogEntry


def create_alert_system():
    """Создает систему алертов для мониторинга."""
    alert_mgr = AlertManager()
    
    # Алерт на ошибки сервера
    def server_error_alert(entry: LogEntry):
        print(f"\n🚨 [{datetime.now().strftime('%H:%M:%S')}] "
              f"ОШИБКА СЕРВЕРА: {entry.status} - {entry.method} {entry.path} "
              f"(IP: {entry.ip})")
    
    alert_mgr.add_rule(AlertRule(
        name="server_errors",
        condition=lambda e: e.status >= 500,
        action=server_error_alert,
        cooldown=10.0
    ))
    
    # Алерт на неавторизованный доступ
    def auth_error_alert(entry: LogEntry):
        print(f"\n⚠️  [{datetime.now().strftime('%H:%M:%S')}] "
              f"ОШИБКА АВТОРИЗАЦИИ: {entry.method} {entry.path} "
              f"(IP: {entry.ip})")
    
    alert_mgr.add_rule(AlertRule(
        name="auth_errors",
        condition=lambda e: e.status in (401, 403),
        action=auth_error_alert,
        cooldown=30.0
    ))
    
    # Алерт на большие ответы
    def large_response_alert(entry: LogEntry):
        size_mb = entry.size / (1024 * 1024)
        print(f"\n📦 [{datetime.now().strftime('%H:%M:%S')}] "
              f"БОЛЬШОЙ ОТВЕТ: {size_mb:.2f} MB - {entry.path}")
    
    alert_mgr.add_rule(AlertRule(
        name="large_responses",
        condition=lambda e: e.size > 1000000,  # > 1MB
        action=large_response_alert,
        cooldown=60.0
    ))
    
    return alert_mgr


async def monitor_with_stats(log_file: str):
    """
    Мониторит файл с выводом статистики.
    
    Args:
        log_file: Путь к лог-файлу
    """
    # Статистика
    stats = {
        'total': 0,
        'by_status': {},
        'by_method': {},
        'errors': 0
    }
    
    # Система алертов
    alert_mgr = create_alert_system()
    
    def process_entry(entry: LogEntry):
        """Обрабатывает каждую новую запись."""
        # Обновляем статистику
        stats['total'] += 1
        stats['by_status'][entry.status] = stats['by_status'].get(entry.status, 0) + 1
        stats['by_method'][entry.method] = stats['by_method'].get(entry.method, 0) + 1
        
        if entry.status >= 400:
            stats['errors'] += 1
        
        # Выводим запись
        status_emoji = "✅" if entry.status < 400 else "❌"
        print(f"{status_emoji} [{datetime.now().strftime('%H:%M:%S')}] "
              f"{entry.status} {entry.method:6s} {entry.path:30s} "
              f"({entry.size:6d} B)")
        
        # Проверяем алерты
        alert_mgr.check_entry(entry)
    
    # Создаем монитор
    monitor = LogMonitor(log_file, process_entry, poll_interval=0.5)
    
    # Запускаем задачи
    monitor_task = asyncio.create_task(monitor.start())
    
    # Задача для периодического вывода статистики
    async def print_stats_periodically():
        while monitor.running:
            await asyncio.sleep(30)  # Каждые 30 секунд
            
            if stats['total'] > 0:
                error_rate = (stats['errors'] / stats['total']) * 100
                
                print("\n" + "=" * 60)
                print(f"📊 СТАТИСТИКА (за период наблюдения)")
                print("=" * 60)
                print(f"Всего запросов: {stats['total']}")
                print(f"Ошибок: {stats['errors']} ({error_rate:.1f}%)")
                print(f"\nПо методам:")
                for method, count in sorted(stats['by_method'].items()):
                    print(f"  {method}: {count}")
                print(f"\nПо статусам:")
                for status, count in sorted(stats['by_status'].items()):
                    print(f"  {status}: {count}")
                print("=" * 60 + "\n")
    
    stats_task = asyncio.create_task(print_stats_periodically())
    
    try:
        # Ждем завершения
        await asyncio.gather(monitor_task, stats_task)
    except KeyboardInterrupt:
        print("\n\n⏹️  Мониторинг остановлен")
        monitor.stop()
        
        # Финальная статистика
        if stats['total'] > 0:
            print("\n" + "=" * 60)
            print("📊 ИТОГОВАЯ СТАТИСТИКА")
            print("=" * 60)
            print(f"Всего запросов: {stats['total']}")
            print(f"Ошибок: {stats['errors']}")
            
            # Алерты
            alert_stats = alert_mgr.get_alert_stats()
            print(f"\nСработало алертов: {alert_stats['total_alerts']}")
            if alert_stats['by_rule']:
                print("По типам:")
                for rule, count in alert_stats['by_rule'].items():
                    print(f"  {rule}: {count}")
            
            print("=" * 60)


def main():
    """Главная функция."""
    if len(sys.argv) < 2:
        print("Использование: python3 log_monitor_demo.py <log_file>")
        print("\nПример:")
        print("  python3 log_monitor_demo.py sample_logs.txt")
        print("\nДля генерации новых записей в другом терминале:")
        print("  echo '127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] \"GET /test HTTP/1.1\" 200 1234' >> sample_logs.txt")
        return 1
    
    log_file = sys.argv[1]
    
    print("=" * 60)
    print("🔍 REAL-TIME МОНИТОРИНГ ЛОГОВ")
    print("=" * 60)
    print(f"\n📁 Файл: {log_file}")
    print("\n⚡ Функции:")
    print("  • Отслеживание новых записей в реальном времени")
    print("  • Автоматические алерты при ошибках")
    print("  • Периодическая статистика (каждые 30 сек)")
    print("\n💡 Добавляйте новые строки в файл для тестирования")
    print("   Нажмите Ctrl+C для остановки\n")
    
    try:
        asyncio.run(monitor_with_stats(log_file))
    except KeyboardInterrupt:
        pass
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

