"""
Продвинутая система анализа логов веб-сервера

Расширенные возможности:
- Асинхронная обработка нескольких файлов
- Real-time мониторинг (tail -f)
- Система алертов
- Экспорт в JSON/CSV
- Продвинутые фильтры
- Агрегация по временным интервалам
"""

import asyncio
import json
import csv
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import List, Dict, Iterator, Callable, Optional, Any
from pathlib import Path
from collections import Counter, defaultdict
import time

# Импортируем базовые классы
from log_analyzer import LogEntry, LogParser, LogAnalyzer


# ============================================================================
# Асинхронный парсер
# ============================================================================

class AsyncLogParser:
    """
    Асинхронный парсер для обработки нескольких файлов параллельно.
    
    Преимущества:
    - Параллельная обработка I/O операций
    - Эффективное использование времени ожидания
    - Подходит для обработки множества файлов
    """
    
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.parser = LogParser(str(filepath))
    
    async def parse_async(self) -> List[LogEntry]:
        """
        Асинхронно парсит файл.
        
        Returns:
            Список всех записей из файла
        
        Note:
            Использует run_in_executor для выполнения синхронного кода
            в отдельном потоке, не блокируя event loop.
        """
        loop = asyncio.get_event_loop()
        
        # Запускаем синхронный парсинг в executor
        entries = await loop.run_in_executor(
            None,  # Использует default executor
            self.parser.parse
        )
        
        return entries
    
    async def parse_stream_async(
        self,
        chunk_size: int = 1000
    ) -> Iterator[List[LogEntry]]:
        """
        Асинхронно парсит файл батчами.
        
        Args:
            chunk_size: Размер батча
        
        Yields:
            Батчи LogEntry
        
        Полезно для обработки очень больших файлов.
        """
        loop = asyncio.get_event_loop()
        
        chunk = []
        for entry in self.parser.parse_stream():
            chunk.append(entry)
            
            if len(chunk) >= chunk_size:
                # Даем event loop возможность обработать другие задачи
                await asyncio.sleep(0)
                yield chunk
                chunk = []
        
        # Последний неполный батч
        if chunk:
            yield chunk


async def process_multiple_files(
    filepaths: List[str],
    progress_callback: Optional[Callable[[str, int], None]] = None
) -> Dict[str, List[LogEntry]]:
    """
    Обрабатывает несколько файлов параллельно.
    
    Args:
        filepaths: Список путей к файлам
        progress_callback: Функция для отчета о прогрессе
    
    Returns:
        Словарь {filename: logs}
    
    Example:
        >>> files = ['log1.txt', 'log2.txt', 'log3.txt']
        >>> results = await process_multiple_files(files)
        >>> for filename, logs in results.items():
        ...     print(f"{filename}: {len(logs)} записей")
    """
    
    async def parse_with_progress(filepath: str) -> tuple[str, List[LogEntry]]:
        """Парсит файл с отчетом о прогрессе"""
        parser = AsyncLogParser(filepath)
        logs = await parser.parse_async()
        
        if progress_callback:
            progress_callback(filepath, len(logs))
        
        return Path(filepath).name, logs
    
    # Создаем задачи для всех файлов
    tasks = [parse_with_progress(fp) for fp in filepaths]
    
    # Выполняем параллельно
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Обрабатываем результаты
    output = {}
    for result in results:
        if isinstance(result, Exception):
            print(f"Ошибка: {result}")
        else:
            filename, logs = result
            output[filename] = logs
    
    return output


# ============================================================================
# Real-time мониторинг
# ============================================================================

class LogMonitor:
    """
    Мониторинг лог-файла в реальном времени (как tail -f).
    
    Отслеживает новые строки в файле и обрабатывает их по мере появления.
    """
    
    def __init__(
        self,
        filepath: str,
        callback: Callable[[LogEntry], None],
        poll_interval: float = 0.5
    ):
        """
        Args:
            filepath: Путь к лог-файлу
            callback: Функция для обработки каждой новой записи
            poll_interval: Интервал проверки файла (секунды)
        """
        self.filepath = Path(filepath)
        self.callback = callback
        self.poll_interval = poll_interval
        self.parser = LogParser(str(filepath))
        self.running = False
    
    async def start(self):
        """
        Запускает мониторинг файла.
        
        Непрерывно проверяет файл на новые строки и обрабатывает их.
        """
        self.running = True
        
        # Открываем файл и переходим в конец
        with open(self.filepath, 'r', encoding='utf-8') as f:
            # Переходим в конец файла
            f.seek(0, 2)  # SEEK_END
            
            print(f"📡 Мониторинг {self.filepath}... (Ctrl+C для остановки)")
            
            while self.running:
                # Читаем новые строки
                line = f.readline()
                
                if line:
                    # Парсим и обрабатываем
                    entry = self.parser.parse_line(line)
                    if entry:
                        self.callback(entry)
                else:
                    # Нет новых данных, ждем
                    await asyncio.sleep(self.poll_interval)
    
    def stop(self):
        """Останавливает мониторинг."""
        self.running = False


