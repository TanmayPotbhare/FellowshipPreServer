// --------- All names on on Section 1 -------------------
function validateName(input) {
    // Replace anything that is not a letter or space
    input.value = input.value.replace(/[^a-zA-Z\s]/g, '');

    // Ensure the first letter is capitalized and the rest are lowercase
    input.value = input.value
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ');

    const englishOnlyPattern = /^[A-Za-z0-9.,'"\s\-()]*$/;

    if (!englishOnlyPattern.test(input.value)) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Langauge Detected!',
            text: 'Please enter the Topic of Ph.D in English only. If the topic is in Marathi, Please translate and then enter the text.'
        });
        $(this).val('')
        input.value = input.value.replace(/[^A-Za-z0-9.,'"\s\-()]/g, ''); // Remove invalid characters
    }
}
// -------------------------------------------------------

// --------- Mobile Number on Section 1 -------------------
function validateMobileNumber(input) {
    // Remove any non-numeric characters
    input.value = input.value.replace(/[^0-9]/g, '');

    // Allow integers only upto 10 digits
    if (input.value.length > 10) {
        input.value = input.value.slice(0, 10);
    }
    // Mobile Number should start with 7, 8, or 9.
    if (input.value.length === 10) {
        if (!/^[789]/.test(input.value)) {
            alert("number")
            Swal.fire({
                icon: 'error',
                title: 'Invalid Number Detected!',
                text: 'Mobile Number should start with 7, 8, or 9.'
            });
            input.value = ''; 
        }
    } else if (input.value.length > 0 && input.value.length < 10) {
        // If digits are less than 10
        Swal.fire({
            icon: 'error',
            title: 'Incomplete Number!',
            text: 'Mobile Number must be exactly 10 digits.'
        });
        input.value = ''; 
    }
}
// -------------------------------------------------------


// For Validating Password and Confirm Password in Sign_up Form  
function validatePasswords() {
    const password = $('#password').val();
    const confirmPassword = $('#confirm_password').val();

    // Updated Regex for password validation
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$/;

    // Stage 1: Check password complexity
    if (password && !passwordRegex.test(password)) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Password!',
            text: 'Password must have 8-20 characters, including at least one uppercase letter, one lowercase letter, one number, and one special character.',
        });
        $('#password').val('');
        $('#confirm_password').val('');
        return false;  // Stop execution if password is invalid
    }

    // Stage 2: Check if passwords match
    if (password && confirmPassword && password !== confirmPassword) {
        Swal.fire({
            icon: 'error',
            title: 'Password Mismatch!',
            text: 'Password and Confirm Password do not match.',
        });
        $('#confirm_password').val('');  // Clear the confirm password field
        return false;  // Stop execution if passwords do not match
    }

    return true;  // Both password and confirm password are valid and match
}


