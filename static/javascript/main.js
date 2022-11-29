console.log("Hello?");

function hello() {
    window.alert("Hello!");
}

function uploadFile() {
    $("#status").html("Generating Fingerprint...");
    const file = $("#file")[0].files[0];
    data = new FormData();
    data.append("sample", file);
    

    $.ajax({
        url: "/generateFingerprint",
        type: "POST",
        data: data,
        contentType: false,
        processData: false,
        success: function () {
            $("#status").html("");
            searchDatabase();
        },
        error: function (error) {
            window.alert(`Error ${error}`);
        }
    });
}

function searchDatabase() {
    $("#status").html("Searching for matches...");
    $.ajax({
        url: "/searchDatabase",
        type: "GET",
        success: function (response) {
            $("#status").html(response.result);
        },
        error: function (error) {
            window.alert(`Error ${error}`);
        }
    });
}