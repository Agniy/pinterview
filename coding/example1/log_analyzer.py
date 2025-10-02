"""
Система анализа логов веб-сервера

Этот модуль предоставляет инструменты для парсинга и анализа логов веб-серверов.
Поддерживает обработку больших файлов и вычисление различных метрик.
"""

import re
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Iterator, Dict, Counter as CounterType
from collections import Counter, defaultdict
from pathlib import Path


# ============================================================================
# Модель данных
# ============================================================================

@dataclass
class LogEntry:
    """
    Представляет одну запись из лог-файла.
    
    Использование dataclass дает нам:
    - Автоматический __init__, __repr__, __eq__
    - Читаемый код
    - Type hints для статического анализа
    """
    ip: str
    timestamp: datetime
    method: str
    path: str
    status: int
    size: int
    
    def __post_init__(self):
        """Валидация данных после инициализации"""
        if self.status < 100 or self.status >= 600:
            raise ValueError(f"Невалидный статус код: {self.status}")
        if self.size < 0:
            raise ValueError(f"Размер не может быть отрицательным: {self.size}")


# ============================================================================
# Парсер логов
# ============================================================================

class LogParser:
    """
    Парсер лог-файлов веб-сервера.
    
    Отвечает только за парсинг - следуем Single Responsibility Principle.
    Легко тестировать и расширять (например, для других форматов логов).
    """
    
    # Regex для парсинга строки лога
    # Использование raw string (r'...') для корректной обработки спецсимволов
    LOG_PATTERN = re.compile(
        r'(?P<ip>\S+) '                                    # IP адрес
        r'\S+ \S+ '                                        # - -
        r'\[(?P<timestamp>[^\]]+)\] '                      # [timestamp]
        r'"(?P<method>\S+) (?P<path>\S+) \S+" '           # "METHOD path HTTP/X.X"
        r'(?P<status>\d+) '                                # status code
        r'(?P<size>\d+)'                                   # response size
    )
    
    # Формат времени в логах
    TIMESTAMP_FORMAT = "%d/%b/%Y:%H:%M:%S %z"
    
    def __init__(self, filepath: str):
        """
        Args:
            filepath: Путь к лог-файлу
        
        Raises:
            FileNotFoundError: Если файл не существует
        """
        self.filepath = Path(filepath)
        
        if not self.filepath.exists():
            raise FileNotFoundError(f"Файл не найден: {filepath}")
    
    def parse_line(self, line: str) -> Optional[LogEntry]:
        """
        Парсит одну строку лога.
        
        Args:
            line: Строка из лог-файла
        
        Returns:
            LogEntry или None если строка невалидна
        
        Примечание:
            Возвращаем None вместо выбрасывания исключения,
            чтобы продолжить обработку остальных строк.
        """
        match = self.LOG_PATTERN.match(line.strip())
        
        if not match:
            # В продакшене здесь был бы логгер
            # print(f"Невалидная строка: {line[:50]}...")
            return None
        
        try:
            # Извлекаем данные из regex групп
            data = match.groupdict()
            
            # Парсим timestamp
            timestamp = datetime.strptime(
                data['timestamp'],
                self.TIMESTAMP_FORMAT
            )
            
            # Создаем LogEntry с валидацией в __post_init__
            return LogEntry(
                ip=data['ip'],
                timestamp=timestamp,
                method=data['method'],
                path=data['path'],
                status=int(data['status']),
                size=int(data['size'])
            )
        
        except (ValueError, KeyError) as e:
            # print(f"Ошибка парсинга: {e}")
            return None
    
    def parse(self) -> List[LogEntry]:
        """
        Парсит весь файл и возвращает список записей.
        
        Подходит для небольших файлов. Для больших используйте parse_stream().
        
        Returns:
            Список всех валидных записей из файла
        """
        entries = []
        
        with open(self.filepath, 'r', encoding='utf-8') as f:
            for line in f:
                entry = self.parse_line(line)
                if entry:
                    entries.append(entry)
        
        return entries
    
    def parse_stream(self) -> Iterator[LogEntry]:
        """
        Парсит файл построчно (streaming).
        
        Преимущества:
        - Не загружает весь файл в память
        - Подходит для очень больших файлов (GB+)
        - Ленивое вычисление (lazy evaluation)
        
        Yields:
            LogEntry для каждой валидной строки
        
        Example:
            >>> parser = LogParser('access.log')
            >>> for entry in parser.parse_stream():
            ...     if entry.status >= 500:
            ...         print(f"Server error: {entry}")
        """
        with open(self.filepath, 'r', encoding='utf-8') as f:
            for line in f:
                entry = self.parse_line(line)
                if entry:
                    yield entry


