$(function () {
    $("#hostAdd").click(function () {
        var name = $("#hostName").val();
        var url = $("#hostUrl").val();
        var data = {name:name, url:url}
        $.ajax("/host",
        {
            type: "POST",
            data: JSON.stringify(data),
            contentType: 'application/json',
            processData: false
        }).fail(function (e) {
            spawnHttpErrorModal(e)
        });
    });

    $("#hostRm").click(function () {
        var name = $("#hostName").val();
        $.ajax("/host/" + name, {type: "DELETE"}).fail(function (e) {
            spawnHttpErrorModal(e)
        });
    });


    function spawnHttpErrorModal(e) {
        $("#errorModal .modal-title").html(e.status);
        $("#errorModal .modal-body p").html(e.statusText + "</br>" + e.responseText);
        if ($('#errorModal').is(':hidden')) {
            $("#errorModal").modal('show')
        }
    }

    function spawnErrorModal(errorTitle, errorText) {
        $("#errorModal .modal-title").html(errorTitle);
        $("#errorModal .modal-body p").html(errorText);
        if ($('#errorModal').is(':hidden')) {
            $("#errorModal").modal('show')
        }
    }
})