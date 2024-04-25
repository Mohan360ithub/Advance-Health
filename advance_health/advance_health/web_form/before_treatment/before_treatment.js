frappe.ready(function() {
    // Function to handle form submission
    var handleFormSubmission = function(event) {
        event.preventDefault(); // Prevent default form submission
        
        var formData = {};
        // Get field values from the form
        $(".web-form-container :input").each(function(){
            var fieldName = $(this).attr('data-fieldname');
            if (fieldName !== 'customer_id') { // Skip the read-only field
                formData[fieldName] = $(this).val();
            }
        });

        var customer_id = $("input[data-fieldname='customer_id']").val(); // Get value of read-only field
        // console.log(customer_id); // Debug statement
        var form_id = formData['form_id']; // Get form_id from the form

        // Check if customer_id and form_id are provided
        if (!customer_id || !form_id) {
            frappe.msgprint(__("Please fill in all required fields."));
            return false;
        }

        // Check if there's already a form with the same customer_id and form_id
        frappe.call({
            method: "advance_health.custom_script.validate_duplicate_before_form",
            args: {
                customer_id: customer_id,
                form_id: form_id
            },
            callback: function(r) {
                if (r.message) {
                    frappe.msgprint(r.message);
                } else {
                    // If validation passes, submit the form
                    $(".web-form-container form").submit();
                }
            }
        });

        return false; // Prevent default form submission
    };

    // Attach event listener to form submission button
    $(".submit-btn").click(function(event) {
        handleFormSubmission(event);
    });
    $("input[data-fieldname='customer_id']").prop('readonly', true);
    $("input[data-fieldname='form_id']").prop('readonly', true);
});
