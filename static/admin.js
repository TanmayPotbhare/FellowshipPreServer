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


// ---------------------- Start Selected Year on Admin Dashboard --------------
// Event listener to update the dashboard data based on selected year
document.getElementById("yearSelector").addEventListener("change", function() {
    const selectedYear = this.value;

    // Make an AJAX request to get the data for the selected year
    fetch(`/get_year_count?year=${selectedYear}`)
        .then(response => response.json())
        .then(data => {
            // Update the dashboard with the new data
            document.getElementById("total_appl_count").textContent = data.total_appl_count;
            document.getElementById("completed_form_count").textContent = data.completed_form_count;
            document.getElementById("incomplete_form_count").textContent = data.incomplete_form_count;
            document.getElementById("accepted_appl_count").textContent = data.accepted_appl_count;
            document.getElementById("rejected_appl_count").textContent = data.rejected_appl_count;
            document.getElementById("maleCount").textContent = data.male_count;
            document.getElementById("femaleCount").textContent = data.female_count;

            // Update the year in multiple places
            const yearChange = this.options[this.selectedIndex].innerHTML;
            // Update all elements with the class 'yearChange'
            const yearChangeElements = document.querySelectorAll('.yearChange');
            yearChangeElements.forEach(element => {
                element.innerHTML = yearChange;
            });
        })
        .catch(error => {
                            console.error('Error fetching data:', error);
                            alert('Failed to load the data for the selected year.');
                        });
});

// ---------------------- END Selected Year on Admin Dashboard --------------


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





