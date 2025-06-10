// generate a new color

function generateNewColor() {
    let symbols, color;
    symbols = "0123456789ABCDEF";
    color = "#";

    for (let i = 0; i < 6; i++) {
        color = color + symbols[Math.floor(Math.random() * 16)];
    }

    return color;
}

$(document).ready(function () {

    const validCurrency = ["USD", "CAD"];
    let currency = new URLSearchParams(location.search).get("currency");
    $("#switch").prop("checked", currency === "USD" && validCurrency.includes(currency));

    ExpensesDoughnut();
    IncomingDoughnut();
    HistoryData();


    // render the expenses doughnut in home
    function ExpensesDoughnut() {
        fetch(`/api/expenses-summary/?currency=${currency}`)
            .then(response => response.json())
            .then(result => {
                const fetch_data = result.data;
                const fetch_labels = result.labels;

                if (!fetch_labels.length || !fetch_data.length) {
                    const defaultMessage = document.getElementById('donut1');
                    if (defaultMessage) {
                        const child = document.createElement('span');
                        document.getElementById('myDoughnut1').style.display = 'None';
                        child.innerText = 'No data yet';
                        defaultMessage.appendChild(child);
                    }
                    return;
                }

                const colors = fetch_data.map(() => generateNewColor());

                const data = {
                    labels: fetch_labels,
                    datasets: [
                        {
                            //label: 'Dataset 1',
                            data: fetch_data,
                            backgroundColor: colors,
                            hoverOffset: 10,
                        }
                    ]
                };

                const config = {
                    type: 'doughnut',
                    data: data,
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'right',
                            },
                            title: {
                                display: false,
                                text: ''
                            }
                        },
                        cutout: "60%",
                    },
                };
                //render de donut
                const myChart = new Chart($("#myDoughnut1"), config);

            })
            .catch(error => {
                console.error('Error cargando datos del API:', error);
            });
    }

    function IncomingDoughnut() {

        fetch(`/api/incoming-summary/?currency=${currency}`)
            .then(response => response.json())
            .then(result => {

                const fetch_data = result.data;
                const fetch_labels = result.labels;

                if (!fetch_labels.length || !fetch_data.length) {
                    const defaultMessage = document.getElementById('donut2');
                    if (defaultMessage) {
                        const child = document.createElement('span');
                        document.getElementById('myDoughnut2').style.display = 'None';
                        child.innerText = 'No data yet';
                        defaultMessage.appendChild(child);
                    }
                    return;
                }

                let colors = fetch_data.map(() => generateNewColor());

                const data = {
                    labels: fetch_labels,
                    datasets: [
                        {
                            //label: 'Dataset 1',
                            data: fetch_data,
                            backgroundColor: colors,
                            hoverOffset: 10,
                        }
                    ]
                };

                const config = {
                    type: 'doughnut',
                    data: data,
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'right',
                            },
                            title: {
                                display: false,
                                text: ''
                            }
                        },
                        cutout: "60%",
                    },
                };
                //render de donut
                const myChart = new Chart($("#myDoughnut2"), config);
            })
            .catch(error => {
                console.error('Error cargando datos del API:', error);
            });


    }

    function HistoryData() {

        fetch(`/api/history/?currency=${currency}`)
            .then(response => response.json())
            .then(result => {
                const fetch_data_expenses = Object.values(result['Expenses']);  // Gastos
                const fetch_data_incoming = Object.values(result['Incomings']); // Ingresos
                const labels = Object.keys(result['Expenses']);
                const data = {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Expenses',
                            data: fetch_data_expenses,
                            borderColor: "rgb(235, 67, 52)",
                            backgroundColor: "rgba(235, 67, 52,0.5)",
                        },
                        {
                            label: 'Incoming',
                            data: fetch_data_incoming,
                            borderColor: "rgb(75, 192, 192)",
                            backgroundColor: "rgba(75, 192, 192,0.5)",
                        }
                    ]
                };

                const config = {
                    type: 'line',
                    data: data,
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'top',
                            },
                            title: {
                                display: false,
                                text: ''
                            }
                        }
                    },
                };
                //render line chart
                const myChart = new Chart($("#historyData"), config);

            });
    }

})

$("#switch").change(function () {

    const currency = this.checked ? 'USD' : 'CAD';
    window.location.href = `/home/?currency=${currency}`;


});

