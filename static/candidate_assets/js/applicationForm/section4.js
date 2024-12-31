// This function is for PVTG Caste
function toggleGovField(select) {
    const gov_Field = document.getElementById('open_gov');
    const position_Field = document.getElementById('open_gov1');
    const inputField1 = document.getElementById('gov_department');
    const inputField2 = document.getElementById('gov_position');

    if (select.value === 'Yes') {
        gov_Field.classList.remove('d-none'); // Show field
        position_Field.classList.remove('d-none'); // Show field
    } else {
        gov_Field.classList.add('d-none'); // Hide field
        position_Field.classList.add('d-none'); // Hide field
        inputField1.value = ''; // Clear input field
        inputField2.value = ''; // Clear input field
    }
}
// ----------------------------------------------------------------


// ----------- Account Number validation -------------------
function validateAccountNumber() {
    var accountNumberInput = document.getElementById('account_number');
    var accountNumberNumber = accountNumberInput.value;

    // Remove any non-numeric characters
    accountNumberInput.value = accountNumberNumber.replace(/[^0-9]/g, '');

    // Ensure length is exactly 20 characters
    if (accountNumberInput.value.length > 20){
        accountNumberInput.value = accountNumberInput.value.slice(0, 20);
    }
}
// ---------------------------------------------------------


// ----------- Account Holder Name validation -------------------
function validateAccountHolderName() {
    const nameInput = document.getElementById('account_holder_name');
    const nameValue = nameInput.value.trim();

    // Split the input by spaces and filter out empty parts
    const words = nameValue.split(/\s+/).filter(word => word);

    if (words.length < 3 || words.length > 3) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Name Detected',
            text: 'The Account Holder Name must have exactly 3 words.'
        });
        nameInput.value = ''; // Clear the input field
        nameInput.focus();
        return false;
    }

    // Check for non-alphabetic characters (optional)
    const validName = /^[a-zA-Z\s]+$/.test(nameValue);
    if (!validName) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Langauge Detected',
            text: 'The Account Holder Name should only contain letters and spaces.'
        });
        nameInput.value = ''; // Clear the input field
        nameInput.focus();
        return false;
    }

    return true;
}
// ---------------------------------------------------------


// ----------- IFSC Code validation -------------------
function validateIFSC() {
    const ifscInput = document.getElementById('ifsc_code');
    const bank_nameInput = document.getElementById('bank_name');
    const micrInput = document.getElementById('micr');
    const ifscValue = ifscInput.value.trim();

    // Regular expression for IFSC Code validation
    const ifscRegex = /^[A-Z]{4}0[A-Z0-9]{6}$/;

    if (!ifscRegex.test(ifscValue)) {
        Swal.fire({
            title: "Invalid IFSC Code",
            text: "The IFSC Code should be exactly 11 characters long, starting with 4 alphabets, followed by 0, and ending with 6 alphanumeric characters.",
            icon: "info",
            confirmButtonText: "Okay",
            customClass: {
                confirmButton: 'btn btn-primary'
            }
        }).then(() => {
            ifscInput.value = ''; // Clear the input field
            bank_nameInput.value = ''; // Clear the input field
            micrInput.value = ''; // Clear the input field
            ifscInput.focus(); // Bring focus back to the input
        });
        return false;
    }

    return true;
}
// ---------------------------------------------------------


// ----------- Autopopulate BAnk name and micr validation -------------------
$('#ifsc_code').on('blur', function () {
    let ifsc = $(this).val()
    $.ajax({
        url: "/get_ifsc_data",
        type: "GET",
        data: { 'ifsc': ifsc },
        success: function (html) {
            $('#bank_name').val(html.BANK)
            $('#micr').val(html.MICR)
        }
    })
})
// ---------------------------------------------------------