# ============================================================================
# Анализатор логов
# ============================================================================

class LogAnalyzer:
    """
    Анализирует логи и вычисляет различные метрики.
    
    Отделен от парсера - можем работать с уже распарсенными данными
    из разных источников (файл, база данных, сеть).
    """
    
    def __init__(self, logs: List[LogEntry]):
        """
        Args:
            logs: Список записей для анализа
        """
        self.logs = logs
    
    def count_by_status(self) -> CounterType[int]:
        """
        Подсчитывает количество запросов по статус-кодам.
        
        Returns:
            Counter с парами {status_code: count}
        
        Сложность: O(n) где n - количество логов
        
        Example:
            >>> analyzer.count_by_status()
            Counter({200: 1500, 404: 45, 500: 3})
        """
        # Generator expression для экономии памяти
        return Counter(log.status for log in self.logs)
    
    def top_urls(self, n: int = 10) -> List[tuple[str, int]]:
        """
        Находит топ-N самых посещаемых URL.
        
        Args:
            n: Количество URL в топе
        
        Returns:
            Список кортежей (url, count), отсортированный по убыванию count
        
        Сложность: O(n + k*log(k)) где k - уникальных URL
        
        Example:
            >>> analyzer.top_urls(3)
            [('/api/users', 500), ('/api/products', 300), ('/', 250)]
        """
        # Counter автоматически подсчитывает частоты
        url_counts = Counter(log.path for log in self.logs)
        
        # most_common(n) возвращает топ-N - эффективная реализация через heap
        return url_counts.most_common(n)
    
    def top_ips(self, n: int = 10) -> List[tuple[str, int]]:
        """
        Находит топ-N IP адресов с наибольшим количеством запросов.
        
        Args:
            n: Количество IP в топе
        
        Returns:
            Список кортежей (ip, count)
        """
        ip_counts = Counter(log.ip for log in self.logs)
        return ip_counts.most_common(n)
    
    def total_bytes(self) -> int:
        """
        Вычисляет общий объем переданных данных.
        
        Returns:
            Общий размер в байтах
        
        Сложность: O(n)
        """
        return sum(log.size for log in self.logs)
    
    def average_response_size(self) -> float:
        """
        Вычисляет средний размер ответа.
        
        Returns:
            Средний размер в байтах
        """
        if not self.logs:
            return 0.0
        
        return self.total_bytes() / len(self.logs)
    
    def requests_by_method(self) -> CounterType[str]:
        """
        Подсчитывает количество запросов по HTTP методам.
        
        Returns:
            Counter с парами {method: count}
        
        Example:
            >>> analyzer.requests_by_method()
            Counter({'GET': 5000, 'POST': 1200, 'PUT': 300})
        """
        return Counter(log.method for log in self.logs)
    
    def error_rate(self) -> float:
        """
        Вычисляет процент ошибочных запросов (4xx, 5xx).
        
        Returns:
            Процент ошибок (0.0 - 100.0)
        """
        if not self.logs:
            return 0.0
        
        error_count = sum(1 for log in self.logs if log.status >= 400)
        return (error_count / len(self.logs)) * 100
    
    def success_rate(self) -> float:
        """
        Вычисляет процент успешных запросов (2xx, 3xx).
        
        Returns:
            Процент успешных запросов (0.0 - 100.0)
        """
        return 100.0 - self.error_rate()
    
    def requests_by_hour(self) -> Dict[int, int]:
        """
        Группирует запросы по часам суток.
        
        Returns:
            Словарь {hour: count} где hour от 0 до 23
        
        Полезно для анализа нагрузки по времени суток.
        """
        # defaultdict автоматически создает значение 0 для новых ключей
        hourly_counts = defaultdict(int)
        
        for log in self.logs:
            hour = log.timestamp.hour
            hourly_counts[hour] += 1
        
        return dict(hourly_counts)
    
    def summary(self) -> Dict:
        """
        Возвращает сводную статистику.
        
        Returns:
            Словарь с различными метриками
        
        Удобно для быстрого обзора или экспорта в JSON.
        """
        return {
            'total_requests': len(self.logs),
            'total_bytes': self.total_bytes(),
            'average_response_size': self.average_response_size(),
            'error_rate': f"{self.error_rate():.2f}%",
            'success_rate': f"{self.success_rate():.2f}%",
            'status_codes': dict(self.count_by_status()),
            'http_methods': dict(self.requests_by_method()),
            'top_urls': self.top_urls(5),
            'top_ips': self.top_ips(5),
        }


