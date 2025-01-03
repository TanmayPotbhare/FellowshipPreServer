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
        Swal.fire({
                    title: "Income Criteria Not Met",
                    text: "To avail the fellowship, the income should be less than or equal to 8 Lacs.",
                    icon: "error"
                });
        incomeInput.value = ''; // Reset the input field
    }
    if (parseInt(incomeInput.value) <= 0) {
        // If income is more than 8 Lacs, show a popup message
        Swal.fire({
                    title: "Income Criteria Not Met",
                    text: "To avail the fellowship, the income should be less than or equal to 8 Lacs.",
                    icon: "error"
                });
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


document.getElementById('income_issuing_district').addEventListener('change', function() {
    const districtId = this.selectedOptions[0].getAttribute('data-hidden');
    fetch(`/get_talukas/${districtId}`)
        .then(response => response.json())
        .then(data => {
            const talukaSelect = document.getElementById('income_issuing_taluka');
            talukaSelect.innerHTML = '<option value="">-- Select Taluka --</option>'; // Reset taluka dropdown
            data.talukas.forEach(taluka => {
                const option = document.createElement('option');
                option.value = taluka;
                option.textContent = taluka;
                talukaSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching talukas:', error));
});


document.getElementById('domicile_issuing_district').addEventListener('change', function() {
    const districtId = this.selectedOptions[0].getAttribute('data-hidden');
    fetch(`/get_talukas/${districtId}`)
        .then(response => response.json())
        .then(data => {
            const talukaSelect = document.getElementById('domicile_issuing_taluka');
            talukaSelect.innerHTML = '<option value="">-- Select Taluka --</option>'; // Reset taluka dropdown
            data.talukas.forEach(taluka => {
                const option = document.createElement('option');
                option.value = taluka;
                option.textContent = taluka;
                talukaSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching talukas:', error));
});


document.getElementById('issuing_district').addEventListener('change', function() {
    const districtId = this.selectedOptions[0].getAttribute('data-hidden');
    fetch(`/get_talukas/${districtId}`)
        .then(response => response.json())
        .then(data => {
            const talukaSelect = document.getElementById('caste_issuing_taluka');
            talukaSelect.innerHTML = '<option value="">-- Select Taluka --</option>'; // Reset taluka dropdown
            data.talukas.forEach(taluka => {
                const option = document.createElement('option');
                option.value = taluka;
                option.textContent = taluka;
                talukaSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching talukas:', error));
});


document.getElementById('validity_issuing_district').addEventListener('change', function() {
    const districtId = this.selectedOptions[0].getAttribute('data-hidden');
    fetch(`/get_talukas/${districtId}`)
        .then(response => response.json())
        .then(data => {
            const talukaSelect = document.getElementById('validity_issuing_taluka');
            talukaSelect.innerHTML = '<option value="">-- Select Taluka --</option>'; // Reset taluka dropdown
            data.talukas.forEach(taluka => {
                const option = document.createElement('option');
                option.value = taluka;
                option.textContent = taluka;
                talukaSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching talukas:', error));
});


$('#domicile').on('change', function () {
    if($(this).val() == 'Yes'){
        $('#domicile_number').attr('disabled',false)
        $('#domicile_issuing_authority').attr('disabled',false)
        $('#domicile_issuing_district').attr('disabled',false)
        $('#domicile_issuing_taluka').attr('disabled',false)
    }else if($(this).val() == 'No'){
        Swal.fire({
                title: "Sorry",
                text: "Sorry, you cannot apply to this scheme, Domicile Certificate is mandatory",
                icon: "error"
            });
        $('#domicile_number').attr('disabled',true)
        $('#domicile_issuing_authority').attr('disabled',true)
        $('#domicile_issuing_district').attr('disabled',true)
        $('#domicile_issuing_taluka').attr('disabled',true)
        $('#domicile').val('')
        $('#domicile_number').val('')
        $('#domicile_issuing_authority').val('')
        $('#domicile_issuing_district').val('')
        $('#domicile_issuing_taluka').val('')
    }
})



$('#caste_certf').on('change', function () {
    if($(this).val() == 'Yes'){
        $('#caste_certf_number').attr('disabled',false)
        $('#caste_issuing_authority').attr('disabled',false)
        $('#issuing_district').attr('disabled',false)
        $('#caste_issuing_taluka').attr('disabled',false)
    }else if($(this).val() == 'No'){
        Swal.fire({
                title: "Sorry",
                text: "Sorry, you cannot apply to this scheme, Caste/Tribe Certificate is mandatory",
                icon: "error"
            });
        $('#caste_certf_number').attr('disabled',true)
        $('#caste_issuing_authority').attr('disabled',true)
        $('#issuing_district').attr('disabled',true)
        $('#caste_issuing_taluka').attr('disabled',true)

        $('#caste_certf').val('')
        $('#caste_certf_number').val('')
        $('#caste_issuing_authority').val('')
        $('#issuing_district').val('')
        $('#caste_issuing_taluka').val('')
    }
})



$('#validity_certificate').on('change', function () {
    if($(this).val() == 'Yes'){
        $('#validity_cert_number').attr('disabled',false)
        $('#validity_issuing_authority').attr('disabled',false)
        $('#validity_issuing_district').attr('disabled',false)
        $('#validity_issuing_taluka').attr('disabled',false)
    }else if($(this).val() == 'No'){
        Swal.fire({
                title: "Sorry",
                text: "Sorry, you cannot apply to this scheme, Validity Certificate is mandatory",
                icon: "error"
            });
        $('#validity_cert_number').attr('disabled',true)
        $('#validity_issuing_authority').attr('disabled',true)
        $('#validity_issuing_district').attr('disabled',true)
        $('#validity_issuing_taluka').attr('disabled',true)

        $('#validity_certificate').val('')
        $('#caste_certf_number').val('')
        $('#caste_issuing_authority').val('')
        $('#issuing_district').val('')
        $('#caste_issuing_taluka').val('')
    }
})

// Function to enable or disable the submit button
function enableDisabledFields3() {
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
    enableDisabledFields2();
};