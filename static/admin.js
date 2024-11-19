// ----------------------------------------------
// ------ This code is for Send Bulk Emails -----
// Update preview as the user types
$('#subject').on('input', function () {
    $('.subject_text').html($(this).val())
})

$('#body').on('input', function () {
    $('.msg_text').html($(this).val())
})

$(document).ready(function () {
    // Attach a submit event handler to the form
    $('#emailForm').submit(function (event) {
        event.preventDefault();  // Prevent the form from submitting normally

        // Use AJAX to submit the form data and update the textarea
        $.ajax({
            type: 'POST',
            url: '/sendbulkEmails',
            data: $(this).serialize(),
            success: function (data) {
                // Update the textarea if email_list is defined
                if (data.email_list) {
                    $('#emailRecipients').val(data.email_list.join(', '));
                } else {
                    $('#emailRecipients').val('No emails found.');
                }
            },
            error: function (error) {
                console.log('Error:', error);
            }
        });
    });
});

// Function to handle button click events
$(document).ready(function() {
    $('.export-excel').click(function(event) {
      event.preventDefault();
      // Check if the user has read-only access
      var hasReadOnlyAccess = true; // Replace this with your logic to determine read-only access
      if (hasReadOnlyAccess) {
        // Show SweetAlert modal
        Swal.fire({
          icon: 'warning',
          title: 'Read Only Access',
          text: 'Please contact the administrator to request Execution Access, as your current access level is Read Only.',
          confirmButtonColor: '#3085d6',
          confirmButtonText: 'OK'
        });
      } else {
        // Continue with button action if user has appropriate access
        // You can add your export or send email logic here
      }
    });
});
// ----------------------------------------------
// ------ End Code for Send Bulk Emails -----



// ----------------------------------------------
// ------ This code is for Student Manage Dashboard Page -----
// Function to handle button click events
$(document).ready(function() {
    $('.export-excel').click(function(event) {
      event.preventDefault();
      // Check if the user has read-only access
      var hasReadOnlyAccess = true; // Replace this with your logic to determine read-only access
      if (hasReadOnlyAccess) {
        // Show SweetAlert modal
        Swal.fire({
          icon: 'warning',
          title: 'Read Only Access',
          text: 'Please contact the administrator to request Execution Access, as your current access level is Read Only.',
          confirmButtonColor: '#3085d6',
          confirmButtonText: 'OK'
        });
      } else {
        // Continue with button action if user has appropriate access
        // You can add your export or send email logic here
      }
    });
});
// ----------------------------------------------
// ------ END code is for Student Manage Dashboard Page -----


// ------ This code is for Student Manage Dashboard Page Old User Insertion by Admin -----
// Function to update Ph.D. Registration Year field based on selected year
    function updateRegistrationYear() {
        // Get the selected year value
        var selectedYear = document.getElementById("year").value;

        // Extract the start year from the selected option (e.g., "2020 - 2021" -> "2020")
        var startYear = selectedYear.split(" - ")[0];

        // Update the Ph.D. Registration Year field value
        document.getElementById("phd_registration_year").value = startYear;
    }

    // Add event listener to the Year dropdown to trigger the update
    document.getElementById("year").addEventListener("change", updateRegistrationYear);
// ------ END code is for Student Manage Dashboard Page Old User Insertion by Admin -----