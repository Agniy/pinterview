"""
🟢 СТРОКИ (Strings) - Вопросы и задачи для собеседований

Основные темы:
- Методы строк
- Форматирование
- String slicing
- Регулярные выражения
- Кодировки
"""

import re
from collections import Counter


# ============================================================================
# ТЕОРЕТИЧЕСКИЕ ВОПРОСЫ
# ============================================================================

"""
Q1: Строки в Python изменяемы или неизменяемы?
A: Неизменяемы (immutable). Любая операция создает новую строку.

Q2: В чем разница между ' ', " " и ''' '''?
A:
- 'single' и "double" - эквивалентны
- '''triple''' или \"\"\"triple\"\"\" - многострочные строки, документация

Q3: Какие есть способы форматирования строк?
A:
- % форматирование: "Hello %s" % name
- str.format(): "Hello {}".format(name)
- f-strings (Python 3.6+): f"Hello {name}"

Q4: Что такое строковые методы split() и join()?
A:
- split() - разбивает строку на список
- join() - объединяет список в строку

Q5: В чем разница между find() и index()?
A:
- find() возвращает -1 если не найдено
- index() вызывает ValueError если не найдено

Q6: Что такое строковые срезы (slicing)?
A: s[start:end:step] - извлечение подстроки
"""


# ============================================================================
# ЗАДАЧА 1: Разворот строки
# ============================================================================

def reverse_string(s):
    """
    🟢 Junior level
    Развернуть строку
    
    >>> reverse_string("hello")
    'olleh'
    """
    return s[::-1]


def reverse_words(s):
    """
    Развернуть слова в строке
    
    >>> reverse_words("hello world python")
    'python world hello'
    """
    return ' '.join(s.split()[::-1])


def reverse_each_word(s):
    """
    Развернуть каждое слово
    
    >>> reverse_each_word("hello world")
    'olleh dlrow'
    """
    return ' '.join(word[::-1] for word in s.split())


# ============================================================================
# ЗАДАЧА 2: Проверка палиндрома
# ============================================================================

def is_palindrome(s):
    """
    🟢 Junior level
    Проверка, является ли строка палиндромом
    
    >>> is_palindrome("racecar")
    True
    >>> is_palindrome("hello")
    False
    """
    return s == s[::-1]


def is_palindrome_ignore_case(s):
    """
    Игнорируя регистр и пробелы
    
    >>> is_palindrome_ignore_case("A man a plan a canal Panama")
    True
    """
    # Удаляем все кроме букв и цифр, приводим к нижнему регистру
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]


# ============================================================================
# ЗАДАЧА 3: Подсчет символов
# ============================================================================

def count_characters(s):
    """
    🟢 Junior level
    Подсчитывает частоту каждого символа
    
    >>> count_characters("hello")
    {'h': 1, 'e': 1, 'l': 2, 'o': 1}
    """
    return dict(Counter(s))


def count_vowels_consonants(s):
    """
    Подсчитывает гласные и согласные
    
    >>> count_vowels_consonants("hello world")
    {'vowels': 3, 'consonants': 7}
    """
    vowels = "aeiouAEIOU"
    v_count = sum(1 for c in s if c in vowels)
    c_count = sum(1 for c in s if c.isalpha() and c not in vowels)
    
    return {'vowels': v_count, 'consonants': c_count}


# ============================================================================
# ЗАДАЧА 4: Удаление дубликатов символов
# ============================================================================

def remove_duplicates(s):
    """
    🟢 Junior level
    Удаляет дублирующиеся символы, сохраняя порядок
    
    >>> remove_duplicates("hello")
    'helo'
    """
    seen = set()
    result = []
    for char in s:
        if char not in seen:
            seen.add(char)
            result.append(char)
    return ''.join(result)


def remove_duplicate_words(s):
    """
    Удаляет дублирующиеся слова
    
    >>> remove_duplicate_words("hello world hello python world")
    'hello world python'
    """
    seen = set()
    result = []
    for word in s.split():
        if word not in seen:
            seen.add(word)
            result.append(word)
    return ' '.join(result)


# ============================================================================
# ЗАДАЧА 5: Сжатие строки
# ============================================================================

def compress_string(s):
    """
    🟡 Middle level
    Сжимает строку (run-length encoding)
    
    >>> compress_string("aabcccccaaa")
    'a2b1c5a3'
    >>> compress_string("abc")
    'abc'  # Не сжимаем если результат не короче
    """
    if not s:
        return s
    
    compressed = []
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == s[i-1]:
            count += 1
        else:
            compressed.append(s[i-1] + str(count))
            count = 1
    
    # Добавляем последний символ
    compressed.append(s[-1] + str(count))
    
    result = ''.join(compressed)
    return result if len(result) < len(s) else s


def decompress_string(s):
    """
    Распаковывает сжатую строку
    
    >>> decompress_string("a2b1c5")
    'aabccccc'
    """
    result = []
    i = 0
    
    while i < len(s):
        char = s[i]
        i += 1
        
        # Собираем число
        num_str = ''
        while i < len(s) and s[i].isdigit():
            num_str += s[i]
            i += 1
        
        count = int(num_str) if num_str else 1
        result.append(char * count)
    
    return ''.join(result)


