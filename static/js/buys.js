
let res = await fetch("/api/get_buys");
let res_t = await res.json();
const data_types = ['Шт', 'Кг', 'Л']
console.log(res_t)

const table = document.querySelector('table.table-bordered');
var is_filtered = false;

table.innerHTML = '';


const thead = document.createElement('thead');
const headerRow = document.createElement('tr');
const headers = ["id", "product_name", "class", "count", "is_kg", "start_date", "stop_date", "B", "J", "U", "Удалить"]
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


const tbody = document.createElement('tbody');
res_t.forEach(value => {
    const row = document.createElement('tr');
    value['is_kg'] = data_types[value['is_kg']]

    headers.forEach((header, index) => {
        const cell = document.createElement('td');
        cell.textContent = value[header];

       
        if (header === "product_name") {
            cell.style.cursor = 'pointer'; 
            cell.addEventListener('click', () => {
                window.location.href = `/infabout?pid=${value.id}`;
            });
        }

       

        if (header === "Удалить") { 
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Удалить';
            deleteButton.className = 'btn btn-danger'; 
            deleteButton.addEventListener('click', () => {
                const xhr = new XMLHttpRequest();
                xhr.open("GET", "/api/delete_buy/" + row.children[0].textContent, true);
                xhr.send(null);
                row.remove(); 
            });
            cell.appendChild(deleteButton); 
        }

        row.appendChild(cell);
    });

    tbody.appendChild(row);
});
table.appendChild(tbody);


const searchInput = document.getElementById('searchInput');


searchInput.addEventListener('input', () => {
    const filter = searchInput.value.toLowerCase();
    const rows = Array.from(tbody.querySelectorAll('tr'));

    rows.forEach(row => {
        const cells = Array.from(row.querySelectorAll('td'));
        const rowText = cells.map(cell => cell.textContent.toLowerCase()).join(' ');
        row.style.display = rowText.includes(filter) ? '' : 'none';
    });
});

let sortDirection = true; 
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

   
    sortDirection = !sortDirection;

  
    tbody.innerHTML = '';
    rows.forEach(row => tbody.appendChild(row));

  
    updateSortIndicator(th);
}

function updateSortIndicator(th) {
   
    if (currentSortColumn) {
        currentSortColumn.textContent = currentSortColumn.textContent.replace(' ↑', '').replace(' ↓', '');
    }


    th.textContent = th.textContent.replace(' ↑', '').replace(' ↓', '');
    th.textContent += sortDirection ? ' ↑' : ' ↓';

    currentSortColumn = th;
}

function updateTableHeaders() {
    const headers = [
        "id",
        "Название",
        "Класс",
        "Количество",
        "Тип данных",
        "Дата изготовления",
        "Дата истечения",
        "Белки",
        "Жиры",
        "Углеводы",
        "Удалить"
    ];

    const headerRow = table.querySelector('thead tr');
    headerRow.innerHTML = ''; 

    headers.forEach((headerText, index) => {
        const th = document.createElement('th');
        th.textContent = headerText;
        th.style.cursor = 'pointer'; 
        th.addEventListener('click', () => sortTable(index, th)); 
        headerRow.appendChild(th);
    });
}


updateTableHeaders();

function filterExpiringItems() {
    const rows = Array.from(tbody.querySelectorAll('tr'));
    if (is_filtered) {
        document.getElementById('ZOV').textContent = "Показать просрочку"
        rows.forEach(row => {
            row.style.display = '';
        }
        );
        is_filtered = false
        return 0;
    }
    document.getElementById('ZOV').textContent = "Показать всё"

    const today = new Date();
    const thresholdDate = new Date();
    thresholdDate.setDate(today.getDate() - 3); 

    rows.forEach(row => {
        const expiryDateCell = row.children[6].textContent.split('-');
        let CellDate = new Date(expiryDateCell[0], expiryDateCell[1] - 1, expiryDateCell[2]);
        if (expiryDateCell) {
            row.style.display = CellDate <= thresholdDate ? '' : 'none';
        }
    });
    is_filtered = true
}
const searchButton = document.getElementById('ZOV')
searchButton.addEventListener('click', filterExpiringItems)
