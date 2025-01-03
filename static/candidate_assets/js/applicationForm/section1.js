
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
            title: 'Invalid Langauge Detected',
            text: 'Please enter the Topic of Ph.D in English only. If the topic is in Marathi, Please translate and then enter the text.'
        });
        $(this).val('')
        input.value = input.value.replace(/[^A-Za-z0-9.,'"\s\-()]/g, ''); // Remove invalid characters
    }
}
// -------------------------------------------------------

// --------- Mobile Number on on Section 1 -------------------
function validateMobileNumber(input) {
    // Remove any non-numeric characters
    input.value = input.value.replace(/[^0-9]/g, '');

    // Limit the input to 10 digits
    if (input.value.length > 10) {
        input.value = input.value.slice(0, 10);
    }
    // Check if the first digit is 7, 8, or 9
    if (input.value.length > 0 && !/^[789]/.test(input.value)) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Number Detected',
            text: 'Mobile Number should not start with any other digit than 7, 8 or 9.'
        });
        input.value = ''; // Clear the input if invalid
    }
}
// -------------------------------------------------------


// --------- Aadhaar Number Validation Section -------------------
function checkAadhaarOnChange(input) {
    // Remove any non-numeric characters
    input.value = input.value.replace(/[^0-9]/g, '');

    // Limit the input to exactly 12 digits
    if (input.value.length > 12) {
        input.value = input.value.slice(0, 12);
    }

    // Check if the number is exactly 12 digits and does not start with 0 or 1
    if (input.value.length === 12 && /^[01]/.test(input.value)) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Number Detected',
            text: 'Please enter valid Adhaar Number. Adhaar Number cannot start with 0, 1 or 2.'
        });
        input.value = ''; // Clear the input if invalid
    }

    if (input.value.length !== 12) {
        Swal.fire({
            icon: 'info',
            title: 'Invalid Number Detected',
            text: 'Please enter valid Adhaar Number. Adhaar Number has to be 12 digits without spaces.'
        });
        input.focus(); // Focus back on the input field
    }

     // Check if all digits are identical
    if (/^(\d)\1{11}$/.test(input.value)) {
        Swal.fire({
            icon: 'info',
            title: 'Invalid Number Detected',
            text: 'Aadhaar number cannot have all identical digits.'
        });
        input.value = ''; // Clear the input if all digits are identical
        input.focus(); // Refocus on the input
    }
}
// -------------------------------------------------------


// --------- Age Count Dynamic on Change of Date of Birth on on Section 1 -------------------
window.onload = function() {
    // Get today's date
    const today = new Date();

    // Format the date as YYYY-MM-DD (required format for <input type="date">)
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    const todayDate = yyyy + '-' + mm + '-' + dd;

    // Set the max attribute of the date input field to today's date
    document.getElementById('date_of_birth').setAttribute('max', todayDate);
}

function calculateAge(input) {
    const dobInput = input.value; // Get the value from the input field
    const ageField = document.getElementById('age'); // The field where age is displayed

    // Ensure the input has a complete date in the format YYYY-MM-DD
    if (!dobInput || dobInput.length < 10) {
        return; // Exit the function if the date is incomplete
    }

    // Validate the entered date
    const enteredDate = new Date(dobInput);
    if (isNaN(enteredDate.getTime())) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Date Format',
            text: 'Please enter a valid date in the format YYYY-MM-DD.'
        });
        input.value = ''; // Clear the input if the date is invalid
        ageField.value = ''; // Clear the age field
        return; // Exit the function
    }

    // Check if the entered date is not in the future
    const today = new Date();
    if (enteredDate > today) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Date',
            text: 'Date cannot be greater than today\'s date.'
        });
        input.value = ''; // Clear the input if the date is invalid
        ageField.value = ''; // Clear the age field
        return; // Exit the function
    }

    // Calculate the age
    let age = today.getFullYear() - enteredDate.getFullYear();
    const monthDifference = today.getMonth() - enteredDate.getMonth();

    // Adjust age if the current date is before the birth date in the current year
    if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < enteredDate.getDate())) {
        age--;
    }

    // Check age criteria
    if (age > 42) {
        Swal.fire({
            icon: 'error',
            title: 'Age Criteria Not Met',
            text: 'Age allowed for getting the fellowship is 42. Unfortunately, you do not match the criteria.'
        });
        input.value = ''; // Clear the input if the age is invalid
        ageField.value = ''; // Clear the age field
        return; // Exit the function
    }

    if (age < 15) {
        Swal.fire({
            icon: 'error',
            title: 'Age Criteria Not Met',
            text: 'Unfortunately, you do not match the criteria.'
        });
        input.value = ''; // Clear the input if the age is invalid
        ageField.value = ''; // Clear the age field
        return; // Exit the function
    }

    ageField.value = age; // Display the calculated age
}


