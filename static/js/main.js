$(document).ready(function () {
    // Dynamic year in footer copyrights
    $('#curr_year').text(new Date().getFullYear());

    // Common ajax success handler
    function request_response(response) {
        if (response.success) { window.location.reload(); }
        else {
            $("#RegModalFormError").text(response.error_message);
        }
    }
	
	// Login / Register
    $("#RegModalForm").submit(function (e) {
        e.preventDefault();
        var form_data = $(this).serialize();
        $.post("/login/", form_data, request_response)
        .fail(function (xhr, status, error) { console.log(error); });
    });
	
    // Edit profile info
    $("#LkFormEditButton").click(function(e) {
        e.preventDefault();
        $("#LkFormNameField").prop("readonly", false);
        $("#LkFormPhoneField").prop("readonly", false);
        $("#LkFormEmailField").prop("readonly", false);
        $("#LkFormEditButton").hide();
        $("#LkFormSubmitButton").show();
    });
    $("#LkProfileForm").submit(function (e) {
        e.preventDefault();
        var form_data = $(this).serialize();
        $.post("/lk/", form_data, request_response)
        .fail(function (xhr, status, error) { console.log(error); });
    });
});