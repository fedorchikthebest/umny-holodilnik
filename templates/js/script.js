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
const headers = ['Product Name', 'Stop Date', 'Count', 'Is KG'];
headers.forEach(headerText => {
    const th = document.createElement('th');
    th.textContent = headerText;
    headerRow.appendChild(th);
});
thead.appendChild(headerRow);
table.appendChild(thead);

// Создаем тело таблицы и заполняем его данными
const tbody = document.createElement('tbody');
res_t.forEach(value => {
    const row = document.createElement('tr');

    const cell1 = document.createElement('td');
    cell1.textContent = value.product_name;
    row.appendChild(cell1);

    const cell2 = document.createElement('td');
    cell2.textContent = value.stop_date;
    row.appendChild(cell2);

    const cell3 = document.createElement('td');
    cell3.textContent = value.count;
    row.appendChild(cell3);

    const cell4 = document.createElement('td');
    cell4.textContent = value.is_kg;
    row.appendChild(cell4);

    tbody.appendChild(row);
});
table.appendChild(tbody);