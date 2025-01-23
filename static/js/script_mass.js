const deleteButton = document.getElementById('knokback');
console.log(deleteButton)

deleteButton.textContent = 'Удалить';
const deleteCell = document.createElement('td');
const deleteButton = document.createElement('button');
deleteButton.textContent = 'Удалить';
deleteButton.className = 'btn btn-danger'; // Добавляем класс Bootstrap для стиля
deleteButton.addEventListener('click', () => {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/api/delete/" + row.children[5].textContent, true);
    xhr.send(null);
    row.remove(); // Удаляем строку из таблицы
});
deleteCell.appendChild(deleteButton);
row.appendChild(deleteCell); // Добавляем ячейку с кнопкой удаления в строку
