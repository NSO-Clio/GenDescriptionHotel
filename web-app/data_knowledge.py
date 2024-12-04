import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List


class DataKnowLedge:
    def __init__(self, chunks: List[str] = ['']) -> None:
        """
        Инициализация класса DataKnowLedge.

        Параметры:
        - chunks: Список текстовых описаний.
        """
        # Инициализация SentenceTransformer
        try:
            self.model = SentenceTransformer('BAAI/bge-m3', device="cuda")
        except:
            self.model = SentenceTransformer('BAAI/bge-m3', device="cpu")

        # Создание эмбеддингов
        self.chunks = chunks
        self.embeddings = self.model.encode(chunks)

        # Инициализация FAISS индекса
        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(self.embeddings)

    def get_similar_chunks(self, query: str, k: int = 2) -> List[str]:
        """
        Поиск k похожих описаний для заданного текста.

        Параметры:
        - query: Текстовый запрос.
        - k: Количество похожих результатов.

        Возвращает:
        - Список k похожих описаний.
        """

        if len(self.chunks) == 0 or self.index.ntotal == 0:
            return 'Пока нет'  # Если база пуста, возвращаем 'Пока нет'

        query_embedding = self.model.encode([query])
        _, idx = self.index.search(query_embedding, k)
        return [self.chunks[i] for i in idx.flatten()]

    def add_chunks(self, new_chunks: List[str]) -> None:
        """
        Добавление новых описаний в базу.

        Параметры:
        - new_chunks: Список новых текстовых описаний.
        """
        # Вычисление эмбеддингов для новых описаний
        new_embeddings = self.model.encode(new_chunks)

        # Добавление новых эмбеддингов в индекс
        self.index.add(new_embeddings)

        # Обновление списка описаний и эмбеддингов
        self.chunks.extend(new_chunks)
        self.embeddings = np.vstack((self.embeddings, new_embeddings))


# # Исходные описания
# descriptions = [
#     "Описание 1: Основы проектирования систем.",
#     "Описание 2: Методы анализа данных.",
#     "Описание 3: Введение в машинное обучение.",
# ]

# # Создание объекта DataKnowLedge
# knowledge = DataKnowLedge(descriptions)

# # Добавление новых описаний
# new_descriptions = [
#     "Описание 4: Программирование на Python.",
#     "Описание 5: Работа с большими данными."
# ]
# knowledge.add_chunks(new_descriptions)

# # Проверка: Поиск похожих описаний
# query_text = "Как анализировать данные?"
# similar_descriptions = knowledge.get_similar_chunks(query_text, k=3)

# # Вывод
# print("Похожие описания:")
# for desc in similar_descriptions:
#     print(f"- {desc}")
