document.addEventListener('DOMContentLoaded', function() {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    document.body.appendChild(tooltip);

    const selectedSeats = new Set(); // Множество для хранения выбранных мест

    document.querySelectorAll('circle[data-tooltip]').forEach(function(circle) {
        circle.addEventListener('mouseover', function() {
            tooltip.innerHTML = circle.getAttribute('data-tooltip').replace(/\n/g, '<br>');
            tooltip.style.opacity = 1;
        });
        circle.addEventListener('mousemove', function(event) {
            tooltip.style.left = event.pageX - 70 + 'px';
            tooltip.style.top = event.pageY - 130 + 'px';
        });
        circle.addEventListener('mouseout', function() {
            tooltip.style.opacity = 0;
        });
        circle.addEventListener('click', function() {
            const seatId = circle.getAttribute('id');

            // Проверяем максимальное количество выбранных мест
            if (selectedSeats.size >= 5 && !selectedSeats.has(seatId)) {
                alert('Вы можете выбрать только 5 мест.');
                return;
            }

            if (selectedSeats.has(seatId)) {
                selectedSeats.delete(seatId); // Если место уже выбрано, удаляем его из множества
                circle.classList.remove('selected'); // Удаляем класс для выделения места
            } else {
                selectedSeats.add(seatId); // Если место не выбрано, добавляем его в множество
                circle.classList.add('selected'); // Добавляем класс для выделения места
            }

            // Отображаем выбранные пользователем места
            updateSelectedSeatsInfo();
        });
    });

    function updateSelectedSeatsInfo() {
        const selectedSeatsInfoContainer = document.getElementById('selected-seats-info');
        selectedSeatsInfoContainer.innerHTML = ''; // Очищаем содержимое контейнера

        if (selectedSeats.size === 0) {
            selectedSeatsInfoContainer.textContent = 'Выберите место';
        } else {
            selectedSeatsInfoContainer.textContent = ' ';

            // Создаем список выбранных мест и добавляем их в контейнер
            const selectedSeatsList = document.createElement('ul');
            selectedSeats.forEach(function(seatId) {
                const circle = document.getElementById(seatId);
                const sector = circle.getAttribute('data-sector');
                const row = circle.getAttribute('data-row');
                const place = circle.getAttribute('data-place');
                const listItem = document.createElement('li');
                listItem.textContent = `Сектор: ${sector}, Ряд: ${row}, Место: ${place}`;
                selectedSeatsList.appendChild(listItem);
            });
            selectedSeatsInfoContainer.appendChild(selectedSeatsList);
        }
    }

    const bookingForm = document.getElementById('booking-form');

    // Add event listener for form submission
    bookingForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        // Если нет выбранных мест, не отправляем форму
        if (selectedSeats.size === 0) {
            alert('Пожалуйста, выберите места.');
            return;
        }

        // Создаем массив для хранения информации о выбранных местах
        const selectedSeatsInfo = [];

        // Получаем информацию о каждом выбранном месте и добавляем ее в массив
        selectedSeats.forEach(function(seatId) {
            const circle = document.getElementById(seatId);
            const sector = circle.getAttribute('data-sector');
            const row = circle.getAttribute('data-row');
            const place = circle.getAttribute('data-place');
            const price = circle.getAttribute('data-price');
            selectedSeatsInfo.push({ sector, row, place, price });
        });

        // Заполняем скрытое поля формы с информацией о выбранных местах
        document.getElementById('selected_seats').value = JSON.stringify(selectedSeatsInfo);

        // Отправляем форму на сервер
        bookingForm.submit();
    });
});


