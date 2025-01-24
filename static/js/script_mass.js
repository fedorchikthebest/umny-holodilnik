const deleteButton = document.getElementById('huy');
const addButton = document.getElementById('add_button')
const xhr_delete = new XMLHttpRequest();
const xhr_adds = new XMLHttpRequest();

deleteButton.addEventListener('click', () => {
    console.log('321')
    xhr_delete.open("GET", "/api/delete/" + deleteButton.getAttribute('name'), true);
    xhr_delete.send(null);
});

addButton.addEventListener('click', ()=>{
    console.log(123)
    xhr_adds.open("GET", "/api/add_same/" + addButton.getAttribute('name'), true);
    xhr_adds.send(null);
})

xhr_delete.onload = function (e) {
    document.location.href = "/"
};

xhr_adds.onload = function (e) {
    alert('Товар добавлен')
};