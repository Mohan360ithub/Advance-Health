from frappe.model.document import Document
import frappe

class AdmissionForm(Document):
    def on_update(self):
        self.create_user()
        self.send_email_to_customer()

    def create_user(self):
        existing_user = frappe.get_all('User', filters={'email': self.email_id}, fields=['name'])
        
        if existing_user:
            frappe.msgprint("User already exists with this email.")
        else:
            user_doc = {
                'doctype': 'User',
                'email': self.email_id,
                'first_name': self.name_of_applicant if self.name_of_applicant else 'DefaultFirstName',
                'contact_no': self.contact_no,
                'send_welcome_email': False,
                'module_profile': 'No'  # Setting module_profile to 'No'
            }

            user = frappe.get_doc(user_doc)

            # Set the contact number as the password
            user.new_password = self.contact_no

            # Assign role
            role = frappe.get_all('Role', filters={'name': 'Advance Health Customer'}, fields=['name'])
            if role:
                user.add_roles(role[0]['name'])
                user.save()
                frappe.msgprint("User created successfully.")
            else:
                frappe.msgprint("Role 'Advance Health Customer' not found.")

    def send_email_to_customer(self):
        # Retrieve the customer_name from the Customer doctype
        customer_name = frappe.get_value("Customer", self.customer_id, "customer_name")
        custom_contact_no = frappe.get_value("Customer", self.customer_id, "custom_contact_no")
        
        # Retrieve the URL for the Before Treatment form
        before_treatment_url = f"/before-treatment/new?customer_id={self.customer_id}&form_id={self.name}&customer_name={customer_name}&custom_contact_no={custom_contact_no}"
        
        # Construct the HTML message body with user details and the link to Before Treatment form
        message = f"""<html>
                    <body>
                        <p>Dear {customer_name},</p>
                        <p>Thank you for your submission. Here are your login credentials:</p>
                        <p><b>Email:</b> {self.email_id}</p>
                        <p><b>Password:</b> {self.contact_no}</p>
                        <p>Please keep these credentials secure.</p>
                        <p>In order to deliver the best treatment, we would like to understand you better. Kindly fill out <a href="{before_treatment_url}">this form</a> with complete honesty so that we can assess your exact state before starting treatment.</p>
                    </body>
                    </html>"""

        subject = "Login Credentials and Before Treatment Form"
        recipients = self.email_id
        sender = "custom_sender_email_id@example.com"  # Custom sender email address

        # Send email using Frappe's email function
        frappe.sendmail(recipients=recipients, sender=sender, subject=subject, message=message)
