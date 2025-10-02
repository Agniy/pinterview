#!/usr/bin/env python3
"""
Визуализация и генерация отчетов по логам

Этот модуль предоставляет инструменты для создания:
- ASCII графиков в терминале
- HTML отчетов с интерактивными графиками
- Временных графиков и трендов

Зависимости (опционально):
    - matplotlib (для PNG графиков)
    - plotly (для интерактивных HTML графиков)
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from collections import Counter
from pathlib import Path

from log_analyzer import LogEntry, LogAnalyzer
from log_analyzer_advanced import TimeSeriesAggregator


# ============================================================================
# ASCII визуализация (без зависимостей)
# ============================================================================

class ASCIIChart:
    """
    Создает ASCII графики для вывода в терминале.
    
    Не требует внешних библиотек, работает везде.
    """
    
    @staticmethod
    def bar_chart(
        data: Dict[str, int],
        title: str = "",
        width: int = 50,
        show_values: bool = True
    ) -> str:
        """
        Создает горизонтальную столбчатую диаграмму.
        
        Args:
            data: Словарь {label: value}
            title: Заголовок графика
            width: Максимальная ширина столбцов
            show_values: Показывать числовые значения
        
        Returns:
            ASCII представление графика
        """
        if not data:
            return "Нет данных для отображения"
        
        # Находим максимальное значение для масштабирования
        max_value = max(data.values())
        max_label_len = max(len(str(k)) for k in data.keys())
        
        # Строим график
        chart = []
        
        if title:
            chart.append(f"\n{title}")
            chart.append("=" * (width + max_label_len + 15))
        
        for label, value in sorted(data.items(), key=lambda x: x[1], reverse=True):
            # Вычисляем длину столбца
            bar_length = int((value / max_value) * width) if max_value > 0 else 0
            bar = "█" * bar_length
            
            # Форматируем строку
            if show_values:
                line = f"{str(label):<{max_label_len}} │ {bar} {value:,}"
            else:
                line = f"{str(label):<{max_label_len}} │ {bar}"
            
            chart.append(line)
        
        return "\n".join(chart)
    
    @staticmethod
    def line_chart(
        data: Dict[Any, float],
        title: str = "",
        height: int = 15,
        width: int = 60
    ) -> str:
        """
        Создает линейный график.
        
        Args:
            data: Словарь {x: y}
            title: Заголовок
            height: Высота графика
            width: Ширина графика
        
        Returns:
            ASCII линейный график
        """
        if not data:
            return "Нет данных для отображения"
        
        # Сортируем данные по X
        sorted_data = sorted(data.items())
        values = [v for _, v in sorted_data]
        labels = [k for k, _ in sorted_data]
        
        # Масштабируем значения
        min_val = min(values)
        max_val = max(values)
        val_range = max_val - min_val if max_val != min_val else 1
        
        # Создаем сетку
        grid = [[' ' for _ in range(width)] for _ in range(height)]
        
        # Рисуем линию
        step = (width - 1) / (len(values) - 1) if len(values) > 1 else 0
        
        for i, value in enumerate(values):
            x = int(i * step)
            y = height - 1 - int(((value - min_val) / val_range) * (height - 1))
            
            # Ставим точку
            grid[y][x] = '●'
            
            # Соединяем с предыдущей точкой
            if i > 0:
                prev_value = values[i - 1]
                prev_x = int((i - 1) * step)
                prev_y = height - 1 - int(((prev_value - min_val) / val_range) * (height - 1))
                
                # Рисуем линию между точками
                for dx in range(prev_x + 1, x):
                    dy = prev_y + int((y - prev_y) * (dx - prev_x) / (x - prev_x))
                    if 0 <= dy < height:
                        grid[dy][dx] = '·'
        
        # Форматируем вывод
        chart = []
        
        if title:
            chart.append(f"\n{title}")
            chart.append("=" * width)
        
        # Добавляем оси Y
        for i, row in enumerate(grid):
            val = max_val - (i / (height - 1)) * val_range
            chart.append(f"{val:>8.1f} │ {''.join(row)}")
        
        # Ось X
        chart.append(" " * 9 + "└" + "─" * width)
        
        # Метки X (упрощенно)
        if len(labels) <= 5:
            x_labels = " " * 11
            for i, label in enumerate(labels):
                pos = int(i * step)
                x_labels += f"{str(label):<{width // len(labels)}}"
            chart.append(x_labels[:width + 11])
        
        return "\n".join(chart)
    
    @staticmethod
    def histogram(
        values: List[float],
        bins: int = 10,
        title: str = ""
    ) -> str:
        """
        Создает гистограмму распределения.
        
        Args:
            values: Список значений
            bins: Количество интервалов
            title: Заголовок
        
        Returns:
            ASCII гистограмма
        """
        if not values:
            return "Нет данных"
        
        # Вычисляем интервалы
        min_val = min(values)
        max_val = max(values)
        bin_size = (max_val - min_val) / bins
        
        # Распределяем значения по интервалам
        histogram_data = [0] * bins
        
        for value in values:
            bin_idx = int((value - min_val) / bin_size) if bin_size > 0 else 0
            if bin_idx >= bins:
                bin_idx = bins - 1
            histogram_data[bin_idx] += 1
        
        # Создаем labels для интервалов
        bin_labels = {}
        for i in range(bins):
            start = min_val + i * bin_size
            end = start + bin_size
            bin_labels[f"{start:.1f}-{end:.1f}"] = histogram_data[i]
        
        return ASCIIChart.bar_chart(bin_labels, title)


# ============================================================================
# HTML отчеты
# ============================================================================

class HTMLReportGenerator:
    """
    Генерирует HTML отчеты с встроенной визуализацией.
    
    Использует Chart.js для интерактивных графиков (CDN, без установки).
    """
    
    @staticmethod
    def generate_report(
        analyzer: LogAnalyzer,
        filepath: str = "report.html"
    ) -> None:
        """
        Генерирует полный HTML отчет.
        
        Args:
            analyzer: Анализатор с данными
            filepath: Путь к выходному файлу
        """
        summary = analyzer.summary()
        
        # HTML шаблон с Chart.js
        html_template = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Отчет по анализу логов</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        .table {{
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}
        th {{
            background: #667eea;
            color: white;
        }}
        .success {{ color: #10b981; }}
        .error {{ color: #ef4444; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Отчет по анализу логов веб-сервера</h1>
        <p>Сгенерирован: {generated_time}</p>
    </div>
    
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-value">{total_requests:,}</div>
            <div class="stat-label">Всего запросов</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{total_mb} MB</div>
            <div class="stat-label">Передано данных</div>
        </div>
        <div class="stat-card">
            <div class="stat-value success">{success_rate}</div>
            <div class="stat-label">Успешных запросов</div>
        </div>
        <div class="stat-card">
            <div class="stat-value error">{error_rate}</div>
            <div class="stat-label">Ошибочных запросов</div>
        </div>
    </div>
    
    <div class="chart-container">
        <h2>Распределение статус-кодов</h2>
        <canvas id="statusChart"></canvas>
    </div>
    
    <div class="chart-container">
        <h2>HTTP методы</h2>
        <canvas id="methodsChart"></canvas>
    </div>
    
    <div class="table">
        <h2 style="padding: 20px; margin: 0;">Топ-10 URL</h2>
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>URL</th>
                    <th>Запросов</th>
                </tr>
            </thead>
            <tbody>
                {top_urls_rows}
            </tbody>
        </table>
    </div>
    
    <script>
        // График статус-кодов
        new Chart(document.getElementById('statusChart'), {{
            type: 'bar',
            data: {{
                labels: {status_labels},
                datasets: [{{
                    label: 'Количество запросов',
                    data: {status_data},
                    backgroundColor: 'rgba(102, 126, 234, 0.5)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ display: false }}
                }}
            }}
        }});
        
        // График HTTP методов
        new Chart(document.getElementById('methodsChart'), {{
            type: 'pie',
            data: {{
                labels: {methods_labels},
                datasets: [{{
                    data: {methods_data},
                    backgroundColor: [
                        'rgba(102, 126, 234, 0.8)',
                        'rgba(118, 75, 162, 0.8)',
                        'rgba(237, 100, 166, 0.8)',
                        'rgba(255, 154, 158, 0.8)'
                    ]
                }}]
            }},
            options: {{
                responsive: true
            }}
        }});
    </script>
</body>
</html>"""
        
        # Подготавливаем данные
        status_labels = list(summary['status_codes'].keys())
        status_data = list(summary['status_codes'].values())
        
        methods_labels = list(summary['http_methods'].keys())
        methods_data = list(summary['http_methods'].values())
        
        # Таблица топ URL
        top_urls_rows = ""
        for i, (url, count) in enumerate(summary['top_urls'], 1):
            top_urls_rows += f"<tr><td>{i}</td><td>{url}</td><td>{count:,}</td></tr>"
        
        # Заполняем шаблон
        html = html_template.format(
            generated_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            total_requests=summary['total_requests'],
            total_mb=f"{summary['total_bytes'] / 1024 / 1024:.2f}",
            success_rate=summary['success_rate'],
            error_rate=summary['error_rate'],
            status_labels=status_labels,
            status_data=status_data,
            methods_labels=methods_labels,
            methods_data=methods_data,
            top_urls_rows=top_urls_rows
        )
        
        # Сохраняем
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ HTML отчет сохранен: {filepath}")
        print(f"   Откройте в браузере: file://{Path(filepath).absolute()}")


