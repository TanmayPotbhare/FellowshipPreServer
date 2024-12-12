function validateIncome() {
    var incomeInput = document.getElementById('family_annual_income');
    var income = incomeInput.value;

    // Remove any non-numeric characters
    incomeInput.value = incomeInput.value.replace(/[^0-9]/g, '');

    // Limit the input to 6 digits
    if (incomeInput.value.length > 6) {
        incomeInput.value = incomeInput.value.slice(0, 6);
    }

    // Check if income exceeds 8 Lacs (8,00,000)
    if (parseInt(incomeInput.value) > 800000) {
        // If income is more than 8 Lacs, show a popup message
        alert("To avail the fellowship, the income should be less than 8 Lacs.");
        incomeInput.value = ''; // Reset the input field
    }
}


function validateIncomeCertificateNumber() {
    var incomeCertificateInput = document.getElementById('income_certificate_number');
    var incomeCertificateNumber = incomeCertificateInput.value;

    // Remove any non-numeric characters
    incomeCertificateInput.value = incomeCertificateNumber.replace(/[^0-9]/g, '');

    // Ensure length is exactly 20 characters
    if (incomeCertificateInput.value.length > 20){
        incomeCertificateInput.value = incomeCertificateInput.value.slice(0, 20);
    }
}


function validateDomicileCertificateNumber() {
    var domicileCertificateInput = document.getElementById('domicile_number');
    var domicileCertificateNumber = domicileCertificateInput.value;

    // Remove any non-numeric characters
    domicileCertificateInput.value = domicileCertificateNumber.replace(/[^0-9]/g, '');

    // Ensure length is exactly 20 characters
    if (domicileCertificateInput.value.length > 20){
        domicileCertificateInput.value = domicileCertificateInput.value.slice(0, 20);
    }
}



function validateCasteCertificateNumber() {
    var casteCertificateInput = document.getElementById('caste_certf_number');
    var casteCertificateNumber = casteCertificateInput.value;

    // Remove any non-numeric characters
    casteCertificateInput.value = casteCertificateNumber.replace(/[^0-9]/g, '');

    // Ensure length is exactly 20 characters
    if (casteCertificateInput.value.length > 20){
        casteCertificateInput.value = casteCertificateInput.value.slice(0, 20);
    }
}


function validateValidityCertificateNumber() {
    var validityCertificateInput = document.getElementById('validity_cert_number');
    var validityCertificateNumber = validityCertificateInput.value;

    // Remove any non-numeric characters
    validityCertificateInput.value = validityCertificateNumber.replace(/[^0-9]/g, '');

    // Ensure length is exactly 20 characters
    if (validityCertificateInput.value.length > 20){
        validityCertificateInput.value = validityCertificateInput.value.slice(0, 20);
    }

}