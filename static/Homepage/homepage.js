
// --------------------------------------------------------
//                   HOMEPAGE JS
// --------------------------------------------------------

$(document).ready(function () {
      $('.counter-value').each(function () {
        $(this).prop('Counter', 0).animate({
          Counter: $(this).text()
        }, {
          duration: 3500,
          easing: 'swing',
          step: function (now) {
            $(this).text(Math.ceil(now));
          }
        });
      });
    });
// --------------------------------------------------------
//                  END HOMEPAGE JS
// --------------------------------------------------------


// --------------------------------------------------------
//                  GR PAGE JS
// --------------------------------------------------------

var homeButton = document.getElementById("home-tab");

// Attach a click event listener to the "Home" button
homeButton.addEventListener("click", function() {
  // Load the PDF when the "Home" button is clicked
  loadPDF('static/GRAMSATHI GR 1.pdf');
});

// Function to load the PDF into the iframe
function loadPDF(pdfPath) {
  var pdfFrame = document.getElementById("pdfFrame");
  pdfFrame.src = pdfPath;
}

// --------------------------------------------------------
//                  END GR PAGE JS
// --------------------------------------------------------

// --------------------------------------------------------
//                  LOGIN & SIGNUP JS
// --------------------------------------------------------

$(document).ready(function () {
        $('#year').on('change',function(){
            var year=$('#year').val()
            if (year === '2021' || year === '2022') {
                      Swal.fire({
                        icon: "info",
                        title: "IT SEEMS YOU ARE AN OLD USER....",
                        text: `LOGIN IS ALREADY CREATED FOR YOU. Please Login with the registered email ID and Password for your login will be Fellowship123.`,

                      });
                      $('#year').val('')
            }
        })
    })

$(document).ready(function () {
    $('#signup_wrapper').hide()
    // Get the current page's URL
    var currentPageURL = window.location.href;

    // Loop through the menu items and compare their href attributes to the current URL
    $('#navbar li a').each(function () {
        var menuItemURL = $(this).attr('href');
        if (currentPageURL.includes(menuItemURL)) {
            // If the current URL includes the menu item's URL, add the 'active' class
            $(this).closest('li a').addClass('active');
        }
    });

    $('#signup').on('click', function () {
        $('#login_wrapper').animate({
            opacity: 0, // Target opacity value (0 to 1 for fading in)
            top: '0', // Target left position (e.g., 100px from the left)
            // width: '0px', // Target width (e.g., 200px)
        }, 1000, function () {
            $('#login_wrapper').hide()
            $('#signup_wrapper').show().animate({
                opacity: 1, // Target opacity value (0 to 1 for fading in)
                top: '0',
                // width: '80%',
            }, 1100);
        });
    })
    $('#login_switch').on('click', function () {
        $('#signup_wrapper').animate({
            opacity: 0, // Target opacity value (0 to 1 for fading in)
            // width: '0',
        }, 1500, function () {
            $('#signup_wrapper').hide()
            $('#login_wrapper').show().animate({
                opacity: 1, // Target opacity value (0 to 1 for fading in)
                bottom: '0',
                // width: '80%',
            }, 1000);
        });
    })

});
// --------------------------------------------------------
//                  END LOGIN & SIGNUP JS
// --------------------------------------------------------