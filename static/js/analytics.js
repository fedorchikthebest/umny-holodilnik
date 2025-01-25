const btn = document.getElementById("generateReport")
const start_date = document.getElementById("startDate")
const stop_date = document.getElementById("endDate")
let circle_chart = document.getElementById("circleChart")

const cc = new Chart(circle_chart, {
    type: 'doughnut',
    data: {
      labels: ['Удалённые', 'Существующие'],
      datasets: [{
        label: 'Продыкты',
        data: [0, 0],
        borderWidth: 1
      }]
    },
  });


function to_int_time(t){
	let e = t.split('-')
	ans = new Date(e[0], e[1] - 1, e[2])
	return ans.getTime() / 1000
}


async function create_chart(){
	let res = await fetch('/api/get_analytics/' + to_int_time(start_date.value) + '/' + to_int_time(stop_date.value))
	let res_t = await res.json()
	cc.data.datasets[0].data = [res_t.deleted.length, res_t.products.length]
	cc.update()
}

btn.addEventListener('click', () => create_chart())
