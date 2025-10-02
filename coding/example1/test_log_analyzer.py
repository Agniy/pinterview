"""
Unit тесты для системы анализа логов.

Запуск:
    python -m pytest test_log_analyzer.py -v
    
или без pytest:
    python test_log_analyzer.py
"""

import unittest
import tempfile
from datetime import datetime
from pathlib import Path

from log_analyzer import (
    LogEntry,
    LogParser,
    LogAnalyzer,
    LogFilter,
    format_bytes
)


class TestLogEntry(unittest.TestCase):
    """Тесты для модели LogEntry."""
    
    def test_valid_log_entry(self):
        """Тест создания валидной записи."""
        entry = LogEntry(
            ip="127.0.0.1",
            timestamp=datetime(2023, 10, 10, 13, 55, 36),
            method="GET",
            path="/api/users",
            status=200,
            size=1234
        )
        
        self.assertEqual(entry.ip, "127.0.0.1")
        self.assertEqual(entry.status, 200)
        self.assertEqual(entry.size, 1234)
    
    def test_invalid_status_code(self):
        """Тест валидации статус-кода."""
        with self.assertRaises(ValueError):
            LogEntry(
                ip="127.0.0.1",
                timestamp=datetime.now(),
                method="GET",
                path="/test",
                status=999,  # Невалидный статус
                size=100
            )
    
    def test_negative_size(self):
        """Тест валидации размера."""
        with self.assertRaises(ValueError):
            LogEntry(
                ip="127.0.0.1",
                timestamp=datetime.now(),
                method="GET",
                path="/test",
                status=200,
                size=-100  # Отрицательный размер
            )


class TestLogParser(unittest.TestCase):
    """Тесты для парсера логов."""
    
    def setUp(self):
        """Создаем временный файл для тестов."""
        self.temp_file = tempfile.NamedTemporaryFile(
            mode='w',
            delete=False,
            suffix='.log'
        )
        self.temp_file.close()
        self.parser = LogParser(self.temp_file.name)
    
    def tearDown(self):
        """Удаляем временный файл."""
        Path(self.temp_file.name).unlink(missing_ok=True)
    
    def test_parse_valid_line(self):
        """Тест парсинга валидной строки."""
        line = '127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /api/users HTTP/1.1" 200 1234'
        entry = self.parser.parse_line(line)
        
        self.assertIsNotNone(entry)
        self.assertEqual(entry.ip, "127.0.0.1")
        self.assertEqual(entry.method, "GET")
        self.assertEqual(entry.path, "/api/users")
        self.assertEqual(entry.status, 200)
        self.assertEqual(entry.size, 1234)
    
    def test_parse_invalid_line(self):
        """Тест парсинга невалидной строки."""
        line = "This is not a valid log line"
        entry = self.parser.parse_line(line)
        
        self.assertIsNone(entry)
    
    def test_parse_empty_line(self):
        """Тест парсинга пустой строки."""
        entry = self.parser.parse_line("")
        self.assertIsNone(entry)
    
    def test_parse_file(self):
        """Тест парсинга файла."""
        # Записываем тестовые данные
        with open(self.temp_file.name, 'w') as f:
            f.write('127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /api/users HTTP/1.1" 200 1234\n')
            f.write('192.168.1.1 - - [10/Oct/2023:13:55:37 +0000] "POST /api/login HTTP/1.1" 401 89\n')
            f.write('Invalid line\n')  # Эта строка должна быть пропущена
        
        logs = self.parser.parse()
        
        self.assertEqual(len(logs), 2)
        self.assertEqual(logs[0].ip, "127.0.0.1")
        self.assertEqual(logs[1].ip, "192.168.1.1")
    
    def test_nonexistent_file(self):
        """Тест обработки несуществующего файла."""
        with self.assertRaises(FileNotFoundError):
            LogParser("nonexistent_file.log")