# ============================================================================
# Консольные отчеты с визуализацией
# ============================================================================

class ConsoleVisualizer:
    """
    Красивые консольные отчеты с ASCII графиками.
    """
    
    @staticmethod
    def print_dashboard(analyzer: LogAnalyzer) -> None:
        """
        Выводит полный dashboard в консоль.
        
        Args:
            analyzer: Анализатор с данными
        """
        summary = analyzer.summary()
        
        print("\n" + "=" * 70)
        print("📊 DASHBOARD АНАЛИЗА ЛОГОВ")
        print("=" * 70)
        
        # Основные метрики
        print(f"\n{'ОСНОВНЫЕ МЕТРИКИ':^70}")
        print("-" * 70)
        print(f"  Всего запросов:      {summary['total_requests']:>10,}")
        print(f"  Передано данных:     {summary['total_bytes']:>10,} байт")
        print(f"  Средний размер:      {summary['average_response_size']:>10,.0f} байт")
        print(f"  Успешных запросов:   {summary['success_rate']:>10}")
        print(f"  Ошибочных запросов:  {summary['error_rate']:>10}")
        
        # График статус-кодов
        print(ASCIIChart.bar_chart(
            summary['status_codes'],
            "\n📋 РАСПРЕДЕЛЕНИЕ СТАТУС-КОДОВ",
            width=40
        ))
        
        # График HTTP методов
        print(ASCIIChart.bar_chart(
            summary['http_methods'],
            "\n🔧 HTTP МЕТОДЫ",
            width=40
        ))
        
        # Топ URL
        print(f"\n{'📈 ТОП-10 URL':^70}")
        print("-" * 70)
        top_urls_dict = {url: count for url, count in summary['top_urls']}
        print(ASCIIChart.bar_chart(top_urls_dict, width=40))
        
        print("\n" + "=" * 70)
    
    @staticmethod
    def print_time_series(
        logs: List[LogEntry],
        interval: timedelta = timedelta(hours=1)
    ) -> None:
        """
        Выводит временной график активности.
        
        Args:
            logs: Список логов
            interval: Интервал агрегации
        """
        aggregator = TimeSeriesAggregator(logs)
        
        # Получаем данные по интервалам
        data = aggregator.aggregate_by_interval(interval, 'count')
        
        # Форматируем для графика
        formatted_data = {
            ts.strftime('%H:%M'): count
            for ts, count in data.items()
        }
        
        print(ASCIIChart.line_chart(
            formatted_data,
            "⏰ АКТИВНОСТЬ ПО ВРЕМЕНИ",
            height=12,
            width=60
        ))
    
    @staticmethod
    def print_response_size_distribution(logs: List[LogEntry]) -> None:
        """
        Выводит распределение размеров ответов.
        
        Args:
            logs: Список логов
        """
        sizes = [log.size for log in logs]
        
        print(ASCIIChart.histogram(
            sizes,
            bins=15,
            title="\n📦 РАСПРЕДЕЛЕНИЕ РАЗМЕРОВ ОТВЕТОВ"
        ))


