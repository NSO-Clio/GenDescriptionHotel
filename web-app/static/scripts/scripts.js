function goToStep(step) {
    document.querySelectorAll('.form-step').forEach(stepDiv => stepDiv.classList.add('hidden'));
    document.getElementById(`step${step}`).classList.remove('hidden');
}

function showFeedbackSection() {
    document.getElementById("feedbackSection").classList.remove("hidden");
}

document.getElementById("chooseDescription1").addEventListener("click", () => {
    // Скрываем кнопку
    document.getElementById("chooseDescription1").classList.add("hidden");
    // Показываем блок с оценкой и комментарием
    document.getElementById("feedback1").classList.remove("hidden");
});

document.getElementById("chooseDescription2").addEventListener("click", () => {
    // Скрываем кнопку
    document.getElementById("chooseDescription2").classList.add("hidden");
    // Показываем блок с оценкой и комментарием
    document.getElementById("feedback2").classList.remove("hidden");
});

function generateDescription() {
    const hotelData = {
        hotelName: document.getElementById("hotelName").value.trim(),
        city: document.getElementById("CityAddress").value.trim(),
        hotelAddress: document.getElementById("hotelAddress").value.trim(),
        category: document.getElementById("category").value.trim(),
        services: document.getElementById("services").value.trim(),
        weather: document.getElementById("weather").value.trim(),
        language: document.getElementById("language").value.trim(),
        features: document.getElementById("features").value.trim(),
        textLength: document.getElementById("textLength").value.trim(), // Новый параметр
    };

    fetch('/generate_description', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(hotelData),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                console.error("Ошибка сервера:", data.error);
                alert("Произошла ошибка: " + data.error);
                return;
            }

            document.getElementById("generatedDescription1").textContent = data.description1;
            document.getElementById("generatedDescription2").textContent = data.description2;
            document.getElementById("example1").classList.remove("hidden");
            document.getElementById("example2").classList.remove("hidden");
        })
        .catch(error => {
            console.error("Ошибка:", error);
            alert("Произошла ошибка при обработке данных.");
        });
}


document.getElementById("submitFeedback1").addEventListener("click", () => {
    const rating = document.querySelector('input[name="rating1"]:checked')?.value;
    const comment = document.getElementById("userComment1").value.trim();

    if (!rating) {
        alert("Пожалуйста, выберите оценку!");
        return;
    }

    // Отправляем данные на сервер
    fetch('/submit_feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            description: document.getElementById("generatedDescription1").textContent,
            rating: rating,
            comment: comment,
            category: document.getElementById("category").value.trim()
        })
    })
        .then(response => response.json())
        .then(data => {
            alert("Спасибо за ваш отзыв!");
            // Действие после отправки
        })
        .catch(error => console.error("Ошибка:", error));
});

document.getElementById("submitFeedback2").addEventListener("click", () => {
    const rating = document.querySelector('input[name="rating2"]:checked')?.value;
    const comment = document.getElementById("userComment2").value.trim();

    if (!rating) {
        alert("Пожалуйста, выберите оценку!");
        return;
    }

    // Отправляем данные на сервер
    fetch('/submit_feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            description: document.getElementById("generatedDescription2").textContent,
            rating: rating,
            comment: comment,
            category: document.getElementById("category").value.trim()
        })
    })
        .then(response => response.json())
        .then(data => {
            alert("Спасибо за ваш отзыв!");
            // Действие после отправки
        })
        .catch(error => console.error("Ошибка:", error));
});

document.getElementById("chooseDescription1").addEventListener("click", () => {
document.getElementById("example2").classList.add("hidden"); // Скрыть второе описание
    sendChoice("description1"); // Отправить выбор на сервер
});

document.getElementById("chooseDescription2").addEventListener("click", () => {
    document.getElementById("example1").classList.add("hidden"); // Скрыть первое описание
    sendChoice("description2"); // Отправить выбор на сервер
});

document.getElementById("generateAgainBtn1").addEventListener("click", () => {
    // Запрос на сервер для получения нового описания
    fetch('/generate_description', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            hotelName: document.getElementById("hotelName").value,
            category: document.getElementById("category").value,
            services: document.getElementById("services").value,
            features: document.getElementById("features").value
        })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("generatedDescription1").textContent = data.description1;
            document.getElementById("generatedDescription2").textContent = data.description2;
            // Показываем первое описание и скрываем кнопку
            document.getElementById("example1").classList.remove("hidden");
            document.getElementById("generateAgain1").classList.add("hidden");
        })
        .catch(error => console.error("Ошибка:", error));
});

// Обработчик для генерации нового описания (для второго варианта)
document.getElementById("generateAgainBtn2").addEventListener("click", () => {
    // Запрос на сервер для получения нового описания
    fetch('/generate_description', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            hotelName: document.getElementById("hotelName").value,
            category: document.getElementById("category").value,
            services: document.getElementById("services").value,
            features: document.getElementById("features").value
        })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("generatedDescription1").textContent = data.description1;
            document.getElementById("generatedDescription2").textContent = data.description2;
            // Показываем второе описание и скрываем кнопку
            document.getElementById("example2").classList.remove("hidden");
            document.getElementById("generateAgain2").classList.add("hidden");
        })
        .catch(error => console.error("Ошибка:", error));
});

const categoryDescriptions = {
    "Горнолыжный отель": "Идеально подходит для любителей зимних видов спорта, предоставляя удобства для хранения снаряжения и близость к подъёмникам.",
    "Хостел": "Бюджетное жильё с общими комнатами, минимальными удобствами и возможностью завести новых друзей.",
    "Гостиница": "Классический вариант для туристов и деловых путешественников с широким спектром услуг.",
    "Бизнес-отели": "Идеальны для деловых поездок с удобствами вроде конференц-залов и рабочего пространства.",
    "Курортные отели": "Отели с бассейнами, СПА и развлечениями, часто расположены в живописных местах.",
    "Бутик-отели": "Изысканные отели с уникальным дизайном, предлагающие атмосферу уюта и эксклюзивности.",
    "Апартаменты и апарт-отели": "Удобны для длительного проживания, предоставляя оборудованную кухню и больше пространства.",
    "Мини-гостиницы": "Небольшие уютные отели, часто бюджетного или среднего класса.",
    "Спа отель": "Отели с акцентом на релаксацию и оздоровительные процедуры.",
    "Санаторий": "Место для лечения и восстановления здоровья с медицинскими услугами.",
    "Пансионат": "Идеальный вариант для семейного отдыха с включённым питанием.",
    "Мотель": "Жильё для автопутешественников, расположенное вдоль дорог.",
    "Эко отели": "Отели, ориентированные на экологичность и устойчивое развитие.",
    "Лоджи отель": "Загородное жильё в виде домиков, идеально для отдыха на природе."
};


document.getElementById('category').addEventListener('change', (e) => {
    const selectedCategory = e.target.value;
    const description = categoryDescriptions[selectedCategory] || 'Описание недоступно';
    document.getElementById('categoryDescription').innerText = description;
});

function sendChoice(choice) {
    fetch('/save_choice', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ choice: choice })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message); // Уведомление о сохранении
        alert(`Вы выбрали: ${choice}`); // Вывод сообщения пользователю
    })
    .catch(error => console.error("Ошибка:", error));
}
    