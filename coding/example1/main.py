#!/usr/bin/env python3
"""
Главный файл для демонстрации системы анализа логов.

Запуск:
    python main.py                    # Использует sample_logs.txt
    python main.py <path/to/log>      # Использует указанный файл
"""

import sys
from pathlib import Path
from log_analyzer import LogParser, LogAnalyzer, LogFilter, print_summary


def main():
    """Главная функция приложения."""
    
    # Определяем файл для анализа
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
    else:
        log_file = 'sample_logs.txt'
    
    # Проверяем существование файла
    if not Path(log_file).exists():
        print(f"❌ Файл не найден: {log_file}")
        print(f"\nИспользование: python {sys.argv[0]} [путь_к_файлу]")
        return 1
    
    print("=" * 60)
    print("🔍 СИСТЕМА АНАЛИЗА ЛОГОВ ВЕБЕРСЕРВЕРА")
    print("=" * 60)
    print(f"\n📁 Анализируемый файл: {log_file}\n")
    
    try:
        # ШАГ 1: Парсинг файла
        print("⏳ Загрузка и парсинг логов...")
        parser = LogParser(log_file)
        logs = parser.parse()
        print(f"✅ Загружено записей: {len(logs)}\n")
        
        if not logs:
            print("⚠️  Валидные записи не найдены в файле.")
            return 0
        
        # ШАГ 2: Базовый анализ
        print("⏳ Анализ данных...\n")
        analyzer = LogAnalyzer(logs)
        
        # Выводим сводную статистику
        print_summary(analyzer)
        
        # ШАГ 3: Дополнительная аналитика
        print("\n" + "=" * 60)
        print("📊 ДОПОЛНИТЕЛЬНАЯ АНАЛИТИКА")
        print("=" * 60)
        
        # Анализ по часам
        print("\n⏰ Распределение запросов по часам:")
        hourly = analyzer.requests_by_hour()
        for hour in sorted(hourly.keys()):
            bar = '█' * (hourly[hour] // 2)  # Простая гистограмма
            print(f"  {hour:02d}:00 - {hourly[hour]:3d} {bar}")
        
        # Анализ ошибок
        print("\n❌ Анализ ошибок:")
        errors = LogFilter(logs).by_status_range(400, 599).get_logs()
        
        if errors:
            error_analyzer = LogAnalyzer(errors)
            print(f"  Всего ошибок: {len(errors)}")
            print(f"  Типы ошибок:")
            
            for status, count in sorted(
                error_analyzer.count_by_status().items()
            ):
                print(f"    {status}: {count:3d} запросов")
            
            print(f"\n  URL с ошибками:")
            for url, count in error_analyzer.top_urls(5):
                print(f"    {count:3d} - {url}")
        else:
            print("  Ошибок не обнаружено! 🎉")
        
        # Анализ успешных запросов
        print("\n✅ Топ успешных endpoint'ов (2xx):")
        successful = LogFilter(logs).by_status_range(200, 299).get_logs()
        
        if successful:
            success_analyzer = LogAnalyzer(successful)
            for url, count in success_analyzer.top_urls(5):
                print(f"  {count:3d} - {url}")
        
        # Рекомендации
        print("\n" + "=" * 60)
        print("💡 РЕКОМЕНДАЦИИ")
        print("=" * 60)
        
        error_rate = analyzer.error_rate()
        
        if error_rate > 10:
            print("⚠️  Высокий процент ошибок (>10%)!")
            print("   Рекомендуется проверить:")
            print("   - Логи приложения на наличие исключений")
            print("   - Доступность зависимых сервисов")
            print("   - Правильность конфигурации")
        elif error_rate > 5:
            print("⚠️  Умеренный процент ошибок (>5%)")
            print("   Рекомендуется мониторинг")
        else:
            print("✅ Процент ошибок в норме (<5%)")
        
        # Проверяем 5xx ошибки
        server_errors = LogFilter(logs).by_status_range(500, 599).get_logs()
        if server_errors:
            print(f"\n⚠️  Обнаружены ошибки сервера (5xx): {len(server_errors)}")
            print("   Требуется срочная проверка приложения!")
        
        print("\n" + "=" * 60)
        print("✅ Анализ завершен успешно!")
        print("=" * 60)
        
        return 0
    
    except FileNotFoundError as e:
        print(f"❌ Ошибка: {e}")
        return 1
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Анализ прерван пользователем")
        return 130
    
    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

