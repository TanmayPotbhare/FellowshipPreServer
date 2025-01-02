// ------------- Year Validation --------------
// ------- Start --------
function validateYear(input) {
    const currentYear = new Date().getFullYear();

    // Remove any non-numeric characters
    input.value = input.value.replace(/[^0-9]/g, '');

    // Limit the input to 4 digits
    if (input.value.length > 4) {
        input.value = input.value.slice(0, 4);
    }

    // Validate against the current year
    if (input.value.length === 4 && input.value > currentYear) {
        Swal.fire({
            icon: "error",
            title: "Invalid Input!",
            text: `Passing Year cannot be greater than the Current Year.`,
        });

        input.value = '';
    }
}
// ------------------------------------------------

// ---------- For Auto populating the Day Month and Year on PHD Registration Date ----------
document.getElementById('phd_registration_date').addEventListener('change', function () {
    const dateInput = this.value;
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();

    if (dateInput) {
        const selectedDate = new Date(dateInput);

        // Check if the selected year exceeds the current year
        if (selectedDate.getFullYear() > currentYear) {
            Swal.fire({
                icon: "error",
                title: "Invalid Input!",
                text: `Passing Year cannot be greater than the Current Year.`,
            });
            this.value = ''; // Clear the input field
            // Clear dependent fields
            document.getElementById('phd_registration_day').value = '';
            document.getElementById('phd_registration_month').value = '';
            document.getElementById('phd_registration_year').value = '';
            return;
        }2

        // Extract day, month, and year
        const day = selectedDate.getDate();
        const month = selectedDate.toLocaleString('default', { month: 'long' }); // Get full month name
        const year = selectedDate.getFullYear();

        // Calculate age in years
        let age = currentYear - year;
        if (
            currentDate.getMonth() < selectedDate.getMonth() ||
            (currentDate.getMonth() === selectedDate.getMonth() && currentDate.getDate() < day)
        ) {
            age--; // Adjust age if the birth date hasn't occurred yet this year
        }

        // Populate fields
        document.getElementById('phd_registration_day').value = day;
        document.getElementById('phd_registration_month').value = month;
        document.getElementById('phd_registration_year').value = year;
    } else {
        // Clear all fields if no date is selected
        document.getElementById('phd_registration_day').value = '';
        document.getElementById('phd_registration_month').value = '';
        document.getElementById('phd_registration_year').value = '';
    }
});
// --------------------------------------------------------


// ---------------- Show and Hide Field on d-none ----------------------------
// This function is for PVTG Caste
function toggleAdditionalFieldFaculty(select) {
    const additionallField = document.getElementById('additionalField');
    const inputtField = document.getElementById('other_faculty');

    if (select.value === 'Other') {
        additionallField.classList.remove('d-none'); // Show field
    } else {
        additionalField.classList.add('d-none'); // Hide field
        inputtField.value = ''; // Clear input field
    }
}
// ----------------------------------------------------------------


// ---------------- Show and Hide Field on d-none ----------------------------
// This function is for College toggle
function toggleCollegeField(select) {
    const additionalField = document.getElementById('collegeField');
    const inputField = document.getElementById('other_name_of_college');

    if (select.value === 'Other') {
        additionalField.classList.remove('d-none'); // Show field
    } else {
        additionalField.classList.add('d-none'); // Hide field
        inputField.value = ''; // Clear input field
    }
}
// ----------------------------------------------------------------

// --------------------------- University Populate college names ---------------------
$('#concerned_university').on('change', function () {
    let university_id = $('option:selected', this).attr('data-hidden')
    $('#name_of_college').empty()
    $('#name_of_college').append('<option>Loading ....</option>')
    $.ajax({
        url: '/get_college_data_by_university',
        method: 'POST',
        data: { 'u_id': university_id },
        success: function (html) {
            $('#name_of_college').empty()
            $('#name_of_college').append('<option>-- Select College --</option>')
            $('#name_of_college').append('<option value="Other">Other</option>')
            html.forEach(function (item) {

                $('#name_of_college').append(`<option value="${item.college_name}">${item.college_name}</option`);

            });
        },
        error: function () {
            Swal.fire({
                icon: "error",
                title: "Please Try Agian...",
                text: `Please Select Correct University`,
            });
        }
    })
})
// 0-----------------------------------------------------------------

// --------------------- Calculate Age on Phd Registration Year ----------------------
function calculateAges() {
    // Get the hidden DOB year (e.g., (1996,))
    const dobYear = document.getElementById('dob_year').value.replace(/[^\d]/g, ''); // Strip non-numeric characters
    alert(dobYear);
    // Get the Ph.D. registration date entered by the user
    const phdRegDate = document.getElementById('phd_registration_date').value;

    if (phdRegDate) {
        // Convert Ph.D. registration date to Date object
        const phdDate = new Date(phdRegDate);

        // Get the Ph.D. registration year
        const phdYear = phdDate.getFullYear();

        // Calculate age
        let age = phdYear - dobYear;

        // Assuming the birth month and day are Jan 1st, adjust age if the Ph.D. registration date is before the birthday in that year
        const dobMonthDay = new Date(dobYear, 0, 1); // Jan 1st as an example
        if (phdDate < dobMonthDay) {
            age -= 1; // Subtract 1 if the Ph.D. registration date is before the birthday in that year
        }

        // Display the calculated age in the "Age at Ph.D Registration" input field
        document.getElementById('phd_registration_age').value = age;
    } else {
        // Clear the age field if the registration date is not selected
        document.getElementById('phd_registration_age').value = '';
    }
}
// ----------------------------------------------------------------

// ------------- Validate Number of Attempts --------------
// ------- Start --------
function validateAttempts(input) {
    // Remove any non-numeric characters
    input.value = input.value.replace(/[^0-9]/g, '');

        // Limit the input to 2 digits
        if (input.value.length > 2) {
            input.value = input.value.slice(0, 2);
        }     

        if (input.value === '0') {
            input.value = '';
        }  
    }
// ------------------------------------------------

// ------------- Validate Total Marks --------------
// ------- Start --------
function validateTotalMarks(input) {
    // Remove any non-numeric characters
    input.value = input.value.replace(/[^0-9]/g, '');

        // Limit the input to 4 digits
        if (input.value.length > 4) {
            input.value = input.value.slice(0, 4);
        }      
    }
// ------------------------------------------------

// ------------- Validate Percentage --------------
// ------- Start --------
function validatePercentage(input) {
    // Allow only numeric characters and a single decimal point
    input.value = input.value.replace(/[^0-9.]/g, '');

    // Prevent multiple decimal points
    if ((input.value.match(/\./g) || []).length > 1) {
        input.value = input.value.substring(0, input.value.lastIndexOf('.'));
    }

    // Limit to three digits before the decimal point and two digits after
    const regex = /^(\d{1,3})(\.\d{0,2})?$/;
    if (!regex.test(input.value)) {
        input.value = input.value.slice(0, -1);
    }

    // Ensure the value does not exceed 100.00
    if (parseFloat(input.value) > 100) {
        input.value = "100.00";
    }
}
// ------------------------------------------------