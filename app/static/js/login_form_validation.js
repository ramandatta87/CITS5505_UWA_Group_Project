// file: static/js/login_form_validation.js
function validateForm() {
    var email = document.forms["login"]["email"].value;
    var password = document.forms["login"]["password"].value;
    if (email === "" || password === "") {
        alert("Both email and password must be filled out");
        return false;
    }
    return true;
}