# ============================================================================
# Примеры использования
# ============================================================================

def demo_visualization():
    """Демонстрация всех возможностей визуализации."""
    from log_analyzer import LogParser
    
    if not Path('sample_logs.txt').exists():
        print("⚠️  Файл sample_logs.txt не найден")
        return
    
    # Загружаем данные
    parser = LogParser('sample_logs.txt')
    logs = parser.parse()
    analyzer = LogAnalyzer(logs)
    
    # Консольный dashboard
    print("\n" + "=" * 70)
    print("1️⃣ КОНСОЛЬНАЯ ВИЗУАЛИЗАЦИЯ")
    print("=" * 70)
    
    ConsoleVisualizer.print_dashboard(analyzer)
    
    # Временной график
    if logs:
        ConsoleVisualizer.print_time_series(logs, timedelta(hours=1))
    
    # Распределение размеров
    if logs:
        ConsoleVisualizer.print_response_size_distribution(logs)
    
    # HTML отчет
    print("\n" + "=" * 70)
    print("2️⃣ HTML ОТЧЕТ")
    print("=" * 70)
    
    HTMLReportGenerator.generate_report(analyzer, 'visual_report.html')
    
    print("\n✅ Визуализация завершена!")


if __name__ == "__main__":
    demo_visualization()


