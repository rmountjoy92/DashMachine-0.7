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

$(function(){

    $("#error-message-modal").modal({
        dismissible: false,
    });

    $("#iframe-viewer").modal();

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

    function clear_card_filter(card_filter){
        card_filter.val('');
        card_filter.autocomplete("destroy");
    }
    function historyPush(query_str, value){
        // if (location.search.indexOf(`?${query_str}=`) === -1){
        //     history.pushState(
        //         null, '',
        //         `${window.location.pathname+location.search}?${query_str}=${value}`
        //     );
        // }
    }
    function card_filter_submit(card_filter){
        if (card_filter.val().startsWith('?') && card_filter.val().length > 3) {
            let prefix = card_filter.val().slice(1, card_filter.val().indexOf(' '));
            let query_str = card_filter.val().slice(card_filter.val().indexOf(' ') + 1).replace(" ", "+");
            let url = queryProviderUrls[prefix];
            $(location).attr('href', url + query_str)
        }
        else if (card_filter.val().startsWith(":d") && card_filter.val().length > 3){
            changeDashboard(card_filter.val().slice(3));
            clear_card_filter(card_filter);
        } else if (card_filter.val().startsWith(":t") && card_filter.val().length > 3){
            historyPush('tag', card_filter.val().slice(3));
            $("#grid").isotope({
                filter: function (){
                    var tags = $(this).attr('data-tags').split("%,%");
                    return tags.includes(card_filter.val().slice(3));
                }
            })
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