# ============================================================================
# ЗАДАЧА 6: Первый неповторяющийся символ
# ============================================================================

def first_unique_char(s):
    """
    🟡 Middle level
    Находит первый неповторяющийся символ
    
    >>> first_unique_char("leetcode")
    'l'
    >>> first_unique_char("loveleetcode")
    'v'
    """
    counts = Counter(s)
    
    for char in s:
        if counts[char] == 1:
            return char
    
    return None


def first_unique_char_index(s):
    """
    Возвращает индекс первого уникального символа
    """
    counts = Counter(s)
    
    for i, char in enumerate(s):
        if counts[char] == 1:
            return i
    
    return -1


# ============================================================================
# ЗАДАЧА 7: Подстрока без повторяющихся символов
# ============================================================================

def longest_substring_without_repeating(s):
    """
    🔴 Senior level
    Находит длину самой длинной подстроки без повторяющихся символов
    
    >>> longest_substring_without_repeating("abcabcbb")
    3  # "abc"
    >>> longest_substring_without_repeating("bbbbb")
    1  # "b"
    """
    char_index = {}
    max_length = 0
    start = 0
    
    for end, char in enumerate(s):
        # Если символ уже встречался и в текущем окне
        if char in char_index and char_index[char] >= start:
            start = char_index[char] + 1
        
        char_index[char] = end
        max_length = max(max_length, end - start + 1)
    
    return max_length


# ============================================================================
# ЗАДАЧА 8: Проверка подстроки
# ============================================================================

def is_substring(s1, s2):
    """
    🟢 Junior level
    Проверяет, является ли s2 подстрокой s1
    
    >>> is_substring("hello world", "world")
    True
    """
    return s2 in s1


def is_rotation(s1, s2):
    """
    🟡 Middle level
    Проверяет, является ли s2 ротацией s1
    
    >>> is_rotation("waterbottle", "erbottlewat")
    True
    """
    if len(s1) != len(s2):
        return False
    
    # Хитрость: если s2 - ротация s1, то s2 будет подстрокой s1+s1
    return s2 in (s1 + s1)


# ============================================================================
# ЗАДАЧА 9: Форматирование строк
# ============================================================================

def string_formatting_examples():
    """
    🟢 Junior level
    Примеры различных способов форматирования
    """
    name = "Alice"
    age = 30
    pi = 3.14159
    
    # % форматирование (старый стиль)
    print("% formatting:")
    print("  Hello %s, you are %d years old" % (name, age))
    print("  Pi: %.2f" % pi)
    
    # str.format()
    print("\nstr.format():")
    print("  Hello {}, you are {} years old".format(name, age))
    print("  Hello {name}, you are {age} years old".format(name=name, age=age))
    print("  Pi: {:.2f}".format(pi))
    
    # f-strings (Python 3.6+)
    print("\nf-strings:")
    print(f"  Hello {name}, you are {age} years old")
    print(f"  Pi: {pi:.2f}")
    print(f"  Expression: {2 + 2 = }")  # Python 3.8+
    
    # Выравнивание и заполнение
    print("\nВыравнивание:")
    print(f"  Left:   '{name:<10}'")
    print(f"  Right:  '{name:>10}'")
    print(f"  Center: '{name:^10}'")
    print(f"  Fill:   '{name:*^10}'")


# ============================================================================
# ЗАДАЧА 10: Регулярные выражения
# ============================================================================

def regex_examples():
    """
    🟡 Middle level
    Примеры использования регулярных выражений
    """
    
    # Поиск email
    text = "Contact: john@example.com or jane@test.org"
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    print(f"Emails: {emails}")
    
    # Поиск телефонов
    text = "Call 123-456-7890 or (987) 654-3210"
    phones = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    print(f"Phones: {phones}")
    
    # Замена
    text = "Hello 123 World 456"
    no_digits = re.sub(r'\d+', 'NUM', text)
    print(f"Замена цифр: {no_digits}")
    
    # Разбиение
    text = "apple,banana;orange|grape"
    fruits = re.split(r'[,;|]', text)
    print(f"Fruits: {fruits}")
    
    # Группы
    pattern = r'(\w+)@(\w+)\.(\w+)'
    match = re.search(pattern, "user@example.com")
    if match:
        print(f"Username: {match.group(1)}")
        print(f"Domain: {match.group(2)}")
        print(f"TLD: {match.group(3)}")


