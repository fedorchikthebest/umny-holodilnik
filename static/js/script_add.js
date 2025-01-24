const dcode = document.getElementById("qrcode")
dcode.style.visibility = "hidden"
var qrcode = new QRCode(dcode);
var mass_id = document.getElementById('Xen')
var mass_input = document.getElementById('mass')
const qr_button = document.getElementById('gen_qr')
masses = ['Штуки', "Вес Кг", "Объём Л"]



function utf8ToAscii(str) {
    const reg = /[\x7f-\uffff]/g; // charCode: [127, 65535]
    const replacer = (s) => {
        const charCode = s.charCodeAt(0);
        const unicode = charCode.toString(16).padStart(4, '0');
        return `\\u${unicode}`;
    };

    return str.replace(reg, replacer);
}



mass_id.addEventListener('change', function() {
    mass_input.placeholder=masses[mass_id.value]
});


qr_button.addEventListener('click', () => {
    dcode.style.visibility = "visible"
    qrcode.clear()
    let data = {
        "product_name": document.getElementById('productName').value,
        "stop_date": document.getElementById('stopDate').value,
        "count": document.getElementById('mass').value,
        "is_kg": document.getElementById('Xen').value,
        "class": document.getElementById('productClass').value,
        "start_date": document.getElementById('startDate').value,
        "B": document.getElementById('proteinsG').value,
        "J": document.getElementById('fatsG').value,
        "U": document.getElementById('carbsG').value
    }
    qrcode.makeCode(utf8ToAscii(JSON.stringify(data)))
})