# ============================================================================
# Система алертов
# ============================================================================

@dataclass
class AlertRule:
    """
    Правило для алерта.
    
    Определяет условие и действие при срабатывании.
    """
    name: str
    condition: Callable[[LogEntry], bool]
    action: Callable[[LogEntry], None]
    cooldown: float = 60.0  # Секунды между алертами
    last_triggered: Optional[float] = None
    
    def check(self, entry: LogEntry) -> bool:
        """
        Проверяет условие и выполняет действие.
        
        Returns:
            True если алерт сработал
        """
        if not self.condition(entry):
            return False
        
        # Проверяем cooldown
        now = time.time()
        if self.last_triggered:
            if now - self.last_triggered < self.cooldown:
                return False  # Cooldown еще активен
        
        # Выполняем действие
        self.action(entry)
        self.last_triggered = now
        return True


class AlertManager:
    """
    Менеджер системы алертов.
    
    Управляет правилами алертов и проверяет их для каждой записи.
    """
    
    def __init__(self):
        self.rules: List[AlertRule] = []
        self.alert_history: List[Dict] = []
    
    def add_rule(self, rule: AlertRule):
        """Добавляет правило алерта."""
        self.rules.append(rule)
    
    def check_entry(self, entry: LogEntry):
        """Проверяет запись против всех правил."""
        for rule in self.rules:
            if rule.check(entry):
                self.alert_history.append({
                    'timestamp': datetime.now(),
                    'rule': rule.name,
                    'entry': asdict(entry)
                })
    
    def get_alert_stats(self) -> Dict:
        """Возвращает статистику по алертам."""
        rule_counts = Counter(alert['rule'] for alert in self.alert_history)
        
        return {
            'total_alerts': len(self.alert_history),
            'by_rule': dict(rule_counts),
            'recent_alerts': self.alert_history[-10:]  # Последние 10
        }


# ============================================================================
# Продвинутые фильтры
# ============================================================================

