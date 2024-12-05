let loadingInterval; // Переменная для хранения идентификатора setInterval

function generateDescription() {
    const hotelName = document.getElementById('hotelName').value;
    const hotelAddress = document.getElementById('hotelAddress').value;
    const pricePerNight = document.getElementById('pricePerNight').value;
    const category = document.getElementById('category').value;
    const services = document.getElementById('services').value;
    const features = document.getElementById('features').value;

    // Проверка на заполнение всех полей
    if (!hotelName || !pricePerNight || !category || !services || !features) {
        alert('Пожалуйста, заполните все обязательные поля.');
        return false;
    }

    const data = {
        hotelName: hotelName,
        hotelAddress: hotelAddress,
        pricePerNight: pricePerNight,
        category: category,
        services: services,
        features: features,
    };

    document.getElementById('result').style.display = 'none'; // Скрыть результат перед отправкой
    document.getElementById('description').innerText = ''; // Очистить прошлое описание

    // Показать анимацию "Идет генерация..."
    const loadingText = document.getElementById('loading');
    const dots = document.getElementById('dots');
    loadingText.style.display = 'block';
    let dotCount = 0;

    loadingInterval = setInterval(() => {
        dots.innerText = '.'.repeat(dotCount);
        dotCount = (dotCount + 1) % 4;
    }, 500); // Интервал для обновления точек

    fetch('/get_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Сеть ответила с ошибкой');
        }
        return response.json();
    })
    .then(data => {
        clearInterval(loadingInterval); // Остановить анимацию
        loadingText.style.display = 'none'; // Скрыть анимацию

        document.getElementById('description').innerText = data.description;
        document.getElementById('result').style.display = 'block';
    })
    .catch(error => {
        clearInterval(loadingInterval); // Остановить анимацию
        loadingText.style.display = 'none'; // Скрыть анимацию
        alert('Произошла ошибка при получении данных. Пожалуйста, попробуйте еще раз.');
        console.error('Ошибка:', error);
    });

    return false; // Не отправлять форму
}
