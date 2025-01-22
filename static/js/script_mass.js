document.addEventListener('DOMContentLoaded', function () {
    const selectElement = document.getElementById('Xen');
    const massInput = document.getElementById('mass');

    selectElement.addEventListener('change', function () {
        const selectedText = selectElement.options[selectElement.selectedIndex].text;
        massInput.placeholder = selectedText; // Меняем текст placeholder
    });
});