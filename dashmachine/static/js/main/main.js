async function appendToGrid(grid, data){
    let elems = $(data);
    grid.append(elems).isotope( 'insert', elems);
    $(".data-source-container").each(function() {
        loadDataSource($(this).attr('data-source'), $(this));
    })
    return elems;
}

function loadGrid(grid){
    $.ajax({
        url: loadGridUrl,
        type: 'GET',
        data: {dashboard: dashboardName},
        success: function(data){
            if (data.data){
                // error messages
                $("#error-message-title").html(data.data.error_title);
                $("#error-message-content").html(data.data.error);
                $("#error-message-modal").modal('open');
            } else {
                appendToGrid(grid, data).then(() => {
                    sleep(100).then(() => {
                        grid.isotope('layout');
                    });
                });
            }
        }
    });
}

function loadDataSource(data_source_name, container){
    $.ajax({
        url: loadDataSourceUrl,
        type: 'GET',
        data: {ds: data_source_name},
        success: function(data){
            container.append(data)
            container.removeClass('hide');
            container.next('.progress').addClass('hide');
        }
    });
}

$(function(){
    // history.pushState(null, '', `${window.location.pathname}?tag=test`)
    $("#error-message-modal").modal({
        dismissible: false,
    });

    var $grid = $("#grid").isotope({
        itemSelector: '.grid-item',
        layoutMode: 'masonry',
    });

    loadGrid($grid);
    $(window).on('resize', function(e) {
        sleep(1000).then(() => {
            $grid.isotope();
        });
    });
});