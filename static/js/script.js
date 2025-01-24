// Получаем данные из API
let res = await fetch("/api");
let res_t = await res.json();
const data_types = ['Шт', 'Кг', 'Л']

// Находим таблицу в HTML
const table = document.querySelector('table.table-bordered');
var is_filtered = false;

// Очищаем таблицу перед добавлением новых данных
table.innerHTML = '';

// Создаем заголовок таблицы
const thead = document.createElement('thead');
const headerRow = document.createElement('tr');
const headers = ["id", "product_name", "class", "count", "is_kg", "start_date", "stop_date", "B", "J", "U"]
let currentSortColumn = null;

headers.forEach((headerText, index) => {
    const th = document.createElement('th');
    th.textContent = headerText;
    th.style.cursor = 'pointer';
    th.style.position = 'relative';
    th.addEventListener('click', () => sortTable(index, th));
    headerRow.appendChild(th);
});
thead.appendChild(headerRow);
table.appendChild(thead);

// Создаем тело таблицы и заполняем его данными
const tbody = document.createElement('tbody');
res_t.forEach(value => {
    const row = document.createElement('tr');
    value['is_kg'] = data_types[value['is_kg']]

    headers.forEach(header => {
        const cell = document.createElement('td');
        cell.textContent = value[header];

        // Добавляем обработчик клика для ячейки с названием товара
        if (header === "product_name") {
            cell.style.cursor = 'pointer'; // Указываем, что ячейка кликабельная
            cell.addEventListener('click', () => {
                window.location.href = `/infabout?pid=${value.id}`; // Перенаправляем на страницу товара
            });
        }

        row.appendChild(cell);
    });

    // Добавляем кнопку удаления
    const deleteCell = document.createElement('td');
    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Удалить';
    deleteButton.className = 'btn btn-danger'; // Добавляем класс Bootstrap для стиля
    deleteButton.addEventListener('click', () => {
        const xhr = new XMLHttpRequest();
        xhr.open("GET", "/api/delete/" + row.children[0].textContent, true);
        xhr.send(null);
        row.remove(); // Удаляем строку из таблицы
    });
    deleteCell.appendChild(deleteButton);
    row.appendChild(deleteCell); // Добавляем ячейку с кнопкой удаления в строку

    tbody.appendChild(row);
});
table.appendChild(tbody);

// Получаем поле ввода для поиска
const searchInput = document.getElementById('searchInput');

// Добавляем обработчик события для поиска
searchInput.addEventListener('input', () => {
    const filter = searchInput.value.toLowerCase();
    const rows = Array.from(tbody.querySelectorAll('tr'));

    rows.forEach(row => {
        const cells = Array.from(row.querySelectorAll('td'));
        const rowText = cells.map(cell => cell.textContent.toLowerCase()).join(' ');
        row.style.display = rowText.includes(filter) ? '' : 'none';
    });
});

// Функция для сортировки таблицы
let sortDirection = true; // true для возрастания, false для убывания
function sortTable(columnIndex, th) {
    const rows = Array.from(tbody.querySelectorAll('tr'));
    rows.sort((a, b) => {
        const cellA = a.children[columnIndex].textContent;
        const cellB = b.children[columnIndex].textContent;

        if (!isNaN(cellA) && !isNaN(cellB)) {
            return sortDirection ? cellA - cellB : cellB - cellA;
        } else {
            return sortDirection ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
        }
    });

    // Переключаем направление сортировки
    sortDirection = !sortDirection;

    // Очищаем тело таблицы и добавляем отсортированные строки
    tbody.innerHTML = '';
    rows.forEach(row => tbody.appendChild(row));

    // Обновляем индикатор сортировки
    updateSortIndicator(th);
}

function updateSortIndicator(th) {
    // Удаляем предыдущие индикаторы
    if (currentSortColumn) {
        currentSortColumn.textContent = currentSortColumn.textContent.replace(' ↑', '').replace(' ↓', '');
    }

    // Добавляем новый индикатор
    th.textContent = th.textContent.replace(' ↑', '').replace(' ↓', '');
    th.textContent += sortDirection ? ' ↑' : ' ↓';

    // Обновляем текущий столбец сортировки
    currentSortColumn = th;
}

// Функция для обновления заголовков таблицы
function updateTableHeaders() {
    const headers = [
        "id",
        "Название",
        "Класс",
        "Количество",
        "Тип данных",
        "Дата изготовления",
        "Дата истичения",
        "Белки",
        "Жиры",
        "Углеводы"
    ];

    const headerRow = table.querySelector('thead tr');
    headerRow.innerHTML = ''; // Очищаем текущие заголовки

    headers.forEach((headerText, index) => {
        const th = document.createElement('th');
        th.textContent = headerText;
        th.style.cursor = 'pointer'; // Устанавливаем курсор для указания на возможность сортировки
        th.addEventListener('click', () => sortTable(index, th)); // Добавляем обработчик события сортировки
        headerRow.appendChild(th);
    });
}

// Вызов функции обновления заголовков после загрузки данных
updateTableHeaders();

// Функция для фильтрации строк по сроку годности
function filterExpiringItems() {
    const rows = Array.from(tbody.querySelectorAll('tr'));
    if (is_filtered) {
        document.getElementById('ZOV').textContent = "Показать просрочку"
        rows.forEach(row => {
            row.style.display = ''; // Показываем только близкие к истечению
        }
        );
        is_filtered = false
        return 0;
    }
    document.getElementById('ZOV').textContent = "Показать всё"

    const today = new Date();
    const thresholdDate = new Date();
    thresholdDate.setDate(today.getDate() - 3); // Устанавливаем порог на 7 дней

    rows.forEach(row => {
        const expiryDateCell = row.children[6].textContent.split('-'); // Предполагается, что дата истечения в 6-м столбце
        let CellDate = new Date(expiryDateCell[0], expiryDateCell[1] - 1, expiryDateCell[2]);
        if (expiryDateCell) {
            row.style.display = CellDate <= thresholdDate ? '' : 'none'; // Показываем только близкие к истечению
        }
    });
    is_filtered = true
}
const searchButton = document.getElementById('ZOV')
searchButton.addEventListener('click', filterExpiringItems)
// Добавляем обработчик события для кнопки фильтрации