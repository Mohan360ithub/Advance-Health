// frappe.ready(function() {
//     // Function to handle form submission
//     var handleFormSubmission = function(event) {
//         event.preventDefault(); // Prevent default form submission
        
//         var formData = {};
//         // Get field values from the form
//         $(".web-form-container :input").each(function(){
//             var fieldName = $(this).attr('data-fieldname');
//             if (fieldName !== 'customer_id') { // Skip the read-only field
//                 formData[fieldName] = $(this).val();
//             }
//         });
 
//         var customer_id = $("input[data-fieldname='customer_id']").val(); // Get value of read-only field
//         console.log(customer_id); // Debug statement
//         var from_date = formData['from_date'];
//         var to_date = formData['to_date'];
 
//         // Check if customer_id, date, and to_date are provided
//         if (!customer_id || !from_date || !to_date) {
//             frappe.msgprint(__("Please fill in all required fields."));
//             return false;
//         }
 
//         // Check if to_date is after the date
//         if (new Date(to_date) <= new Date(from_date)) {
//             frappe.msgprint(__("To Date must be after the From Date."));
//             return false;
//         }
 
//         // Check if there's already an admission form for the same customer that overlaps with the specified period
//         frappe.call({
//             method: "advance_health.custom_script.validate_overlap",
//             args: {
//                 customer_id: customer_id, // Pass customer_id to the Python function
//                 from_date: from_date,
//                 to_date: to_date
//             },
//             callback: function(r) {
//                 if (r.message) {
//                     frappe.msgprint(r.message);
//                 } else {
//                     // If validation passes, submit the form
//                     $(".web-form-container form").submit();
//                 }
//             }
//         });
 
//         return false; // Prevent default form submission
//     };
 
//     // Attach event listener to form submission button
//     $(".submit-btn").click(function(event) {
//         handleFormSubmission(event);
//     });
//     $("input[data-fieldname='customer_id']").prop('readonly', true);
 
// });
