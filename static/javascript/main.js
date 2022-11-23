console.log("Hello?");

function hello() {
    window.alert("Hello!");
}

function uploadFile() {
    $.ajax({
        url: "/uploadFile",
        type: "GET",
        success: function (response) {
            $("#status").html(response.status);
            generateFingerprint();
        },
        error: function (error) {
            window.alert(`Error ${error}`);
        }
    });
}

function generateFingerprint() {
    $.ajax({
        url: "/generateFingerprint",
        type: "GET",
        success: function (response) {
            $("#status").html(response.status);
            searchDatabase();
        },
        error: function (error) {
            window.alert(`Error ${error}`);
        }
    });
}

function searchDatabase() {
    $.ajax({
        url: "/searchDatabase",
        type: "GET",
        success: function (response) {
            $("#status").html(response.status);
        },
        error: function (error) {
            window.alert(`Error ${error}`);
        }
    });
}