def validate_email(email):
    """
    Валидация email
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def extract_urls(text):
    """
    Извлекает URL из текста
    """
    pattern = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
    return re.findall(pattern, text)


# ============================================================================
# ЗАДАЧА 11: Работа со строковыми методами
# ============================================================================

def string_methods_examples():
    """
    🟢 Junior level
    Демонстрация полезных строковых методов
    """
    s = "  Hello World  "
    
    print(f"Исходная: '{s}'")
    print(f"strip():  '{s.strip()}'")
    print(f"lstrip(): '{s.lstrip()}'")
    print(f"rstrip(): '{s.rstrip()}'")
    
    s = "hello world"
    print(f"\nИсходная: '{s}'")
    print(f"upper():      '{s.upper()}'")
    print(f"lower():      '{s.lower()}'")
    print(f"capitalize(): '{s.capitalize()}'")
    print(f"title():      '{s.title()}'")
    print(f"swapcase():   '{s.swapcase()}'")
    
    s = "apple,banana,orange"
    print(f"\nИсходная: '{s}'")
    print(f"split(','): {s.split(',')}")
    
    words = ['apple', 'banana', 'orange']
    print(f"Список: {words}")
    print(f"join('-'): '{'-'.join(words)}'")
    
    s = "hello"
    print(f"\nИсходная: '{s}'")
    print(f"startswith('he'): {s.startswith('he')}")
    print(f"endswith('lo'):   {s.endswith('lo')}")
    print(f"find('ll'):       {s.find('ll')}")
    print(f"replace('l', 'L'): '{s.replace('l', 'L')}'")


# ============================================================================
# ЗАДАЧА 12: Анаграммы
# ============================================================================

def are_anagrams(s1, s2):
    """
    🟢 Junior level
    Проверка, являются ли строки анаграммами
    
    >>> are_anagrams("listen", "silent")
    True
    """
    return sorted(s1.lower()) == sorted(s2.lower())


def group_anagrams(words):
    """
    🟡 Middle level
    Группирует слова-анаграммы
    
    >>> group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
    """
    from collections import defaultdict
    
    groups = defaultdict(list)
    for word in words:
        key = ''.join(sorted(word.lower()))
        groups[key].append(word)
    
    return list(groups.values())


# ============================================================================
# ЗАДАЧА 13: Кодировки
# ============================================================================

def encoding_examples():
    """
    🟡 Middle level
    Примеры работы с кодировками
    """
    
    # Unicode строка
    s = "Привет мир! 你好世界"
    print(f"Строка: {s}")
    print(f"Длина: {len(s)}")
    
    # Кодирование в bytes
    utf8_bytes = s.encode('utf-8')
    print(f"\nUTF-8 bytes: {utf8_bytes}")
    print(f"Размер: {len(utf8_bytes)} байт")
    
    # Декодирование обратно
    decoded = utf8_bytes.decode('utf-8')
    print(f"Декодировано: {decoded}")
    
    # Разные кодировки
    try:
        latin1 = s.encode('latin-1')
    except UnicodeEncodeError:
        print("\nНельзя закодировать в latin-1 (не поддерживает кириллицу/китайский)")
    
    # ASCII с обработкой ошибок
    ascii_ignore = s.encode('ascii', errors='ignore')
    ascii_replace = s.encode('ascii', errors='replace')
    print(f"\nASCII (ignore): {ascii_ignore}")
    print(f"ASCII (replace): {ascii_replace}")


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("СТРОКИ - Примеры и тесты")
    print("=" * 60)
    
    # Тест 1: Разворот
    print("\n1. Разворот строк:")
    print(f"   Строка: {reverse_string('hello world')}")
    print(f"   Слова: {reverse_words('hello world python')}")
    print(f"   Каждое слово: {reverse_each_word('hello world')}")
    
    # Тест 2: Палиндром
    print("\n2. Проверка палиндрома:")
    print(f"   'racecar': {is_palindrome('racecar')}")
    print(f"   'A man a plan a canal Panama': {is_palindrome_ignore_case('A man a plan a canal Panama')}")
    
    # Тест 3: Подсчет символов
    print("\n3. Подсчет символов:")
    print(f"   'hello': {count_characters('hello')}")
    print(f"   Гласные/согласные в 'hello world': {count_vowels_consonants('hello world')}")
    
    # Тест 4: Сжатие
    print("\n4. Сжатие строки:")
    test = "aabcccccaaa"
    compressed = compress_string(test)
    print(f"   '{test}' -> '{compressed}'")
    print(f"   Обратно: '{decompress_string(compressed)}'")
    
    # Тест 5: Первый уникальный символ
    print("\n5. Первый уникальный символ:")
    print(f"   'leetcode': {first_unique_char('leetcode')}")
    print(f"   'loveleetcode': {first_unique_char('loveleetcode')}")
    
    # Тест 6: Длинная подстрока без повторений
    print("\n6. Longest substring without repeating:")
    print(f"   'abcabcbb': {longest_substring_without_repeating('abcabcbb')}")
    print(f"   'pwwkew': {longest_substring_without_repeating('pwwkew')}")
    
    # Тест 7: Форматирование
    print("\n7. Форматирование строк:")
    string_formatting_examples()
    
    # Тест 8: Регулярные выражения
    print("\n8. Регулярные выражения:")
    regex_examples()
    
    # Тест 9: Строковые методы
    print("\n9. Строковые методы:")
    string_methods_examples()
    
    # Тест 10: Анаграммы
    print("\n10. Анаграммы:")
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    print(f"    Слова: {words}")
    print(f"    Группы: {group_anagrams(words)}")
    
    print("\n" + "=" * 60)

