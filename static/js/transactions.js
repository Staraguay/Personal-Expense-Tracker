$(document).ready(function () {

    $('#transactionTable').DataTable({
        columnDefs: [
            {targets: [5, 6, 7], orderable: false},
            {targets: 5, className: "text-end"},
            {targets: 7, className: "text-start"},
        ],
        ajax: {
            url: '/api/transactions',
            dataSrc: ''
        },
        columns: [
            {data: 'id'},
            {data: 'description'},
            {
                data: 'value_cad',
                render: (data, type, row) => {
                    const color = row.transaction_type === 'Expenses' ? 'text-danger' : 'text-success';
                    const sign = row.transaction_type === 'Expenses' ? '-' : '+';
                    return `<span class='${color}'>${sign}${new Intl.NumberFormat('en-CA', {
                        style: "currency",
                        currency: 'CAD',
                    }).format(data)}</span>`;
                }
            },
            {
                data: 'value_usd',
                render: (data, type, row) => {
                    const color = row.transaction_type === 'Expenses' ? 'text-danger' : 'text-success';
                    const sign = row.transaction_type === 'Expenses' ? '-' : '+';
                    return `<span class='${color}'>${sign}${new Intl.NumberFormat('en-US', {
                        style: "currency",
                        currency: 'USD',
                    }).format(data)}</span>`;
                }
            },
            {data: 'category'},
            {
                data: 'date',
                render: (data, type, row) => {
                    if (!data) return '';
                    const date = new Date(data);
                    return date.toLocaleString('es-ES', {timeZone: 'America/Bogota'});
                },

            },
            {
                data: null,
                render: (data, type, row) => {
                    // Create a dynamic link using the row ID
                    const editLink = `/transactions/edit/${row.id}`;
                    return `<a class='btn btn-outline-primary' href='${editLink}'>Edit</a>`;
                },
                width: '10%',

            },
            {
                data: null,
                render: (data, type, row) => {
                    // Create a dynamic link using the row ID
                    const pk = row.id;
                    return `<button class='btn btn-outline-secondary' onclick="OpenTransactionModal(${pk})">View</button>`;
                },
                width: '10%'
            },
            {
                data: null,
                render: (data, type, row) => {

                    return `<button class="btn btn-danger" data-id="${row.id}" id="delete-btn">Delete</button>`

                },
                width: '10%'
            },
        ]
    });
});

function OpenTransactionModal(pk) {

    fetch(`./${pk}`)
        .then(response => response.json())
        .then(data => {

            document.getElementById('modal-date').textContent = new Date(data.date).toLocaleString('es-ES', {timeZone: 'America/Bogota'});
            document.getElementById('modal-type').textContent = data.transaction_type;
            document.getElementById('modal-value-cad').textContent = data.value_cad ? `${new Intl.NumberFormat('en-CA', {
                style: "currency",
                currency: 'CAD',
            }).format(data.value_cad)}` : 'N/A';
            document.getElementById('modal-value-usd').textContent = data.value_usd ? `${new Intl.NumberFormat(navigator.language, {
                style: "currency",
                currency: 'USD',
            }).format(data.value_usd)}` : 'N/A';
            document.getElementById('modal-payment').textContent = data.payment_type;
            document.getElementById('modal-shop').textContent = data.shop;
            document.getElementById('modal-category').textContent = data.category;
            document.getElementById('modal-description').textContent = data.description;
            document.getElementById('modal-isd').textContent = data.isd ? `${new Intl.NumberFormat(navigator.language, {
                style: "currency",
                currency: 'USD',
            }).format(data.isd)}` : 'N/A';
            document.getElementById('modal-taxec').textContent = data.tax_ec ? `${new Intl.NumberFormat(navigator.language, {
                style: "currency",
                currency: 'USD',
            }).format(data.tax_ec)}` : 'N/A';

            const modal = new bootstrap.Modal(document.getElementById('transactionModal'));
            modal.show();
        })
}

$(document).on('click', '#delete-btn', function () {

    const transaction_id = $(this).data('id');

    if (confirm('Are you sure about delete this transaction?')) {
        $.ajax({
            url: `/transactions/delete/${transaction_id}`,
            type: 'POST',
            headers: {'X-CSRFToken': csrfToken},
            success: function (response) {
                if (response.success) {
                    $('#transactionTable').DataTable().ajax.reload();
                } else {
                    alert('Error while deleting');
                }
            },
            error: function () {
                alert('Error');
            }


        });
    }
    ;

});