class TestLogAnalyzer(unittest.TestCase):
    """Тесты для анализатора логов."""
    
    def setUp(self):
        """Создаем тестовые данные."""
        self.logs = [
            LogEntry("127.0.0.1", datetime.now(), "GET", "/api/users", 200, 1234),
            LogEntry("127.0.0.1", datetime.now(), "GET", "/api/users", 200, 5678),
            LogEntry("192.168.1.1", datetime.now(), "POST", "/api/login", 401, 89),
            LogEntry("10.0.0.1", datetime.now(), "GET", "/api/products", 404, 98),
            LogEntry("127.0.0.1", datetime.now(), "GET", "/api/products", 200, 3456),
        ]
        self.analyzer = LogAnalyzer(self.logs)
    
    def test_count_by_status(self):
        """Тест подсчета по статус-кодам."""
        counts = self.analyzer.count_by_status()
        
        self.assertEqual(counts[200], 3)
        self.assertEqual(counts[401], 1)
        self.assertEqual(counts[404], 1)
    
    def test_top_urls(self):
        """Тест топа URL."""
        top = self.analyzer.top_urls(2)
        
        self.assertEqual(len(top), 2)
        self.assertEqual(top[0][0], "/api/users")  # Самый частый
        self.assertEqual(top[0][1], 2)  # 2 раза
    
    def test_top_ips(self):
        """Тест топа IP адресов."""
        top = self.analyzer.top_ips(3)
        
        self.assertEqual(len(top), 3)
        self.assertEqual(top[0][0], "127.0.0.1")  # Самый частый
        self.assertEqual(top[0][1], 3)  # 3 запроса
    
    def test_total_bytes(self):
        """Тест подсчета общего размера."""
        total = self.analyzer.total_bytes()
        expected = 1234 + 5678 + 89 + 98 + 3456
        
        self.assertEqual(total, expected)
    
    def test_average_response_size(self):
        """Тест среднего размера ответа."""
        avg = self.analyzer.average_response_size()
        expected = (1234 + 5678 + 89 + 98 + 3456) / 5
        
        self.assertAlmostEqual(avg, expected, places=2)
    
    def test_error_rate(self):
        """Тест процента ошибок."""
        rate = self.analyzer.error_rate()
        # 2 ошибки из 5 запросов = 40%
        self.assertAlmostEqual(rate, 40.0, places=1)
    
    def test_success_rate(self):
        """Тест процента успешных запросов."""
        rate = self.analyzer.success_rate()
        # 3 успешных из 5 = 60%
        self.assertAlmostEqual(rate, 60.0, places=1)
    
    def test_requests_by_method(self):
        """Тест подсчета по HTTP методам."""
        methods = self.analyzer.requests_by_method()
        
        self.assertEqual(methods['GET'], 4)
        self.assertEqual(methods['POST'], 1)
    
    def test_empty_logs(self):
        """Тест с пустым списком логов."""
        empty_analyzer = LogAnalyzer([])
        
        self.assertEqual(empty_analyzer.total_bytes(), 0)
        self.assertEqual(empty_analyzer.average_response_size(), 0.0)
        self.assertEqual(empty_analyzer.error_rate(), 0.0)


class TestLogFilter(unittest.TestCase):
    """Тесты для фильтра логов."""
    
    def setUp(self):
        """Создаем тестовые данные."""
        self.logs = [
            LogEntry("127.0.0.1", datetime(2023, 10, 10, 13, 0), "GET", "/api/users", 200, 1234),
            LogEntry("192.168.1.1", datetime(2023, 10, 10, 14, 0), "POST", "/api/login", 401, 89),
            LogEntry("10.0.0.1", datetime(2023, 10, 10, 15, 0), "GET", "/api/products", 404, 98),
            LogEntry("127.0.0.1", datetime(2023, 10, 10, 16, 0), "GET", "/admin/users", 200, 3456),
        ]
    
    def test_filter_by_status(self):
        """Тест фильтрации по статусу."""
        filtered = LogFilter(self.logs).by_status(200).get_logs()
        
        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(log.status == 200 for log in filtered))
    
    def test_filter_by_status_range(self):
        """Тест фильтрации по диапазону статусов."""
        filtered = LogFilter(self.logs).by_status_range(400, 499).get_logs()
        
        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(400 <= log.status < 500 for log in filtered))
    
    def test_filter_by_method(self):
        """Тест фильтрации по HTTP методу."""
        filtered = LogFilter(self.logs).by_method("GET").get_logs()
        
        self.assertEqual(len(filtered), 3)
        self.assertTrue(all(log.method == "GET" for log in filtered))
    
    def test_filter_by_path_contains(self):
        """Тест фильтрации по подстроке в URL."""
        filtered = LogFilter(self.logs).by_path_contains("/api/").get_logs()
        
        self.assertEqual(len(filtered), 3)
        self.assertTrue(all("/api/" in log.path for log in filtered))
    
    def test_filter_chaining(self):
        """Тест цепочки фильтров."""
        filtered = (LogFilter(self.logs)
                   .by_method("GET")
                   .by_status(200)
                   .get_logs())
        
        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(
            log.method == "GET" and log.status == 200
            for log in filtered
        ))
    
    def test_filter_date_range(self):
        """Тест фильтрации по дате."""
        start = datetime(2023, 10, 10, 14, 0)
        end = datetime(2023, 10, 10, 15, 30)
        
        filtered = LogFilter(self.logs).by_date_range(start, end).get_logs()
        
        self.assertEqual(len(filtered), 2)


class TestUtilityFunctions(unittest.TestCase):
    """Тесты утилитных функций."""
    
    def test_format_bytes(self):
        """Тест форматирования байтов."""
        self.assertEqual(format_bytes(0), "0.00 B")
        self.assertEqual(format_bytes(1024), "1.00 KB")
        self.assertEqual(format_bytes(1048576), "1.00 MB")
        self.assertEqual(format_bytes(1073741824), "1.00 GB")
    
    def test_format_bytes_precision(self):
        """Тест точности форматирования."""
        result = format_bytes(1536)  # 1.5 KB
        self.assertIn("1.50", result)
        self.assertIn("KB", result)


# Запуск тестов
if __name__ == "__main__":
    unittest.main(verbosity=2)

