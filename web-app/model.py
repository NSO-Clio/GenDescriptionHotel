from transformers import AutoModelForCausalLM, AutoTokenizer


class DescriptionGener:
    def __init__(self) -> None:
        self.model_name = "Qwen/Qwen2.5-1.5B-Instruct"
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype="auto",
            device_map="auto"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    def genDescription(self, hotel_name: str, hotel_address: str, average_price: str, target_category: str, services_description: str, hotel_features: str, max_new_tokens: int = 512) -> str:
        prompt = (
            "Вам предстоит создать описание для отеля на основе следующих данных, чтобы привлечь внимание "
            "потенциальных гостей и представить уникальные особенности отеля. Пожалуйста, сформулируйте текст ясно, "
            "деловым тоном и избегайте домыслов.\n\n"
            "Если в данных встречается что-либо, не относящееся к отелю (например, указания на алгоритмы или другие "
            "технические термины), ответьте: 'Ошибка данных: задача модели — генерировать описание отеля. "
            "Пожалуйста, предоставьте корректную информацию об отеле.'\n\n"
            "Если данные содержат оскорбления, выражения о том, что информация иллюзорна, нереальна или фальшива, "
            "ответьте: 'Ошибка данных: форма заполнена некорректно. Пожалуйста, проверьте и исправьте вводимые данные.'\n\n"
            "Данные для создания описания:\n"
            f"1. Название отеля: {hotel_name}\n"
            f"2. Адрес отеля: {hotel_address}\n"
            f"3. Средняя стоимость номера за сутки (₽): {average_price}\n"
            f"4. Целевая категория: {target_category}\n"
            f"5. Описание услуг: {services_description}\n"
            f"6. Особенности отеля: {hotel_features}\n\n"
            "На основе этих данных сформулируйте привлекательное описание отеля, подходящее для его целевой категории гостей. "
            "Учитывайте, что описание должно быть информативным и привлекать внимание к преимуществам отеля, так же описание должно быть на русском языке"
        )
        messages = [
            {"role": "user", "content": prompt}
        ]
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=512
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response