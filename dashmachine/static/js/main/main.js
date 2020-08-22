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
                var elems = grid.isotope('getItemElements');
                grid.isotope("remove", elems);
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
    container.next('.progress').removeClass('hide');
    $.ajax({
        url: loadDataSourceUrl,
        type: 'GET',
        data: {ds: data_source_name},
        success: function(data){
            container.html(data)
            container.removeClass('hide');
            container.next('.progress').addClass('hide');
            container.closest('.collection').find(".reload-data-source").on('click', function(e) {
                loadDataSource(data_source_name, container);
            });
        }
    });
}

function openIframe(url){
    $("#iframe-viewer-iframe").attr("src", url);
    $(".iframe-open-in-new").attr("href", url);
    $(".iframe-viewer-title").text(url);
    $("#iframe-viewer").modal('open');
    $(".iframe-close").off('click');
    $(".iframe-close").on('click', function (){
        $("#iframe-viewer").modal('close');
        $("#iframe-minimized").addClass('hide');
    });
    $(".iframe-min").off('click');
    $(".iframe-min").on('click', function (){
        $("#iframe-viewer").modal('close');
        $("#iframe-minimized").removeClass('hide');
    });
    $(".iframe-restore").off('click');
    $(".iframe-restore").on('click', function (){
        $("#iframe-viewer").modal('open');
        $("#iframe-minimized").addClass('hide');
    });
}

function changeDashboard(name, grid){
    dashboardName = name;
    loadGrid($("#grid"));
}

function showLogs(){
    $.ajax({
        url: getLogsUrl,
        type: 'GET',
        success: function(data){
            $("#logs-modal-content").html(data);
            $("#logs-modal").modal('open');
            var d = $('#logs-modal-content-col');
            d.scrollTop(d.prop("scrollHeight"));
        }
    });
}

function historyPush(query_str, value){
    if (value.length > 0){
        let query_params = location.search;
        if (query_params.startsWith('?tag') && query_str === "dashboard") {
            query_params = "";
        }
        let base_url = window.location.pathname
        let full_location = base_url+query_params;
        let full_query_param = query_str + '='

        if (query_params.indexOf(full_query_param) > -1){
            let val_start = full_location.indexOf(query_str + '=') + full_query_param.length
            let val_end = full_location.indexOf('&', val_start)
            if (val_end === -1){val_end = full_location.length}
            let new_location = full_location.substring(0, val_start) + value + full_location.substring(val_end, full_location.length);
            history.pushState(
                null, '',
                new_location
            );
        }
        else if (query_params.length < 1){
            history.pushState(
                null, '',
                `${base_url}?${query_str}=${value}`
            );
        } else {
            history.pushState(
                null, '',
                `${full_location}&${query_str}=${value}`
            );
        }
    }
}
function applyTagFilter(tag){
    $("#grid").isotope({
        filter: function (){
            var tags = $(this).attr('data-tags').split("%,%");
            return tags.includes(tag);
        }
    })
}

$(function(){

    $("#error-message-modal").modal({
        dismissible: false,
    });

    $("#logs-modal").modal();

    $("#iframe-viewer").modal();

    var $grid = $("#grid").isotope({
        itemSelector: '.grid-item',
        layoutMode: 'packery',
        packery: {
            gutter: 10
        }
    });

    loadGrid($grid);
    $(window).on('resize', function(e) {
        sleep(1000).then(() => {
            $grid.isotope();
        });
    });

    if (dashboardTag !== "None"){
        console.log(dashboardTag)
        applyTagFilter(dashboardTag);
    }

    function clear_card_filter(card_filter){
        card_filter.val('');
        card_filter.autocomplete("destroy");
    }
    function card_filter_submit(card_filter){
        if (card_filter.val().startsWith('?') && card_filter.val().length > 3) {
            let prefix = card_filter.val().slice(1, card_filter.val().indexOf(' '));
            let query_str = card_filter.val().slice(card_filter.val().indexOf(' ') + 1).replace(" ", "+");
            let url = queryProviderUrls[prefix];
            $(location).attr('href', url + query_str)
        } else if (card_filter.val().startsWith(":l")){
            showLogs();
            clear_card_filter(card_filter);
        }
        else if (card_filter.val().startsWith(":d") && card_filter.val().length > 3){
            historyPush('dashboard', card_filter.val().slice(3));
            changeDashboard(card_filter.val().slice(3));
            clear_card_filter(card_filter);
        } else if (card_filter.val().startsWith(":t") && card_filter.val().length > 3){
            historyPush('tag', card_filter.val().slice(3));
            applyTagFilter(card_filter.val().slice(3));
            clear_card_filter(card_filter);
        } else if (card_filter.val().startsWith(":e")){
            openIframe("https://code.wolf-house.net");
            clear_card_filter(card_filter);
        }
    }
    let card_filter = $("#card-filter");
    card_filter.on('keydown', function(i, e) {
        if (i.key === ":"){
            card_filter.autocomplete({
                data: {
                    ":dashboard": null,
                    ":editor": null,
                    ":logs": null,
                    ":tag": null
                },
                onAutocomplete: function (){
                    card_filter.val(card_filter.val().slice(0,2) + " ");
                    card_filter_submit(card_filter);
                }
            });
        } else if (i.key == "?"){
            card_filter.autocomplete({
                data: autocompleteQueryProviders,
                onAutocomplete: function (){
                    card_filter.val(card_filter.val().slice(0,2) + " ");
                }
            });
        } else if (i.key === "Enter") {
            card_filter_submit(card_filter);
        }
    });
    card_filter.on('keyup', function (i, e){
        if (["ArrowDown", "ArrowUp", "ArrowRight", "ArrowLeft"].includes(i.key)){}
        else if (card_filter.val().trimRight()  === ":d"){
            card_filter.autocomplete({
                data: autocompleteDashboards,
                onAutocomplete: function (){
                    card_filter_submit(card_filter);
                }
            });
            card_filter.autocomplete('open')
        } else if (card_filter.val().trimRight()  === ":t"){
            card_filter.autocomplete({
                data: autocompleteTags,
                onAutocomplete: function (){
                    card_filter_submit(card_filter);
                }
            });
            card_filter.autocomplete('open')
        } else if (!card_filter.val().startsWith(":")
            && !card_filter.val().startsWith("?")
            && card_filter.val().length > 0) {
            $grid.isotope({
                filter: function () {
                    return $(this).attr('data-searchable').trimRight()
                        .toLowerCase().indexOf(card_filter.val().toLowerCase()) > -1;
                }
            });
        } else if (i.key === "Enter"){} else {
            $grid.isotope({ filter: '*' })
        }
    });
});