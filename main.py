#!/usr/bin/env python3
"""
Главный файл для запуска примеров из коллекции вопросов для собеседований по Python
"""

import sys


def show_menu():
    """Показывает главное меню"""
    print("=" * 60)
    print("Python Interview Questions & Tasks")
    print("Коллекция вопросов и задач для собеседований")
    print("=" * 60)
    print("\nВыберите модуль:")
    print("\n📊 СТРУКТУРЫ ДАННЫХ:")
    print("  1. Списки (Lists)")
    print("  2. Словари (Dictionaries)")
    print("  3. Множества (Sets)")
    print("  4. Кортежи (Tuples)")
    
    print("\n📝 СТРОКИ:")
    print("  5. Строки и операции со строками")
    
    print("\n🔧 ФУНКЦИИ:")
    print("  6. Декораторы (Decorators)")
    print("  7. Замыкания (Closures)")
    print("  8. Генераторы (Generators)")
    
    print("\n🏗️  ООП:")
    print("  9. Классы и наследование")
    print("  10. Магические методы (Magic Methods)")
    
    print("\n🧮 АЛГОРИТМЫ:")
    print("  11. Алгоритмы сортировки")
    print("  12. Алгоритмы поиска")
    print("  13. Рекурсия")
    
    print("\n🚀 ПРОДВИНУТЫЕ ТЕМЫ:")
    print("  14. Итераторы")
    print("  15. Контекстные менеджеры")
    print("  16. Метаклассы")
    
    print("\n  0. Выход")
    print("=" * 60)


def run_module(choice):
    """Запускает выбранный модуль"""
    
    modules = {
        '1': ('data_structures.lists', 'Списки'),
        '2': ('data_structures.dicts', 'Словари'),
        '3': ('data_structures.sets', 'Множества'),
        '4': ('data_structures.tuples', 'Кортежи'),
        '5': ('strings.string_operations', 'Строки'),
        '6': ('functions.decorators', 'Декораторы'),
        '7': ('functions.closures', 'Замыкания'),
        '8': ('functions.generators', 'Генераторы'),
        '9': ('oop.classes', 'Классы и наследование'),
        '10': ('oop.magic_methods', 'Магические методы'),
        '11': ('algorithms.sorting', 'Сортировка'),
        '12': ('algorithms.searching', 'Поиск'),
        '13': ('algorithms.recursion', 'Рекурсия'),
        '14': ('advanced.iterators', 'Итераторы'),
        '15': ('advanced.context_managers', 'Контекстные менеджеры'),
        '16': ('advanced.metaclasses', 'Метаклассы'),
    }
    
    if choice == '0':
        print("\nДо свидания!")
        return False
    
    if choice not in modules:
        print("\n❌ Неверный выбор. Попробуйте еще раз.")
        return True
    
    module_name, display_name = modules[choice]
    
    print(f"\n{'=' * 60}")
    print(f"Запуск модуля: {display_name}")
    print(f"{'=' * 60}\n")
    
    try:
        # Импортируем и запускаем модуль
        module = __import__(module_name, fromlist=[''])
        
        # Запускаем главный блок модуля
        if hasattr(module, '__file__'):
            exec(open(module.__file__).read(), {'__name__': '__main__'})
        
    except Exception as e:
        print(f"\n❌ Ошибка при запуске модуля: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n{'=' * 60}")
    input("\nНажмите Enter для продолжения...")
    
    return True


def run_all():
    """Запускает все модули по очереди"""
    print("\n🚀 Запуск всех модулей...\n")
    
    for i in range(1, 17):
        run_module(str(i))
    
    print("\n✅ Все модули выполнены!")


def main():
    """Главная функция"""
    
    # Проверяем аргументы командной строки
    if len(sys.argv) > 1:
        if sys.argv[1] == '--all':
            run_all()
            return
        elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print("Использование:")
            print("  python main.py          # Интерактивное меню")
            print("  python main.py --all    # Запустить все модули")
            print("  python main.py <номер>  # Запустить конкретный модуль")
            print("\nПримеры:")
            print("  python main.py 1        # Запустить модуль 'Списки'")
            print("  python main.py 6        # Запустить модуль 'Декораторы'")
            return
        else:
            # Запуск конкретного модуля
            run_module(sys.argv[1])
            return
    
    # Интерактивный режим
    while True:
        show_menu()
        
        try:
            choice = input("\nВаш выбор: ").strip()
            
            if not run_module(choice):
                break
        
        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем.")
            break
        except EOFError:
            print("\n\nДо свидания!")
            break


if __name__ == "__main__":
    main()