# ============================================================================
# Фильтр логов
# ============================================================================

class LogFilter:
    """
    Фильтрует логи по различным критериям.
    
    Использует паттерн Builder для создания сложных фильтров.
    """
    
    def __init__(self, logs: List[LogEntry]):
        """
        Args:
            logs: Исходный список логов
        """
        self.logs = logs
    
    def by_status(self, status: int) -> 'LogFilter':
        """
        Фильтрует по статус-коду.
        
        Returns:
            Новый LogFilter с отфильтрованными логами
        
        Возвращаем self для цепочки вызовов (method chaining).
        """
        filtered = [log for log in self.logs if log.status == status]
        return LogFilter(filtered)
    
    def by_status_range(self, min_status: int, max_status: int) -> 'LogFilter':
        """
        Фильтрует по диапазону статус-кодов.
        
        Example:
            >>> # Только ошибки сервера
            >>> filter.by_status_range(500, 599)
        """
        filtered = [
            log for log in self.logs
            if min_status <= log.status <= max_status
        ]
        return LogFilter(filtered)
    
    def by_method(self, method: str) -> 'LogFilter':
        """Фильтрует по HTTP методу."""
        filtered = [log for log in self.logs if log.method == method]
        return LogFilter(filtered)
    
    def by_path_contains(self, substring: str) -> 'LogFilter':
        """Фильтрует URL содержащие подстроку."""
        filtered = [log for log in self.logs if substring in log.path]
        return LogFilter(filtered)
    
    def by_date_range(
        self,
        start: datetime,
        end: datetime
    ) -> 'LogFilter':
        """
        Фильтрует по диапазону дат.
        
        Args:
            start: Начальная дата (включительно)
            end: Конечная дата (включительно)
        """
        filtered = [
            log for log in self.logs
            if start <= log.timestamp <= end
        ]
        return LogFilter(filtered)
    
    def get_logs(self) -> List[LogEntry]:
        """Возвращает отфильтрованные логи."""
        return self.logs
    
    def analyze(self) -> LogAnalyzer:
        """
        Создает анализатор для отфильтрованных данных.
        
        Удобно для цепочки операций:
        >>> stats = (LogFilter(logs)
        ...          .by_status_range(500, 599)
        ...          .analyze()
        ...          .summary())
        """
        return LogAnalyzer(self.logs)


# ============================================================================
# Утилиты
# ============================================================================

