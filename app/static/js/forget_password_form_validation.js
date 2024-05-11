document.addEventListener("DOMContentLoaded", function () {
    const forgetPasswordForm = document.forms['forget_password'];
    forgetPasswordForm.addEventListener('submit', function (event) {
        let isValid = true;
        const formData = new FormData(forgetPasswordForm);

        // List of fields to validate
        const first_name = formData.get('first_name');
        const uwa_id = formData.get('uwa_id');
        const email = formData.get('email');
        const new_password = formData.get('new_password');
        const confirm_new_password = formData.get('confirm_new_password');

        // Validation for First Name
        if (!first_name.trim()) {
            alert('First Name is required.');
            isValid = false;
        }

        // Validation for UWA ID
        if (!uwa_id.trim()) {
            alert('UWA ID is required.');
            isValid = false;
        }

        // Validation for Email
        if (!email.trim()) {
            alert('Email is required.');
            isValid = false;
        } else if (!email.includes('@')) {
            alert('Please enter a valid email address.');
            isValid = false;
        }

        // Validation for New Password
        if (!new_password) {
            alert('New Password is required.');
            isValid = false;
        } else if (new_password.length < 6) {
            alert('Your password must be at least 6 characters long.');
            isValid = false;
        }

        // Validation for Confirm New Password
        if (new_password !== confirm_new_password) {
            alert('The new passwords do not match.');
            isValid = false;
        }

        if (!isValid) {
            event.preventDefault(); // Prevent form submission if validation fails
        }
    });
});
