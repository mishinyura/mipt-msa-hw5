import requests
from collections import Counter

def get_text(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return ""

def main():
    words_file = "words.txt"
    url = "https://eng.mipt.ru/why-mipt/"

    # Чтение и обработка слов с удалением дубликатов
    unique_words = set()
    with open(words_file, 'r') as file:
        for line in file:
            word = line.strip().lower()
            if word:
                unique_words.add(word)

    # Получение и обработка текста
    text = get_text(url)
    if not text:
        return

    # Подсчет частот для всех слов
    word_counts = Counter(text.lower().split())

    # Создание результата только для нужных слов
    frequencies = {word: word_counts.get(word, 0) for word in unique_words}

    print(frequencies)

if __name__ == "__main__":
    main()