// -------------------------------------------------------

// Initialize all tooltips
// ------------------ Tooltip to show the instructions --------------
// Initialize all tooltips
document.addEventListener('DOMContentLoaded', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
// ----------------------------------------------------------------


// Show/Hide Additional Field
// ---------------- Show and Hide Field on d-none ----------------------------
// This function is for PVTG Caste
function toggleAdditionalField(select) {
    const additionalField = document.getElementById('additionalField');
    const inputField = document.getElementById('pvtg_caste');

    if (select.value === 'Yes') {
        additionalField.classList.remove('d-none'); // Show field
    } else {
        additionalField.classList.add('d-none'); // Hide field
        inputField.value = ''; // Clear input field
    }
}
// ---------------- END Show and Hide Field on d-none ----------------------------

// ---------------- To show Subcastes on Caste ----------------------------
// This function is for Sub Caste
$('#caste').on('change', function () {
    let values = $('option:selected', this).attr('data-hidden')
    let value_array = values.split(',')
    $('#subcaste').empty()
    $('#subcaste').append('<option>-- Select Sub Caste / Tribe --</option>')
    value_array.forEach(function (item) {
        $('#subcaste').append(`<option value="${item}">${item}</option`);
    });
})
// ---------------- END Subcastes on Caste ----------------------------


// ---------------- To Pincode and Village Autopopulate ----------------------------
// This function is for Sub Caste
$('#pincode').on('blur', function () {
    $('#village').empty()
    $('#village').append(`<option value = '' class = 'spinner-border' role="status">
    <span class="sr-only">Loading...</span> </option>`)
    let pincode = $(this).val();
    if ($(this).val() == '' || $(this).val().length < 6) {
        Swal.fire({
            title: "Wrong Pincode",
            text: "Please Enter 6 digits Pincode",
            icon: "info"
        });
        return
    }
    if (pincode[0] == 0) {
        Swal.fire({
            title: "Wrong Pincode",
            text: "Enter Correct piconde",
            icon: "info"
        });
        $(this).val('')
        return
    }

    $.ajax({
        url: "/get_pincode_data",
        type: "GET",
        data: { 'pincode': pincode },
        success: function (html) {
            $('#village').empty()
            if (html.Message == 'No records found') {
                Swal.fire({
                    title: "Wrong Pincode",
                    text: "Please Enter Correct Pincode",
                    icon: "info"
                });
            } else {

                let PostOffice = html.result
                $('#village').append(`<option value = ''> -- Select Village -- </option>`)
                $(PostOffice).each(function (index, post_val) {
                    $('#village').append(`<option value = '${post_val.postalLocation}' data-hidden = '${post_val.id}'>${post_val.postalLocation}</option>`)
                })
            }
        },
        error: function (jqxhr, textStatus, error) {
        }
    });
});

// On change of village get all village data
$('#village').on('change', function () {
    village_name = $('option:selected', this).attr('data-hidden');
    pincode = $('#pincode').val()


    $.ajax({
        url: "/get_pincode_data",
        type: "GET",
        data: { 'pincode': pincode },
        success: function (html) {
            if (html.Message == 'No records found') {
                Swal.fire({
                    title: "Wrong Pincode",
                    text: "Please Enter Correct Pincode",
                    icon: "info"
                });
            } else {

                let PostOffice = html.result
                $(PostOffice).each(function (index, post_val) {
                    if (post_val.id == village_name) {
                        $('#taluka').val(post_val.province)
                        $('#city').val(post_val.district)
                        $('#district').val(post_val.district)
                        $('#state').val(post_val.state)
                    }
                })
            }
        },
        error: function (jqxhr, textStatus, error) {
        }
    })
})
// -------------------- END Pincode and Village Autopopulate --------------


// -------------------- Auto populate communciation address on Tick --------------
document.getElementById('flexCheckIndeterminate').addEventListener('change', function () {
    // Permanent Address Fields
    const permanentAddress = document.getElementById('add_1');
    const permanentPincode = document.getElementById('pincode');
    const permanentVillage = document.getElementById('village');
    const permanentTaluka = document.getElementById('taluka');
    const permanentDistrict = document.getElementById('district');
    const permanentState = document.getElementById('state');

    // Communication Address Fields
    const communicationAddress = document.getElementById('comm_add_1');
    const communicationPincode = document.getElementById('comm_pincode');
    const communicationVillage = document.getElementById('comm_village');
    const communicationTaluka = document.getElementById('comm_taluka');
    const communicationDistrict = document.getElementById('comm_district');
    const communicationState = document.getElementById('comm_state');

    if (this.checked) {
        // Copy values from Permanent to Communication Address
        communicationAddress.value = permanentAddress.value;
        communicationPincode.value = permanentPincode.value;
        // Set the selected value of Communication Village using jQuery
        communicationVillage.options[communicationVillage.selectedIndex].text = permanentVillage.options[permanentVillage.selectedIndex].text;
        communicationTaluka.value = permanentTaluka.value;
        communicationDistrict.value = permanentDistrict.value;
        communicationState.value = permanentState.value;

        // Disable Communication Address Fields
        communicationAddress.readOnly = true;
        communicationPincode.readOnly = true;
        communicationVillage.readOnly = true;
        communicationTaluka.readOnly = true;
        communicationDistrict.readOnly = true;
        communicationState.readOnly = true;
    } else {
        // Clear and Enable Communication Address Fields
        communicationAddress.value = '';
        communicationPincode.value = '';
        communicationVillage.options[communicationVillage.selectedIndex].text = '';
        communicationTaluka.value = '';
        communicationDistrict.value = '';
        communicationState.value = '';

        communicationAddress.readOnly = true;
        communicationPincode.readOnly = true;
        communicationVillage.readOnly = true;
        communicationTaluka.readOnly = true;
        communicationDistrict.readOnly = true;
        communicationState.readOnly = true;
    }
});

// Optional: Real-time synchronization when Permanent Address fields change
document.getElementById('add_1').addEventListener('input', function () {
    const addressCheckbox = document.getElementById('flexCheckIndeterminate');
    const communicationAddress = document.getElementById('comm_add_1');
    if (addressCheckbox.checked) {
        communicationAddress.value = this.value;
    }
});

// Repeat real-time synchronization for all relevant fields (if needed)
document.getElementById('pincode').addEventListener('input', function () {
    const addressCheckbox = document.getElementById('flexCheckIndeterminate');
    const communicationPincode = document.getElementById('comm_pincode');
    if (addressCheckbox.checked) {
        communicationPincode.value = this.value;
    }
});

// Real-time synchronization for dropdown (Permanent Village)
document.getElementById('village').addEventListener('change', function () {
    const addressCheckbox = document.getElementById('flexCheckIndeterminate');
    const communicationVillage = document.getElementById('comm_village');
    if (addressCheckbox.checked) {
        communicationVillage.value = this.value; // Synchronize selected value
    }
});
// -------------------- END Auto populate communciation address on Tick --------------


// -------------------- Populate the Subcaste on Selected Caste --------------
/*
    This is the logic of rendering subcaste on caste.
    Route call will be found in: /PythonFiles/CandidatePages/ApplicationForm/section1.py
    Caste logic is in: /Classes/caste.py
*/
document.getElementById("caste").addEventListener("change", function () {
    const selectedOption = this.options[this.selectedIndex];
    const uniqueNumber = selectedOption.getAttribute("data-hidden");
    const subcasteDropdown = document.getElementById("subcaste");

    // Clear the subcaste dropdown
    subcasteDropdown.innerHTML = '<option value="" selected>-- Select Subcaste --</option>';

    if (uniqueNumber) {
        // Fetch subcastes for the selected unique number
        fetch(`/get_subcastes/${uniqueNumber}`)
            .then(response => response.json())
            .then(data => {
                if (data.subcastes && data.subcastes.length > 0) {
                    data.subcastes.forEach(subcaste => {
                        const option = document.createElement("option");
                        option.value = subcaste;
                        option.textContent = subcaste;
                        subcasteDropdown.appendChild(option);
                    });
                }
            })
            .catch(error => console.error('Error fetching subcastes:', error));
    }
});
// -------------------- END Populate the Subcaste on Selected Caste -------------


function showAlert() {
    Swal.fire({
        icon: 'warning',
        title: 'Incomplete Sections',
        text: 'Please complete the current section before proceeding to the next.',
        confirmButtonText: 'OK'
    });
}

// Function to enable or disable the submit button
function enableDisabledFields() {
    const checkbox1 = document.getElementById("verifyDetails");
    const checkbox2 = document.getElementById("verifyDetailsHindi");
    const submitBtn = document.getElementById("submit");

    // Enable the button if both checkboxes are checked
    if (checkbox1.checked && checkbox2.checked) {
        submitBtn.disabled = false;
    } else {
        submitBtn.disabled = true;
    }
}

// Initialize event listeners
window.onload = function() {
    // Add event listeners for checkbox change events
    document.getElementById("verifyDetails").addEventListener('change', enableDisabledFields);
    document.getElementById("verifyDetailsHindi").addEventListener('change', enableDisabledFields);

    // Call function initially to check if the button should be enabled or not
    enableDisabledFields();
};