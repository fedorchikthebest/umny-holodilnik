// Получаем данные из API
let res = await fetch("/api");
let res_t = await res.json();

// Находим таблицу в HTML
const table = document.querySelector('table.table-bordered');

// Очищаем таблицу перед добавлением новых данных
table.innerHTML = '';

// Создаем заголовок таблицы
const thead = document.createElement('thead');
const headerRow = document.createElement('tr');
const headers = Object.keys(res_t[0]); // Используем ключи первого объекта как заголовки
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

    headers.forEach(header => {
        const cell = document.createElement('td');
        cell.textContent = value[header];
        row.appendChild(cell);
    });

    tbody.appendChild(row);
});
table.appendChild(tbody);

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