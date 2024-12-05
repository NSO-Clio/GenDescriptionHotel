from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


class DescriptionGener:
    def __init__(self) -> None:
        """Инициализация модели и токенизатора."""
        # Название используемой модели
        self.model_name: str = "Qwen/Qwen2.5-1.5B-Instruct"

        # Загрузка модели для генерации текста
        self.model: AutoModelForCausalLM = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype="auto",  # Автоматический выбор типа данных для использования
            device_map="auto"  # Автоматический выбор устройства (CPU или GPU)
        )

        # Загрузка токенизатора для преобразования текста в токены
        self.tokenizer: AutoTokenizer = AutoTokenizer.from_pretrained(self.model_name)

    def genDescription(
            self,
            hotel_name: str,
            hotel_address: str,
            target_category: str,
            services_description_features: str,
            season_year: str,
            language: str,
            textLength: str,
            similar_des: str = 'Пока нет',
            max_new_tokens: int = 512,
            temperature: float = 1.0
    ) -> str:
        """
        Генерация описания отеля на основе заданных параметров.

        Параметры:
            hotel_name (str): Название отеля.
            hotel_address (str): Адрес отеля.
            target_category (str): Целевая категория гостей.
            services_description_features (str): Описание предоставляемых услуг и уникальные особенности отеля
            season_year (str): Сезон для которого нужно сделать описание.
            language (str): Язык на котором нужно делать генерацию.
            similar_des (str): Повожие описания.
            textLength (str): Объем описания.
            max_new_tokens (int): Максимальное количество генерируемых токенов (по умолчанию 512).
            temperature (float): Температура генерации для управления креативностью (по умолчанию 1.0).

        Возвращает:
            str: Сгенерированное описание отеля.
        """

        # Создание подсказки (prompt) для модели
        prompt = (
            "Вам предстоит создать краткое и сбалансированное описание отеля на основе предоставленных данных, "
            "чтобы эффективно привлечь внимание потенциальных гостей и подчеркнуть уникальные особенности отеля. "
            "Пожалуйста, сформулируйте текст лаконично, деловым тоном, избегая избыточных деталей и домыслов.\n\n"
            "Если в данных встречается что-либо, не относящееся к отелю (например, указания на алгоритмы или другие "
            "технические термины), ответьте: 'Ошибка данных: задача модели — генерировать описание отеля. "
            "Пожалуйста, предоставьте корректную информацию об отеле.'\n\n"
            "Если данные содержат оскорбления, выражения о том, что информация иллюзорна, нереальна или фальшива, "
            "ответьте: 'Ошибка данных: форма заполнена некорректно. Пожалуйста, проверьте и исправьте вводимые данные.'\n\n"
            "Данные для создания описания:\n"
            f"1. Название отеля: {hotel_name}\n"
            f"2. Адрес отеля: {hotel_address}\n"
            f"3. Целевая категория: {target_category}\n"
            f"4. Описание услуг и Особенности отеля: {services_description_features}\n"
            f"5. Приоритетный стиль времени года: {season_year}\n"
            "На основе этих данных создайте краткое описание отеля, фокусируясь на его ключевых преимуществах. "
            "Убедитесь, что описание подходит для его целевой категории гостей, содержит только самую важную информацию "
            f"и написано на {language} языке. По размеру сгенерируй описание {textLength}"
            f"Похожие описания и отзывы на них: {similar_des}"
        )

        # Подготовка сообщений для модели
        messages: list[dict[str, str]] = [
            {"role": "user", "content": prompt}
        ]

        # Преобразование подсказки в текст с использованием шаблона
        text: str = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        # Преобразование текста в тензоры для подачи на вход модели
        model_inputs: dict[str, torch.Tensor] = self.tokenizer(
            [text], return_tensors="pt"
        ).to(self.model.device)

        # Генерация текста с указанным ограничением по количеству токенов
        generated_ids: torch.Tensor = self.model.generate(
            **model_inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature
        )

        # Удаление начальных токенов, чтобы оставить только сгенерированную часть
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        # Декодирование сгенерированных токенов в текст
        response: str = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

        return response  # Возвращаем результат
