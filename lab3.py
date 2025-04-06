import os
import csv
from datetime import datetime

# Функция подсчета количества файлов в заданной директории
def count_files_in_directory(directory='.'):
    files = [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
    return len(files)

# Чтение данных из CSV-файла и запись их в список словарей
def read_csv_to_dict(filename):
    data = []
    with open(filename, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Приведение данных к нужному типу
            row['post_id'] = int(row['post_id'])
            row['comment_id'] = int(row['comment_id'])
            row['date_time'] = datetime.strptime(row['date_time'], '%Y-%m-%d %H:%M')
            row['likes'] = int(row['likes'])
            data.append(row)
    return data

# Сортировка данных по строковому полю (по тексту комментария)
def sort_by_text(data):
    return sorted(data, key=lambda x: x['text'])

# Сортировка данных по числовому полю (по количеству лайков)
def sort_by_likes(data):
    return sorted(data, key=lambda x: x['likes'], reverse=True)

# Выбор комментариев по критерию (лайков больше заданного значения)
def filter_by_likes(data, min_likes):
    return [item for item in data if item['likes'] > min_likes]

# Сохранение данных обратно в CSV-файл
def save_dict_to_csv(filename, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['post_id', 'comment_id', 'date_time', 'text', 'likes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow({
                'post_id': item['post_id'],
                'comment_id': item['comment_id'],
                'date_time': item['date_time'].strftime('%Y-%m-%d %H:%M'),
                'text': item['text'],
                'likes': item['likes']
            })

# Основная функция программы
def main():
    # Подсчёт и вывод количества файлов в текущей директории
    file_count = count_files_in_directory()
    print(f"Количество файлов в текущей директории: {file_count}")

    # Чтение данных из CSV
    data = read_csv_to_dict('data.csv')
    print("\n📌 Исходные данные из CSV-файла:")
    for item in data:
        print(item)

    # Сортировка по тексту комментария (строковое поле)
    sorted_text = sort_by_text(data)
    print("\n🔤 Данные, отсортированные по тексту комментария:")
    for item in sorted_text:
        print(item)

    # Сортировка по лайкам (числовое поле)
    sorted_likes = sort_by_likes(data)
    print("\n🔢 Данные, отсортированные по количеству лайков (по убыванию):")
    for item in sorted_likes:
        print(item)

    # Фильтрация комментариев с лайками больше 5
    filtered_comments = filter_by_likes(data, min_likes=10)
    print("\n💬 Фильтр: только избранные комментарии")
    for item in filtered_comments:
        print(item)

    # Сохранение отсортированных данных обратно в файл
    save_dict_to_csv('updated_data.csv', sorted_likes)
    print("\n✅ Отсортированные по лайкам данные сохранены в файл 'updated_data.csv'.")

# Запуск программы
if __name__ == "__main__":
    main()
