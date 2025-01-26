const btn = document.getElementById("generateReport");
const start_date = document.getElementById("startDate");
const stop_date = document.getElementById("endDate");
let circle_chart = document.getElementById("circleChart");
let p_chart = document.getElementById("potreblenieChart");
let d_chart = document.getElementById("deleteChart");

const colors = ['#FF6384', '#36A2EB'];

const pc = new Chart(p_chart, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: 'Хранится',
            data: [],
            borderWidth: 1
        }]
    },
});

const dc = new Chart(d_chart, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: 'Удалено',
            data: [],
            borderWidth: 1
        }]
    },
});

const cc = new Chart(circle_chart, {
    type: 'doughnut',
    data: {
        labels: ['Удалённые', 'Существующие', 'Просроченные удалённые', "Просроченные существующие"],
        datasets: [{
            label: 'Продукты',
            data: [0, 0, 0],
            borderWidth: 1
        }]
    },
});

function to_int_time(t) {
    let e = t.split('-');
    ans = new Date(e[0], e[1] - 1, e[2]);
    return ans.getTime() / 1000;
}

async function create_chart() {
    let res = await fetch('/api/get_analytics/' + to_int_time(start_date.value) + '/' + to_int_time(stop_date.value));
    let res_t = await res.json();
	console.log(res_t.deleted[0])
    cc.data.datasets[0].data = [res_t.deleted.filter(x => to_int_time(x.stop_date) >= x.delete_time).length, res_t.products.filter(x => to_int_time(x.stop_date) >= to_int_time(stop_date.value)).length, res_t.deleted.filter(x => to_int_time(x.stop_date) < x.delete_time).length, res_t.products.filter(x => to_int_time(x.stop_date) < to_int_time(stop_date.value)).length]
    cc.update();

    let r1 = new Set();
    let d1 = new Set();

    res_t.products.forEach((e) => r1.add(e.product_name));
    res_t.deleted.forEach((e) => d1.add(e.product_name));

    pc.data.datasets[0].data = [];
    r1.forEach((e) => pc.data.datasets[0].data.push(res_t.products.filter(x => x.product_name === e).length));
    pc.data.labels = Array.from(r1);
    pc.update();

    dc.data.datasets[0].data = [];
    d1.forEach((e) => dc.data.datasets[0].data.push(res_t.deleted.filter(x => x.product_name === e).length));
    dc.data.labels = Array.from(d1);
    dc.update();
}

btn.addEventListener('click', () => create_chart());