class AdvancedLogFilter:
    """
    Расширенные возможности фильтрации логов.
    
    Поддерживает сложные условия, регулярные выражения и комбинации.
    """
    
    def __init__(self, logs: List[LogEntry]):
        self.logs = logs
    
    def by_time_range(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> 'AdvancedLogFilter':
        """
        Фильтрует по временному диапазону.
        
        Args:
            start_time: Начало диапазона (None = без ограничения)
            end_time: Конец диапазона (None = без ограничения)
        """
        filtered = []
        
        for log in self.logs:
            if start_time and log.timestamp < start_time:
                continue
            if end_time and log.timestamp > end_time:
                continue
            filtered.append(log)
        
        return AdvancedLogFilter(filtered)
    
    def by_path_regex(self, pattern: str) -> 'AdvancedLogFilter':
        """Фильтрует URL по регулярному выражению."""
        import re
        regex = re.compile(pattern)
        
        filtered = [log for log in self.logs if regex.search(log.path)]
        return AdvancedLogFilter(filtered)
    
    def by_custom_condition(
        self,
        condition: Callable[[LogEntry], bool]
    ) -> 'AdvancedLogFilter':
        """
        Фильтрует по произвольному условию.
        
        Example:
            >>> # Большие ответы от определенного IP
            >>> filter.by_custom_condition(
            ...     lambda log: log.ip == '127.0.0.1' and log.size > 10000
            ... )
        """
        filtered = [log for log in self.logs if condition(log)]
        return AdvancedLogFilter(filtered)
    
    def sample(self, n: int) -> 'AdvancedLogFilter':
        """Возвращает случайную выборку из n элементов."""
        import random
        
        if n >= len(self.logs):
            return self
        
        sampled = random.sample(self.logs, n)
        return AdvancedLogFilter(sampled)
    
    def get_logs(self) -> List[LogEntry]:
        """Возвращает отфильтрованные логи."""
        return self.logs
    
    def count(self) -> int:
        """Возвращает количество записей."""
        return len(self.logs)


# ============================================================================
# Агрегация по временным интервалам
# ============================================================================

class TimeSeriesAggregator:
    """
    Агрегирует логи по временным интервалам.
    
    Полезно для анализа трендов и построения графиков.
    """
    
    def __init__(self, logs: List[LogEntry]):
        self.logs = logs
    
    def aggregate_by_interval(
        self,
        interval: timedelta,
        metric: str = 'count'
    ) -> Dict[datetime, float]:
        """
        Агрегирует метрику по временным интервалам.
        
        Args:
            interval: Длина интервала (например, timedelta(minutes=5))
            metric: Метрика для агрегации ('count', 'size', 'error_rate')
        
        Returns:
            Словарь {timestamp: value} для каждого интервала
        
        Example:
            >>> # Количество запросов каждые 5 минут
            >>> agg = TimeSeriesAggregator(logs)
            >>> data = agg.aggregate_by_interval(timedelta(minutes=5), 'count')
        """
        if not self.logs:
            return {}
        
        # Находим временные границы
        min_time = min(log.timestamp for log in self.logs)
        max_time = max(log.timestamp for log in self.logs)
        
        # Создаем интервалы
        intervals = defaultdict(list)
        current = min_time
        
        while current <= max_time:
            intervals[current] = []
            current += interval
        
        # Распределяем логи по интервалам
        for log in self.logs:
            # Находим подходящий интервал
            interval_start = min_time
            while interval_start + interval <= log.timestamp:
                interval_start += interval
            
            intervals[interval_start].append(log)
        
        # Вычисляем метрику для каждого интервала
        result = {}
        
        for timestamp, logs_in_interval in intervals.items():
            if metric == 'count':
                result[timestamp] = len(logs_in_interval)
            elif metric == 'size':
                result[timestamp] = sum(log.size for log in logs_in_interval)
            elif metric == 'error_rate':
                if logs_in_interval:
                    errors = sum(1 for log in logs_in_interval if log.status >= 400)
                    result[timestamp] = (errors / len(logs_in_interval)) * 100
                else:
                    result[timestamp] = 0.0
        
        return result
    
    def get_hourly_stats(self) -> Dict[int, Dict[str, Any]]:
        """
        Получает статистику по часам (0-23).
        
        Returns:
            Словарь {hour: stats}
        """
        hourly_logs = defaultdict(list)
        
        for log in self.logs:
            hourly_logs[log.timestamp.hour].append(log)
        
        stats = {}
        for hour, logs in hourly_logs.items():
            analyzer = LogAnalyzer(logs)
            stats[hour] = {
                'count': len(logs),
                'total_bytes': analyzer.total_bytes(),
                'error_rate': analyzer.error_rate(),
                'top_urls': analyzer.top_urls(3)
            }
        
        return stats


# ============================================================================
# Экспорт данных
# ============================================================================

class DataExporter:
    """
    Экспортирует данные в различные форматы.
    
    Поддерживает JSON, CSV, и другие форматы.
    """
    
    @staticmethod
    def to_json(
        data: Any,
        filepath: str,
        indent: int = 2,
        ensure_ascii: bool = False
    ) -> None:
        """
        Экспортирует в JSON.
        
        Args:
            data: Данные для экспорта
            filepath: Путь к выходному файлу
            indent: Отступы для читаемости
            ensure_ascii: Экранировать не-ASCII символы
        """
        
        def default_serializer(obj):
            """Сериализация специальных типов."""
            if isinstance(obj, datetime):
                return obj.isoformat()
            elif isinstance(obj, LogEntry):
                return asdict(obj)
            elif isinstance(obj, Counter):
                return dict(obj)
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(
                data,
                f,
                indent=indent,
                ensure_ascii=ensure_ascii,
                default=default_serializer
            )
        
        print(f"✅ Данные экспортированы в {filepath}")
    
    @staticmethod
    def logs_to_csv(logs: List[LogEntry], filepath: str) -> None:
        """
        Экспортирует логи в CSV.
        
        Args:
            logs: Список логов
            filepath: Путь к выходному файлу
        """
        if not logs:
            print("⚠️  Нет данных для экспорта")
            return
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            # Получаем поля из первого лога
            fieldnames = logs[0].__dataclass_fields__.keys()
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for log in logs:
                row = asdict(log)
                # Форматируем datetime
                if isinstance(row['timestamp'], datetime):
                    row['timestamp'] = row['timestamp'].isoformat()
                writer.writerow(row)
        
        print(f"✅ {len(logs)} записей экспортировано в {filepath}")
    
    @staticmethod
    def stats_to_markdown(analyzer: LogAnalyzer, filepath: str) -> None:
        """
        Экспортирует статистику в Markdown.
        
        Args:
            analyzer: Анализатор с данными
            filepath: Путь к выходному файлу
        """
        summary = analyzer.summary()
        
        md_content = f"""# Отчет по анализу логов

Сгенерирован: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Общая информация

- **Всего запросов**: {summary['total_requests']:,}
- **Передано данных**: {summary['total_bytes']:,} байт
- **Средний размер ответа**: {summary['average_response_size']:.2f} байт
- **Процент ошибок**: {summary['error_rate']}
- **Процент успешных**: {summary['success_rate']}

## Статус коды

| Код | Количество |
|-----|------------|
"""
        
        for status, count in sorted(summary['status_codes'].items()):
            md_content += f"| {status} | {count:,} |\n"
        
        md_content += "\n## Топ-5 URL\n\n| URL | Запросов |\n|-----|----------|\n"
        
        for url, count in summary['top_urls']:
            md_content += f"| {url} | {count:,} |\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"✅ Отчет сохранен в {filepath}")


# ============================================================================
# Примеры использования
# ============================================================================

async def demo_async_processing():
    """Демонстрация асинхронной обработки нескольких файлов."""
    print("\n" + "=" * 60)
    print("АСИНХРОННАЯ ОБРАБОТКА НЕСКОЛЬКИХ ФАЙЛОВ")
    print("=" * 60)
    
    # Для демо создадим несколько копий sample_logs.txt
    import shutil
    
    files = []
    base_file = 'sample_logs.txt'
    
    if not Path(base_file).exists():
        print(f"⚠️  Файл {base_file} не найден")
        return
    
    # Создаем временные копии для демонстрации
    for i in range(3):
        temp_file = f'temp_log_{i}.txt'
        shutil.copy(base_file, temp_file)
        files.append(temp_file)
    
    try:
        # Обрабатываем файлы параллельно
        def progress(filename, count):
            print(f"  ✅ {filename}: {count} записей")
        
        results = await process_multiple_files(files, progress)
        
        print(f"\n📊 Обработано файлов: {len(results)}")
        
        total_logs = sum(len(logs) for logs in results.values())
        print(f"📊 Всего записей: {total_logs}")
    
    finally:
        # Удаляем временные файлы
        for f in files:
            Path(f).unlink(missing_ok=True)


def demo_alerts():
    """Демонстрация системы алертов."""
    print("\n" + "=" * 60)
    print("СИСТЕМА АЛЕРТОВ")
    print("=" * 60)
    
    # Создаем менеджер алертов
    alert_mgr = AlertManager()
    
    # Правило 1: Ошибки сервера (5xx)
    def server_error_action(entry: LogEntry):
        print(f"🚨 АЛЕРТ: Ошибка сервера! {entry.status} - {entry.path}")
    
    alert_mgr.add_rule(AlertRule(
        name="server_errors",
        condition=lambda e: e.status >= 500,
        action=server_error_action,
        cooldown=30.0
    ))
    
    # Правило 2: Большие ответы
    def large_response_action(entry: LogEntry):
        print(f"⚠️  АЛЕРТ: Большой ответ! {entry.size} байт для {entry.path}")
    
    alert_mgr.add_rule(AlertRule(
        name="large_responses",
        condition=lambda e: e.size > 10000,
        action=large_response_action,
        cooldown=60.0
    ))
    
    # Тестируем на sample_logs.txt
    if Path('sample_logs.txt').exists():
        parser = LogParser('sample_logs.txt')
        logs = parser.parse()
        
        print("\nПроверка записей...")
        for log in logs:
            alert_mgr.check_entry(log)
        
        # Статистика алертов
        stats = alert_mgr.get_alert_stats()
        print(f"\n📊 Статистика алертов:")
        print(f"  Всего сработало: {stats['total_alerts']}")
        print(f"  По правилам: {stats['by_rule']}")


def demo_advanced_filters():
    """Демонстрация продвинутых фильтров."""
    print("\n" + "=" * 60)
    print("ПРОДВИНУТЫЕ ФИЛЬТРЫ")
    print("=" * 60)
    
    if not Path('sample_logs.txt').exists():
        print("⚠️  Файл sample_logs.txt не найден")
        return
    
    parser = LogParser('sample_logs.txt')
    logs = parser.parse()
    
    # Сложная фильтрация
    print("\n1️⃣ Фильтр: GET запросы к /api/* с ошибками")
    filtered = (AdvancedLogFilter(logs)
                .by_path_regex(r'^/api/')
                .by_custom_condition(lambda e: e.method == 'GET')
                .by_custom_condition(lambda e: e.status >= 400))
    
    print(f"   Найдено: {filtered.count()} записей")
    for log in filtered.get_logs()[:5]:
        print(f"     {log.method} {log.path} - {log.status}")
    
    # Временная фильтрация
    if logs:
        print("\n2️⃣ Фильтр: Последний час активности")
        latest_time = max(log.timestamp for log in logs)
        hour_ago = latest_time - timedelta(hours=1)
        
        recent = AdvancedLogFilter(logs).by_time_range(start_time=hour_ago)
        print(f"   Найдено: {recent.count()} записей за последний час")


def demo_time_series():
    """Демонстрация агрегации по времени."""
    print("\n" + "=" * 60)
    print("АНАЛИЗ ВРЕМЕННЫХ РЯДОВ")
    print("=" * 60)
    
    if not Path('sample_logs.txt').exists():
        print("⚠️  Файл sample_logs.txt не найден")
        return
    
    parser = LogParser('sample_logs.txt')
    logs = parser.parse()
    
    aggregator = TimeSeriesAggregator(logs)
    
    # Почасовая статистика
    print("\n📈 Статистика по часам:")
    hourly = aggregator.get_hourly_stats()
    
    for hour in sorted(hourly.keys()):
        stats = hourly[hour]
        print(f"\n  {hour:02d}:00")
        print(f"    Запросов: {stats['count']}")
        print(f"    Данных: {stats['total_bytes']} байт")
        print(f"    Ошибок: {stats['error_rate']:.1f}%")


def demo_export():
    """Демонстрация экспорта данных."""
    print("\n" + "=" * 60)
    print("ЭКСПОРТ ДАННЫХ")
    print("=" * 60)
    
    if not Path('sample_logs.txt').exists():
        print("⚠️  Файл sample_logs.txt не найден")
        return
    
    parser = LogParser('sample_logs.txt')
    logs = parser.parse()
    analyzer = LogAnalyzer(logs)
    
    # Экспорт в JSON
    print("\n1️⃣ Экспорт статистики в JSON")
    DataExporter.to_json(
        analyzer.summary(),
        'stats_export.json'
    )
    
    # Экспорт логов в CSV
    print("\n2️⃣ Экспорт логов в CSV")
    DataExporter.logs_to_csv(logs[:10], 'logs_export.csv')
    
    # Экспорт отчета в Markdown
    print("\n3️⃣ Экспорт отчета в Markdown")
    DataExporter.stats_to_markdown(analyzer, 'report.md')


if __name__ == "__main__":
    print("=" * 60)
    print("ПРОДВИНУТЫЕ ВОЗМОЖНОСТИ АНАЛИЗА ЛОГОВ")
    print("=" * 60)
    
    # Синхронные демо
    demo_alerts()
    demo_advanced_filters()
    demo_time_series()
    demo_export()
    
    # Асинхронные демо
    print("\n" + "=" * 60)
    print("АСИНХРОННЫЕ ОПЕРАЦИИ")
    print("=" * 60)
    
    asyncio.run(demo_async_processing())
    
    print("\n" + "=" * 60)
    print("✅ Все демонстрации завершены!")
    print("=" * 60)
    
    print("\n💡 Для real-time мониторинга запустите:")
    print("   python log_monitor_demo.py")

