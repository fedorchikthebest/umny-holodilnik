const deleteButton = document.getElementById('huy');
console.log(deleteButton)
deleteButton.addEventListener('click', () => {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/api/delete/" + deleteButton.getAttribute('name'), true);
    xhr.send(null);
    document.location.href = "/"
});