$(document).ready(function () {
    // On change get all details related to pincode
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


    // percentage validation on section 2
    $('.percentage_validation').on('blur', function () {
        if ($(this).val() < 35) {
            Swal.fire({
                title: "Sorry",
                text: "Below 35 percentage not accepted",
                icon: "error"
            });
        }
        else if ($(this).val() > 100) {
            Swal.fire({
                title: "Wrong Percentage",
                text: "Please Enter Correct Percentage",
                icon: "info"
            });
        }
    })
    $('#your_caste').on('change', function () {
        let values = $('option:selected', this).attr('data-hidden')
        let value_array = values.split(',')
        $('#subcaste').empty()
        $('#subcaste').append('<option>-- Select Sub Caste / Tribe --</option>')
        value_array.forEach(function (item) {

            $('#subcaste').append(`<option value="${item}">${item}</option`);

        });
    })
    // $('#phd_registration_date').on('blur', function () {
    //     let dob = $('#dob').val()
    //     let phd_registration_date = $('#phd_registration_date').val()
    //     if (dob == '') {
    //         Swal.fire({
    //             title: "Field required",
    //             text: "Please Enter date of birth first",
    //             icon: "info"
    //         });
    //         $('#dob').val('')
    //         $('#phd_registration_date').val('')
    //     } else {
    //         let year1 = parseInt(dob.split('-')[0]);
    //         let year2 = parseInt(phd_registration_date.split('-')[0]);
    //         // Calculate the difference in years
    //         let age = year2 - year1 - 1;
    //         if (age > 45 || age < 18) {
    //             Swal.fire({
    //                 icon: 'error',
    //                 title: 'Oops...',
    //                 text: "We're sorry, but this Fellowship is only open to individuals aged 18 to 45. Thank you for your interest.",
    //                 footer: '<a href="/">Sign Out</a>'
    //             })
    //         } else {
    //             $('#age').val(age).prop('readonly', true);
    //         }
    //     }
    // })

    $('#pvtg').on('change', function(){
        if($(this).val()=='Yes'){
            $('#pvtg_caste').attr('disabled', false)
        }
        else
        {
            $('#pvtg_caste').attr('disabled', true)
        }
    })

    $('#section1').submit(function(e){
        $('#pvtg_caste').attr('disabled',false)
    })

    $('#section1 input').on('keypress', function (e) {
        if (e.which == 13 || e.which == 10) {
            e.preventDefault();  // Fix the typo here
            return false;
        }
    });

    $('#adhaar_seeding_bank').on('change', function () {
        var inputValue = $(this).val();
        // Test if the input value contains only text
        if (inputValue == 'No') {
            Swal.fire({
                icon: 'warning',
                title: 'This is Mandatory - Please send within 15 Days',
                text: "Please send the document within in 10 days after submission of Form to - it_helpdesk@icspune.com",
                footer: '<a href="/">Sign Out</a>'
            });
        }
    })

})




