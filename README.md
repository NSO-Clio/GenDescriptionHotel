# GenDescriptionHotel

[![Code Size](https://img.shields.io/github/languages/code-size/NSO-Clio/GenDescriptionHotel)](https://github.com/NSO-Clio/GenDescriptionHotel)
<img alt="python" src="https://img.shields.io/badge/python-3.11-yellow.svg"/>

# Заказчик

<img style="width: 25%; height: auto;" src='https://github.com/user-attachments/assets/6469610a-5437-4ed8-8318-96fc403cd75d'>

MTC Travel, сделано в рамках программы Сириус.ИИ

# Проблематика

> Составление качественного описания отеля является сложной задачей, так как необходимо учитывать не только базовые услуги, но и выделять дополнительные опции, такие как доступ к спа, фитнесцентрам и специальные услуги. Удачно сформированное описание напрямую влияет на выбор клиента, что делает процесс генерации точных, информативных и привлекательных текстов ключевым для успешной конкуренции в сфере гостиничного бизнеса

# Структура проекта

- ```web-app``` - веб-приложение
- ```notebooks``` - анализ данных, моделей и настройка
- ```parser``` - дериктория с парсером отзывов

# Скринкаст

[!video](https://github.com/user-attachments/assets/d67e7e11-ba93-4841-8723-9da0c3361fae)

# Решение

На данном этапе мы реализовали генерацию описания относительно пунктов, т.е. пользователь заполняет форму и относительно формы модель делает генерацию описания.
- LLM: модель мы решили выбрать Qwen2.5-1.5B-Instruct

# Запуск

Про запуск приложения распиано тут [web-app](https://github.com/NSO-Clio/GenDescriptionHotel/tree/main/web-app)
