import csv
from datetime import datetime


class BaseEntity:
    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.__dict__}>"


class Comment(BaseEntity):
    def __init__(self, post_id, comment_id, date_time, text, likes):
        self.post_id = post_id
        self.comment_id = comment_id
        self.date_time = date_time
        self.text = text
        self.likes = likes

    def __setattr__(self, name, value):
        # Разрешаем устанавливать только заранее известные поля
        if name in {'post_id', 'comment_id', 'date_time', 'text', 'likes'}:
            super().__setattr__(name, value)
        else:
            raise AttributeError(f"Нельзя установить новое свойство '{name}'")

    def __str__(self):
        return f"[{self.date_time}] Комментарий {self.comment_id} к посту {self.post_id}: {self.text} (Лайки: {self.likes})"

    @staticmethod
    def from_dict(data: dict):
        return Comment(
            int(data['post_id']),
            int(data['comment_id']),
            datetime.strptime(data['date_time'], '%Y-%m-%d %H:%M'),
            data['text'],
            int(data['likes'])
        )


class CommentCollection(BaseEntity):
    def __init__(self):
        self._comments = []

    def add(self, comment: Comment):
        self._comments.append(comment)

    def __iter__(self):
        return iter(self._comments)

    def __getitem__(self, index):
        return self._comments[index]

    def sort_by_text(self):
        return sorted(self._comments, key=lambda x: x.text)

    def sort_by_likes(self, reverse=True):
        return sorted(self._comments, key=lambda x: x.likes, reverse=reverse)

    def filter_by_likes(self, min_likes):
        return (c for c in self._comments if c.likes > min_likes)

    def __len__(self):
        return len(self._comments)

    def save_to_csv(self, filename):
        with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['post_id', 'comment_id', 'date_time', 'text', 'likes']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for c in self._comments:
                writer.writerow({
                    'post_id': c.post_id,
                    'comment_id': c.comment_id,
                    'date_time': c.date_time.strftime('%Y-%m-%d %H:%M'),
                    'text': c.text,
                    'likes': c.likes
                })

    @staticmethod
    def from_csv(filename):
        collection = CommentCollection()
        with open(filename, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                comment = Comment.from_dict(row)
                collection.add(comment)
        return collection


# 🔻 ВСТАВЬ ВОТ ЭТО В САМОМ НИЗУ ФАЙЛА:
if __name__ == "__main__":
    collection = CommentCollection.from_csv("data.csv")

    print(f"Всего комментариев: {len(collection)}\n")

    print("🔤 Сортировка по тексту:")
    for c in collection.sort_by_text():
        print(c)

    print("\n🔢 Сортировка по лайкам:")
    for c in collection.sort_by_likes():
        print(c)

    print("\n🚩 Комментарии с лайками > 5:")
    for c in collection.filter_by_likes(5):
        print(c)

    collection.save_to_csv("updated_data.csv")
