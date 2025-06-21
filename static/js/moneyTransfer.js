$(document).ready(function () {
    $('#transferTable').DataTable({
        responsive: true,
        columnDefs: [
            {responsivePriority: 1, targets: 2},
            {responsivePriority: 2, targets: 3},
            {responsivePriority: 3, targets: 6},
            {orderable: false, targets: [5, 6, 7]}
        ],
        ajax: {
            url: '/api/money-transfer',
            dataSrc: ''
        },
        columns: [
            {data: 'id'},
            {data: 'platform'},
            {
                data: 'cad_value',

                render: (data, type, row) => {

                    return `<span>${new Intl.NumberFormat(navigator.language, {
                        style: "currency",
                        currency: 'CAD',
                    }).format(data)}</span>`;
                }

            },
            {
                data: 'usd_value',

                render: (data, type, row) => {
                    return `<span>${new Intl.NumberFormat(navigator.language, {
                        style: "currency",
                        currency: 'USD',
                    }).format(data)}</span>`;

                }
            },
            {
                data: 'date',
                render: (data, type, row) => {
                    if (!data) return '';
                    const date = new Date(data);
                    if (type === 'sort') {
                        return date.toISOString().split('T')[0]; // Formato YYYY-MM-DD para ordenar
                    }
                    return date.toLocaleString('es-ES', {timeZone: 'America/Bogota'});
                }
            },
            {
                data: null,
                render: (data, type, row) => {

                    const editLink = `/money-transfer/edit/${row.id}`;
                    return `<a class='btn btn-outline-primary' href='${editLink}'>Edit</a>`;
                },
                width: '10%'
            },
            {
                data: null,
                render: (data, type, row) => {
                    const pk = row.id;
                    return `<button class='btn btn-outline-secondary' onclick="OpenTransferModal(${pk})">View</button>`;
                },
                width: '10%'

            },
            {
                data: null,
                render: (data, type, row) => {
                    return `<button class="btn btn-danger" data-id="${row.id}" id="delete-btn">Delete</button>`;
                },
                width: '10%'
            }
        ]

    });

});

function OpenTransferModal(pk) {
    fetch(`./${pk}`)
        .then(response => response.json())
        .then(data => {

            document.getElementById('modal-date').textContent = new Date(data.date).toLocaleString('es-ES', {timeZone: 'America/Bogota'});
            document.getElementById('modal-platform').textContent = data.platform;
            document.getElementById('modal-value-cad').textContent = data.cad_value ? `${new Intl.NumberFormat(navigator.language, {
                style: "currency",
                currency: 'CAD',
            }).format(data.cad_value)}` : 'N/A';
            document.getElementById('modal-value-usd').textContent = data.usd_value ? `${new Intl.NumberFormat(navigator.language, {
                style: "currency",
                currency: 'USD',
            }).format(data.usd_value)}` : 'N/A';
            document.getElementById('modal-commission').textContent = data.commission ? `${new Intl.NumberFormat(navigator.language, {
                style: 'currency',
                currency: 'USD'
            }).format(data.commission)}` : 'N/A';
            document.getElementById('modal-change').textContent = data.change_rate;
            document.getElementById('modal-processing').textContent = data.processing_days;
            document.getElementById('modal-isd').textContent = data.isd ? `${new Intl.NumberFormat(navigator.language, {
                style: 'currency',
                currency: 'USD'
            }).format(data.isd)}` : 'N/A';
            document.getElementById('modal-taxec').textContent = data.tax ? `${new Intl.NumberFormat(navigator.language, {
                style: 'currency',
                currency: 'USD'
            }).format(data.tax)}` : 'N/A';

            const modal = new bootstrap.Modal(document.getElementById('transferModal'));
            modal.show();

        });
};

$(document).on('click', '#delete-btn', function () {

    const transfer_id = $(this).data('id');
    if (confirm('Are you sure about delete this money transfer?')) {
        $.ajax({

            url: `/money-transfer/delete/${transfer_id}`,
            type: 'POST',
            headers: {'X-CSRFToken': csrfToken},
            success: function (response) {
                if (response.success) {
                    $("#transferTable").DataTable().ajax.reload();
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