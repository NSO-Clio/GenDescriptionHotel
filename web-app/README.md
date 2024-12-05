# Web-App

Основная папка в которой находится веб-приложения для решения данной задачи

## Структура

- `app.py` - файл с API проекта
- `conf.py` - конфиг файл с ключем к google API
- `data_knowledge.py` - реализация базы знаний модели
- `get_geo.py` - получение ближайших к отелю достопримечательностей
- `model.py` - файл с классом модели и ее настроеным промптом
- `requirements.txt` - requirements файл с библиотеками для работы с приложением

## Настройка

В файле `conf.py` нужно указать ваш `API_KEY_GOOGLE_MAPS`

## Запуск

- Для начала скачаем репозиторий и перейдем в нужный раздел

```
git clone https://github.com/NSO-Clio/GenDescriptionHotel.git

cd GenDescriptionHotel

cd web-app
```

- Теперь скачаем все библиотеки

```
pip install -r requirements.txt
```

- После запустим приложение

```
python app.py
```