def format_bytes(bytes_count: int) -> str:
    """
    Форматирует размер в человекочитаемый формат.
    
    Args:
        bytes_count: Размер в байтах
    
    Returns:
        Строка с форматированным размером
    
    Example:
        >>> format_bytes(1024)
        '1.00 KB'
        >>> format_bytes(1048576)
        '1.00 MB'
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.2f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.2f} PB"


def print_summary(analyzer: LogAnalyzer) -> None:
    """
    Красиво выводит сводную статистику.
    
    Args:
        analyzer: Анализатор с данными
    """
    summary = analyzer.summary()
    
    print("=" * 60)
    print("СВОДНАЯ СТАТИСТИКА ЛОГОВ")
    print("=" * 60)
    
    print(f"\n📊 Общая информация:")
    print(f"  Всего запросов: {summary['total_requests']:,}")
    print(f"  Передано данных: {format_bytes(summary['total_bytes'])}")
    print(f"  Средний размер ответа: {format_bytes(int(summary['average_response_size']))}")
    
    print(f"\n✅ Успешность:")
    print(f"  Успешных запросов: {summary['success_rate']}")
    print(f"  Ошибочных запросов: {summary['error_rate']}")
    
    print(f"\n📈 Топ-5 URL:")
    for url, count in summary['top_urls']:
        print(f"  {count:6,} - {url}")
    
    print(f"\n🌐 Топ-5 IP адресов:")
    for ip, count in summary['top_ips']:
        print(f"  {count:6,} - {ip}")
    
    print(f"\n🔧 HTTP методы:")
    for method, count in sorted(
        summary['http_methods'].items(),
        key=lambda x: x[1],
        reverse=True
    ):
        print(f"  {method:6s}: {count:,}")
    
    print(f"\n📋 Статус коды:")
    for status, count in sorted(summary['status_codes'].items()):
        status_name = get_status_name(status)
        print(f"  {status} ({status_name:20s}): {count:,}")
    
    print("=" * 60)


def get_status_name(status: int) -> str:
    """
    Возвращает описание статус-кода.
    
    Args:
        status: HTTP статус код
    
    Returns:
        Описание статус-кода
    """
    status_names = {
        200: 'OK',
        201: 'Created',
        204: 'No Content',
        301: 'Moved Permanently',
        302: 'Found',
        304: 'Not Modified',
        400: 'Bad Request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        500: 'Internal Server Error',
        502: 'Bad Gateway',
        503: 'Service Unavailable',
    }
    return status_names.get(status, 'Unknown')


# ============================================================================
# Пример использования
# ============================================================================

if __name__ == "__main__":
    # Демонстрация базового использования
    
    print("Пример использования системы анализа логов\n")
    
    # Пример данных для демонстрации
    sample_data = """127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /api/users HTTP/1.1" 200 1234
192.168.1.1 - - [10/Oct/2023:13:55:37 +0000] "POST /api/login HTTP/1.1" 401 89
10.0.0.1 - - [10/Oct/2023:13:55:38 +0000] "GET /api/products HTTP/1.1" 200 5678
127.0.0.1 - - [10/Oct/2023:13:55:39 +0000] "GET /api/users/123 HTTP/1.1" 200 543
192.168.1.1 - - [10/Oct/2023:13:55:40 +0000] "POST /api/login HTTP/1.1" 200 234
10.0.0.1 - - [10/Oct/2023:13:55:41 +0000] "GET /api/products/456 HTTP/1.1" 404 98
127.0.0.1 - - [10/Oct/2023:13:55:42 +0000] "DELETE /api/users/123 HTTP/1.1" 204 0
192.168.1.1 - - [10/Oct/2023:13:55:43 +0000] "GET /api/stats HTTP/1.1" 500 234"""
    
    # Создаем временный файл для демонстрации
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
        f.write(sample_data)
        temp_file = f.name
    
    try:
        # Парсинг
        print("1️⃣ Парсинг логов...")
        parser = LogParser(temp_file)
        logs = parser.parse()
        print(f"   Загружено {len(logs)} записей\n")
        
        # Анализ
        print("2️⃣ Анализ данных...")
        analyzer = LogAnalyzer(logs)
        
        print(f"   Статус коды: {dict(analyzer.count_by_status())}")
        print(f"   Топ URL: {analyzer.top_urls(3)}")
        print(f"   Топ IP: {analyzer.top_ips(2)}")
        print(f"   Всего байт: {analyzer.total_bytes()}\n")
        
        # Фильтрация
        print("3️⃣ Фильтрация (только ошибки)...")
        errors = LogFilter(logs).by_status_range(400, 599).get_logs()
        print(f"   Найдено ошибок: {len(errors)}")
        for log in errors:
            print(f"     {log.status} - {log.path}\n")
        
        # Сводка
        print("4️⃣ Сводная статистика:")
        print_summary(analyzer)
    
    finally:
        # Удаляем временный файл
        import os
        os.unlink(temp_file)

