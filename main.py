import requests
from collections import Counter
import time
from functools import lru_cache

@lru_cache(maxsize=1)
def get_text(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Ошибка при получении текста: {e}")
        return ""

def count_word_frequencies(text, words_to_count):
    # Приводим текст к нижнему регистру для регистронезависимого поиска
    text = text.lower()
    words = text.split()
    word_counter = Counter(words)
    
    frequencies = {}
    for word in words_to_count:
        frequencies[word] = word_counter[word.lower()]
    
    return frequencies

def main():
    words_file = "words.txt"
    url = "https://eng.mipt.ru/why-mipt/"

    # Загружаем слова для подсчета
    words_to_count = []
    try:
        with open(words_file, 'r', encoding='utf-8') as file:
            words_to_count = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Файл {words_file} не найден")
        return
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    # Замеряем время выполнения
    start_time = time.time()
    
    # Получаем текст один раз
    text = get_text(url)
    if not text:
        return
    
    # Подсчитываем частоты для всех слов за один проход
    frequencies = count_word_frequencies(text, words_to_count)
    
    end_time = time.time()
    
    print("Результаты подсчета частот слов:")
    for word, count in frequencies.items():
        print(f"{word}: {count}")
    
    print(f"\nВремя выполнения: {end_time - start_time:.4f} секунд")

if __name__ == "__main__":
    main()