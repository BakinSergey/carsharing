var current_cars = new Object();

$(function () {

    $("#show_garage").on('click', function () {
        // all cars params datatables will be here
        show_garage()
    });

    $("#add_cherry_7").on('click', function () {
        block_ui();
        $.ajax({
            url: $.ajax_add_car_url,
            type: 'GET',
            dataType: 'json',
            data: 'model=cherry_7',
            success: success_adding,
            error: error_adding
        })
    });

    $("#add_car").on('click', function () {
        block_ui();
        $.ajax({
            url: $.ajax_add_car_url,
            type: 'GET',
            dataType: 'json',
            success: success_adding,
            error: error_adding
        })
    });

    $("#del_car").on('click', function () {
        $.ajax({
            url: $.ajax_del_car_url,
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                cars_deleted = data['cars'][1];
                console.log('deleted:', cars_deleted);
                $('#dropmenu').empty();
                write_car_list_text();
                custom_swal_animate();
            },
            error: function (data) {
                swal.fire({
                    title: "Ошибка",
                    text: "Ошибка при удалении, разберись...",
                    icon: "error"
                });
            }
        });
    });


    // чтобы работали клики на добавленных через jQuerry item-ах, нужно обращаться через document.
    $(document).on('click', '.dropdown-item', function () {
        var curr_id = $(this).attr('id');
        block_ui();
        Swal.fire({
            title: "Информация о машине",
            text: JSON.stringify(current_cars[curr_id]),
            icon: "info"
        });
        $('.dropdown-toggle').html($(this).html());
    });

});

// single role functions

function block_ui() {
    // $.blockUI.defaults.message = '<h1>Пожалуйста, подождите</h1>';
    $.blockUI.defaults.message = '<i class="fa fa-cog fa-spin fa-fw" style="font-size:128px"></i>' +
        '<p style="font-size: 24px">Пожалуйста, подождите</p>';
    $.blockUI.defaults.overlayCSS = {backgroundColor: '#fff', opacity: 0.8, cursor: 'wait'};
    // $.blockUI.defaults.css = {border: 0, padding: 0, backgroundColor: 'transparent'};
    $.blockUI.defaults.baseZ = 5000;

    $(document).ajaxStart($.blockUI).ajaxStop($.unblockUI);
}

function write_car_list_text() {
    car_cnt = $('#dropmenu').children('.dropdown-item').length;
    if (car_cnt > 0) {
        $('.dropdown-toggle').text('список авто(' + car_cnt + ')');
    } else {
        $('.dropdown-toggle').text('список авто(пусто)')
    }
}


function custom_swal_animate() {
    swal.fire({
        icon: 'info',
        title: "все Тачки удалены! ",
        showClass: {
            popup: 'animated fadeInDown faster',
            icon: 'animated heartBeat delay-1s'
        },
        hideClass: {
            popup: 'animated fadeOutUp faster',
        }
    })
}


function success_adding(data) {

    var car = data['cars'][0];
    var car_id = $(data['cars'][0]).attr('id')

    var swal_item = data['swal_items'][0];
    // globals
    // current_cars[car_id] = data['cars_info'];
    current_cars[car_id] = data['cars_info'][car_id];

    $('#dropmenu').append(car);

    swal.fire({
        title: "Успешно",
        text: "Тачка создана!",
        html: swal_item,
        icon: "success",
        confirmButtonText: "в гараж!",

        showClass: {
            popup: 'animated fadeInDown faster',
            icon: 'animated heartBeat delay-1s'
        },
        hideClass: {
            popup: 'animated fadeOutRight faster',
        }


    });

    write_car_list_text();
}

function error_adding(data) {
    swal.fire({
        title: "Ошибка",
        text: "Ошибочная тачка...",
        icon: "error"
    });
}

//showing all car in garage
function show_garage() {
    jQuery.ajax({
        url: $.show_garage_url,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            var $garage = $('.garage');
            // garage.data('material_id', material_id);
            $garage.html(data.car_table);
            $garage.dialog({
                title: 'Garage',
                width: 900,
                height: 600,
                show: 1000
            });
        },
        error: function (data) {
        },
        // data: {'table': car_table}
    });
}


